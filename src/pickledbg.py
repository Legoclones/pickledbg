#!/usr/bin/env python3

###############################################################################
# 
# pickledbg - a simple Python pickle debugger
# 
# This class overrides the _Unpickler class from the pickle module to provide
# a simple command-line interface for debugging pickled objects. It allows
# stepping through the unpickling process and inspecting the stack and memo.
# The format and design was meant to look and function similar to GEF, 
# including color schemes.
# 
###############################################################################


### GLOBAL IMPORTS ###
import sys, io, pickletools
from os import system, get_terminal_size
import readline
from pickle import _Unpickler, _Unframer, _Stop


### LOCAL IMPORTS ###
from colors import *
from errors import *
from util import *


### CLASSES ###
class DbgUnpickler(_Unpickler):
    def __init__(self, file, *, fix_imports=True,
                 encoding="ASCII", errors="strict", buffers=None,
                 pickle_disasm: list[str] = []):
        self._buffers = iter(buffers) if buffers is not None else None
        self._file_readline = file.readline
        self._file_read = file.read
        self.memo = {}
        self.encoding = encoding
        self.errors = errors
        self.proto = 0
        self.fix_imports = fix_imports

        ### EVERYTHING BELOW THIS LINE IS CUSTOM DEBUGGER CODE ###
        self.pickle_disasm = pickle_disasm
        self.disasm_line_no = 0
        self.addresses = [int(line.split(":")[0]) for line in self.pickle_disasm]
        self.curr_addr = lambda: self.addresses[self.disasm_line_no]
        self.options = {'step-verbose': False}
        if self.pickle_disasm == []:
            self.disas_failed = True
        else:
            self.disas_failed = False

    def load(self):
        if not hasattr(self, "_file_read"):
            raise UnpicklingError("Unpickler.__init__() was not called by "
                                  "%s.__init__()" % (self.__class__.__name__,))
        self._unframer = _Unframer(self._file_read, self._file_readline)
        self.read = self._unframer.read
        self.readinto = self._unframer.readinto
        self.readline = self._unframer.readline
        self.metastack = []
        self.stack = []
        self.append = self.stack.append
        self.proto = 0

        ### EVERYTHING BELOW THIS LINE IS CUSTOM DEBUGGER CODE ###
        self.last_command = None
        self.start = False
        try:
            while True:
                self.handle_input()
        except _Stop as stopinst:
            return stopinst.value

    def handle_input(self, inp=None):
        """Handles user input for the debugger.
        
        If ENTER is pressed without any input, the last command is repeated."""
        # get input from the user
        if inp is None:
            try:
                inp = input(greenify("pickledbg>  "))
            except (EOFError, KeyboardInterrupt):
                raise PickleDBGError("Quitting...")

        # case-insensitive handling
        inp = inp.lower().strip()

        if inp == "ni" or inp == "next":
            if not self.start:
                print(redify("[-] You must start the debugger first. Try using the 'start' command."))
                return

            self.last_command = inp

            # run the next instruction
            key = self.read(1)
            if not key:
                raise EOFError
            assert isinstance(key, (bytes, bytearray))

            self.dispatch[key[0]](self)

            # print current state
            self.disasm_line_no += 1
            self.print_state()

        elif inp.startswith("step "):
            if not self.start:
                print(redify("[-] You must start the debugger first. Try using the 'start' command."))
                return

            self.last_command = inp

            try:
                steps = int(inp[5:])
            except:
                print(redify("[-] Invalid command. Enter 'step <number>' to step through a number of instructions."))
                return

            for _ in range(steps):
                # run the next instruction
                key = self.read(1)
                if not key:
                    raise EOFError
                assert isinstance(key, (bytes, bytearray))

                self.dispatch[key[0]](self)

                # print current state
                self.disasm_line_no += 1
                if self.options['step-verbose']:
                    self.print_state()

            if not self.options['step-verbose']:
                self.print_state()

        elif inp.startswith("step-to "):
            if not self.start:
                print(redify("[-] You must start the debugger first. Try using the 'start' command."))
                return

            if self.disas_failed:
                print(redify("[-] Disassembly failed. Cannot step to a specific instruction."))
                return

            self.last_command = inp

            try:
                step_to = int(inp[8:])
            except:
                print(redify("[-] Invalid command. Enter 'step-to <address>' to step to a specific instruction address."))
                return

            if step_to < self.curr_addr():
                print(redify("[-] Invalid command. You cannot step backwards."))
                return

            if step_to not in self.addresses:
                print(redify("[-] Invalid command. Invalid instruction address, check the disassembly."))
                return

            while self.curr_addr() < step_to:
                # run the next instruction
                key = self.read(1)
                if not key:
                    raise EOFError
                assert isinstance(key, (bytes, bytearray))

                self.dispatch[key[0]](self)

                # print current state
                self.disasm_line_no += 1

                if self.options['step-verbose']:
                    self.print_state()

            if not self.options['step-verbose']:
                self.print_state()

        elif inp == "start" or inp == "run":
            self.last_command = inp

            if self.start:
                print(redify("[-] Debugger already started. You must exit and restart the program again."))
                return

            self.start = True
            self.print_state()

        elif inp == "":
            # repeat last command
            self.handle_input(self.last_command)

        elif inp[:6] == "export":
            self.last_command = inp

            filename = "out.disasm"

            if len(inp) > 6:
                if inp[6] == " ":
                    filename = inp[7:].strip()
                else:
                    print(redify("[-] Invalid command. Type 'help' for a list of available commands."))
                    return

            print("Exporting disassembly to " + filename + "...")

            try:
                with open(filename, "w") as tmpfile:
                    pickletools.dis(open(sys.argv[1], "rb"), out=tmpfile)
            except:
                print(redify("[-] Error: could not export pickle disassembly"))

        elif inp == '?' or inp.startswith('help'):
            self.last_command = inp

            try:
                arg = inp.split()[1]
            except:
                arg='pickledbg help'

            terminal_width = get_terminal_size()[0]
            lengths = (terminal_width - len(f' {arg} '))//2
            print(grayify('─'*lengths)+cyanify(f' {arg} ')+grayify('─'*lengths))

            if arg == 'pickledbg help':
                print_help(terminal_width)

            elif arg == 'options':
                print(redify("step-verbose"))
                print(f"When set to {blueify('true')}, the debugger will print the state of the Pickle Machine after each instruction rather than just the final state.")
                print(f"{yellowify("Default:")} {blueify('false')}")
                print()
                print(grayify('─'*terminal_width))


        elif inp == "show options":
            self.last_command = inp

            terminal_width = get_terminal_size()[0]
            lengths = (terminal_width - len(' options '))//2
            print(grayify('─'*lengths)+cyanify(' options ')+grayify('─'*lengths))
            for option in self.options:
                print(blueify(option)+": "+str(self.options[option]))
            print(grayify('─' * terminal_width))    

        elif inp.startswith("set "):
            self.last_command = inp

            try:
                option = inp[4:].split(" ")[0]
                value = inp[4:].split(" ")[1]
            except:
                print(redify("[-] Invalid command. Enter 'set <option> <value>' to set an option."))
                return

            if option in self.options:
                if type(self.options[option]) == bool:
                    if value == "true":
                        self.options[option] = True
                    elif value == "false":
                        self.options[option] = False
                    else:
                        print(redify("[-] Invalid command. Enter 'set <option> <True/False>' to set this option."))
                else:
                    self.options[option] = value # When adding more options, add more checks here
            else:
                print(redify("[-] Invalid command. Option does not exist."))


        elif inp == "exit" or inp == "quit":
            raise PickleDBGError("Quitting...")

        else:
            print(redify("[-] Invalid command. Type 'help' for a list of available commands."))

    def print_state(self):
        """Prints the current state of the Pickle Machine.
        
        After another instruction has been consumed by the unpickling process,
        this function prints the PVM storage areas, including the stack, 
        metastack, and memo. It also prints the disassembly of the pickle file
        including the current instruction and 3 instructions before and after
        it.

        All information is printed after a `clear -x` command to move the data
        to the top of the terminal windows, *without* clearing the history.
        """
        system('clear -x')

        ### STACK & MEMO ###
        terminal_width = get_terminal_size()[0]
        print(header('stack & memo', terminal_width))
        print(blueify("stack     ")+": ", colorize_array(self.stack))
        if self.metastack != []: 
            print(blueify("metastack ")+": ", colorize_array(self.metastack))
        print(blueify("memo      ")+": ", colorize_dict(self.memo))

        ### DISASSEMBLY ###
        print(header('disassembly', terminal_width))

        try:
            # get up to 3 previous instructions
            tmp = '\n   '.join(self.pickle_disasm[max(0,self.disasm_line_no-3):self.disasm_line_no])
            if tmp != '':
                print('   '+grayify(tmp))

            # print current instruction
            print(greenify(' ➤ '+self.pickle_disasm[self.disasm_line_no]))

            # print up to 3 next instructions
            tmp = '\n   '.join(self.pickle_disasm[self.disasm_line_no+1:self.disasm_line_no+4])
            if tmp != '':
                print('   '+tmp)
        except IndexError:
            print(redify("[-] Error: could not print disassembly"))

        # footer
        print(grayify(''.join(['─' for _ in range(terminal_width)])))



### MAIN ###
def main():
    # check that pickle file is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <picklefile>")
        sys.exit(1)

    # try to read pickle_file
    try:
        pickle_file = open(sys.argv[1], "rb")
    except:
        print(redify(f"[-] Error: could not open '{sys.argv[1]}'"))
        sys.exit(1)

    # get pickletools disassembly
    try:
        output = io.StringIO()
        pickletools.dis(pickle_file, out=output)
        pickle_disasm = output.getvalue().split('\n')[:-2]
    except Exception as e:
        print(redify("[-] Error: could not disassemble pickle file, will try to continue anyway"))
        print(redify(str(e)))
        pickle_disasm = []

    # configure readline
    readline.set_completer_delims(' ')
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    try:
        final_value = DbgUnpickler(open(sys.argv[1], "rb"), pickle_disasm=pickle_disasm).load()
        print(greenify("\n[+] Unpickling complete. Final value: ") + cyanify(ascii(final_value)))
    except PickleDBGError as e:
        print(redify("\n[-] "+str(e)))


if __name__ == "__main__":
    main()