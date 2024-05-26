# Pickle Examples
## Hello World
*not yet implemented*

## Sickle
[`sickle.pickle`](sickle.pickle) is a pickle reverse engineering problem from SECCON CTF 2023 Quals that implements a flag checker. This pickle is unique because it was designed to include flow control, such as `jump` statements and `if` statements. It was defined as below:

```python
payload = b'<bytes>'

f = io.BytesIO(payload)
res = pickle.load(f)
```

The `f` variable used `seek` to jump ahead or behind in instructions based on how the pickle ran. Since this is not intended pickle behavior, the debugger won't work out-of-the-box with this functionality; source code adjustments are required.

## Snek
[`snek.pickle`](snek.pickle) is part of a reverse engineering problem from LACTF 2023 where unloading the pickle created a Python code object that ran a snake game that had to be reversed. Obtaining the code object from the pickle bytes was essential to pulling out the real source code for the game.