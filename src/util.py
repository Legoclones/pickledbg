from typing import Optional, Union
import readline
from colors import *

commands = {
    'ni': [],
    'next': [],
    'step': [],
    'step-to': [],
    'start': [],
    'run': [],
    'export': [],
    '?': [],
    'exit': [],
    'quit': [],
    'set': {
        'step-verbose': ['true', 'false']
    },
    'show': ['options'],
    'help': ['options']
}


def completer(text: str, state: int) -> Optional[str]:
    """Completer function for readline to provide command completion.
    
    Args:
        text (str): The current text being completed.
        state (int): The state of the completion, used to iterate through options.

    Returns:
        Optional[str]: The next completion option or None if no more options are available.
    """
    buffer = readline.get_line_buffer().split()
    
    def get_options(cmd_tree: Union[dict, list], tokens: list[str], current_text: str) -> list[str]:
        # we only have a list of valid leaf commands
        if isinstance(cmd_tree, list):
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]
        
        if not tokens:
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]

        token = tokens[0]
        rest = tokens[1:]
        next_branch = cmd_tree.get(token)

        if next_branch is None:
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]

        return get_options(next_branch, rest, current_text)
    
    options = get_options(commands, buffer, text)
    if state < len(options):
        return options[state]
    else:
        return None


def print_help(terminal_width: int) -> None:
    """Prints the color-coded help menu for the Pickle Debugger."""
    # start
    print(redify("start"))
    print("Starts the debugger, pointing to the first instruction but not executing it. Must only be ran once. To restart debugging, close the program and run it again. Must also be run before stepping through instructions.")
    print(yellowify("Aliases:")+' run')
    print()
    print(grayify('─'*terminal_width))


    # ni
    print(redify("ni"))
    print("Executes the next instruction and shows the updated Pickle Machine state. Must be ran after 'start'.")
    print(yellowify("Aliases:")+' next')
    print()
    print(grayify('─'*terminal_width))
    

    # step
    print(redify("step"))
    print("Executes the next given number of instructions and shows the updated Pickle Machine state.")
    print(yellowify("Syntax:")+' step <number>')
    print()
    print(grayify('─'*terminal_width))
    

    # step-to
    print(redify("step-to"))
    print("Executes instructions until the instruction address is reached and shows the updated Pickle Machine state.")
    print(yellowify("Syntax:")+' step-to <address>')
    print()
    print(grayify('─'*terminal_width))


    # export 
    print(redify("export"))
    print("Writes the disassembly of the pickle to a file. If no filename is specified, the default is 'out.disasm'.")
    print(yellowify("Syntax:")+' export [filename]')
    print()
    print(grayify('─'*terminal_width))


    # show options
    print(redify("show options"))
    print("Shows the current options and their values.")
    print()
    print(grayify('─'*terminal_width))


    # set
    print(redify("set"))
    print("Sets an option to a value.")
    print(yellowify("Syntax:")+' set <option> <value>')
    print()
    print(grayify('─'*terminal_width))
    
    
    # help
    print(redify("help"))
    print("Shows this help menu. Type 'help options' for available options.")
    print(yellowify("Aliases:")+' ?')
    print()
    print(grayify('─'*terminal_width))


    # exit
    print(redify("exit"))
    print("Exits the debugger.")
    print(yellowify("Aliases:")+' quit')
    print()
    print(grayify('─'*terminal_width))