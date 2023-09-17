# pickledbg
`pickledbg` is a set of tools used to help analyze, create, and understand Python pickles. Many tools and documentation already exist, including [the official Python pickle documentation](https://docs.python.org/3/library/pickle.html), the [pickletools module for pickle disassembly](https://docs.python.org/3/library/pickletools.html), and the [Julia language's documentation for pickles](https://docs.juliahub.com/Pickle/LAUNc/0.3.2/). `pickledbg` introduces additional pickle-analyzing tools and more comprehensive documentation. `pickledbg.py` is a [GDB](https://www.sourceware.org/gdb/)+[GEF](https://github.com/hugsy/gef)-style debugger, where pickles are unpacked instruction by instruction, showing the Pickle Machine state (stack, metastack, and memo) at each step. `picklecomp.py` (not yet created) is used to make the generation of custom Python pickles easier, specifically intended for CTF pickle jails. Lastly, more extensive and clearer documentation is present in the `pickle_doc/` folder (not yet created), intended for you to understand each opcode, pickles as a whole, and relevant source code from one spot without having to go anywhere else.

## `pickledbg.py`
The current [pickle source code](https://github.com/python/cpython/blob/3.11/Lib/pickle.py) was used as the framework for this debugger, only adding in code and making minor modifications to print out the state and handle commands. The implementation of each opcode was untouched to ensure it behaves exactly as it would when normally being unpickled. The format and designed was meant to look and function similar to GEF, including color schemes.

Since pickles may be unloaded in a custom environment (extra modules imported, builtins modified/removed, etc.), a short section exists in the source code to add in that custom code. This should help simulate the unpickling process in an environment as close to the real-world one as possible. In addition, some builtins may be removed or overwritten either in the custom code or during the unpickling process, so "copies" of several builtins (such as `print`, `input`, `bool`, etc.) were created, and those copies are used inside any custom code added to the pickle source code. This ensures that debugging functionality will still work properly even if the environment is changed.

### Install
No dependencies need to be installed. A simple `git clone` should suffice. 

### Usage
```python
┌──(user㉿computer)-[~/pickledbg]
└─$ python3 pickledbg.py
Usage: pickledbg.py <picklefile>

┌──(user㉿computer)-[~/pickledbg]
└─$ python3 pickledbg.py test.pickle
pickledbg>  help
────────────────────────────────── pickledbg help ──────────────────────────────────
start
Starts the debugger, pointing to the first instruction but not executing it. Must
only be ran once. To restart debugging, close the program and run it again. Must
also be run before stepping through instructions.
Aliases: run

────────────────────────────────────────────────────────────────────────────────────
ni
Executes the next instruction and shows the updated Pickle Machine state. Must be
ran after 'start'.
Aliases: next

────────────────────────────────────────────────────────────────────────────────────
export
Writes the disassembly of the pickle to a file. If no filename is specified, the
default is 'out.disasm'.
Syntax: export [filename]

────────────────────────────────────────────────────────────────────────────────────
help
Shows this help menu.
Aliases: ?

────────────────────────────────────────────────────────────────────────────────────
exit
Exits the debugger.
Aliases: quit

────────────────────────────────────────────────────────────────────────────────────
pickledbg>
```

(*Example of what the debug interface looks like when running.*)

![](documentation.png)

## `picklecomp.py`
Work in progress

## Pickle Documentation
(work in progress) You can see Python pickle documentation [here](pickle_doc/).

## Notes
This tool may be periodically updated depending on how lazy I'm feeling. If you run into an issue, feel free to leave a note or make a pull request.
