# Pickle Examples
## Hello World
[`helloworld.pickle`](./helloworld.pickle) is a very simple hand-crafted pickle that simply runs `print('Hello World!')` when unpickled. It was crafted using the `pickleassem` module with the below code:

```python
import pickle, pickletools
from pickleassem import PickleAssembler

pa = PickleAssembler(proto=5)
pa.push_global('builtins','print')
pa.push_mark()
pa.push_short_binstring('Hello World!')
pa.build_tuple()
pa.build_reduce()
pk = pa.assemble()

print(pk)
pickletools.dis(pk)
pickle.loads(pk)
```

Output:
```python
b'\x80\x05cbuiltins\nprint\n(U\x0cHello World!tR.'
    0: \x80 PROTO      5
    2: c    GLOBAL     'builtins print'
   18: (    MARK
   19: U        SHORT_BINSTRING 'Hello World!'
   33: t        TUPLE      (MARK at 18)
   34: R    REDUCE
   35: .    STOP
highest protocol among opcodes = 2
Hello World!
```

## Sickle
[`sickle.pickle`](./sickle.pickle) is a pickle reverse engineering problem from SECCON CTF 2023 Quals that implements a flag checker. This pickle is unique because it was designed to include flow control, such as `jump` statements and `if` statements. It was defined as below:

```python
payload = b'<bytes>'

f = io.BytesIO(payload)
res = pickle.load(f)
```

The `f` variable used `seek` to jump ahead or behind in instructions based on how the pickle ran. Since this is not intended pickle behavior, the debugger won't work out-of-the-box with this functionality; source code adjustments are required.

## Snek
[`snek.pickle`](./snek.pickle) is part of a reverse engineering problem from LACTF 2023 where unloading the pickle created a Python code object that ran a snake game that had to be reversed. Obtaining the code object from the pickle bytes was essential to pulling out the real source code for the game.