# Changelog

## 2.2.0 (2025-07-04)

### Additions
* Final value is printed when unpickling is finished without any errors.
* Dictionaries in lists/tuples are now color-coded.
* Dictionary keys are now color-coded.

### Changes
* ‼️**BIG**‼️ Pickledbg has been modified to be a subclass of `pickle._Unpickler` instead of a complete copy of the code. 
    * Only a few functions are overloaded, all other functions/classes/globals were removed, reducing code size significantly.
    * This way, as the mainstream Python `_Unpickler` class evolves, pickledbg doesn't require manual updates. Instead, it will use the default `_Unpickler` class for your Python version.
    * (don't ask me why I didn't do this in the first place, no idea)
* Some code cleanup including better comments and docstrings, function typing, and splitting up code more.

## 2.1.0 (2024-10-13)

### Additions (courtesy of [souvlakias](https://github.com/souvlakias) in [#1](https://github.com/Legoclones/pickledbg/pull/1))
* `step` command is added to step `x` instructions
* `step-to` command is added to step to a specific address
* `step-verbose` is added as an option (default set to `False`). When enabled, the `step` and `step-to` commands show the output of the Pickle Machine for *each* instruction run, not simply the last one run.
* `show options` command is added to list all available options.
* `set` command is added to change a default option.
* History is available in the commandline using up/down arrows and autocomplete is available

### Changes
* Fixed a bug so pickles that are valid but throw an error in `pickletools` are still run ([1ec62f8](https://github.com/Legoclones/pickledbg/commit/1ec62f8371403973a44d4b1c2f8d1ca6eece1a50))
* Updated code to match latest 3.13 version ([1a0da4d](https://github.com/Legoclones/pickledbg/commit/1a0da4d7c249682224c53ef40bb0e950c5cb9d29) and [8642887](https://github.com/Legoclones/pickledbg/commit/8642887ab423b046ceed7986d953f6987640af49))

## 2.0.0 (2024-06-13)

### Additions
* Examples have been added in the `examples/` folder

### Changes
* `pickledbg` can now be installed as a Python module through pip and is accessible through the command line

## 1.0.0 (2023-09-17)

Initial release.