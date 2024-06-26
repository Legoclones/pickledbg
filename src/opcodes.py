MARK           = b'('
STOP           = b'.'
POP            = b'0'
POP_MARK       = b'1'
DUP            = b'2'
FLOAT          = b'F'
INT            = b'I'
BININT         = b'J'
BININT1        = b'K'
LONG           = b'L'
BININT2        = b'M'
NONE           = b'N'
PERSID         = b'P'
BINPERSID      = b'Q'
REDUCE         = b'R'
STRING         = b'S'
BINSTRING      = b'T'
SHORT_BINSTRING= b'U'
UNICODE        = b'V'
BINUNICODE     = b'X'
APPEND         = b'a'
BUILD          = b'b'
GLOBAL         = b'c'
DICT           = b'd'
EMPTY_DICT     = b'}'
APPENDS        = b'e'
GET            = b'g'
BINGET         = b'h'
INST           = b'i'
LONG_BINGET    = b'j'
LIST           = b'l'
EMPTY_LIST     = b']'
OBJ            = b'o'
PUT            = b'p'
BINPUT         = b'q'
LONG_BINPUT    = b'r'
SETITEM        = b's'
TUPLE          = b't'
EMPTY_TUPLE    = b')'
SETITEMS       = b'u'
BINFLOAT       = b'G'
TRUE           = b'I01\n'
FALSE          = b'I00\n'
PROTO          = b'\x80'
NEWOBJ         = b'\x81'
EXT1           = b'\x82'
EXT2           = b'\x83'
EXT4           = b'\x84'
TUPLE1         = b'\x85'
TUPLE2         = b'\x86'
TUPLE3         = b'\x87'
NEWTRUE        = b'\x88'
NEWFALSE       = b'\x89'
LONG1          = b'\x8a'
LONG4          = b'\x8b'
BINBYTES       = b'B'
SHORT_BINBYTES = b'C'
SHORT_BINUNICODE = b'\x8c'
BINUNICODE8      = b'\x8d'
BINBYTES8        = b'\x8e'
EMPTY_SET        = b'\x8f'
ADDITEMS         = b'\x90'
FROZENSET        = b'\x91'
NEWOBJ_EX        = b'\x92'
STACK_GLOBAL     = b'\x93'
MEMOIZE          = b'\x94'
FRAME            = b'\x95'
BYTEARRAY8       = b'\x96'
NEXT_BUFFER      = b'\x97'
READONLY_BUFFER  = b'\x98'