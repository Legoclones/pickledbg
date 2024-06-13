#!/usr/bin/env python3

#######################################################################################
# 
# picklecomp - a simple Python pickle compiler
# 
# This script is meant to facilitate creating custom pickles by hand. The usage is 
# fairly simple, you insert the bytes into the `mypickle_arr` variable, then run the 
# script. It will print out the pickle as hex and as bytes, and optionally write it to 
# a file.
# 
# There are two main ways to create a pickle. You can either use the pickle opcode 
# constants and define custom bytes afterwards, or use the custom-defined opcode 
# functions. The latter is easier, but the former is more flexible.
# 
# Here's an example. Let's say you want to use the BININT2 opcode to load the number 
# 1337 onto the stack. The first way of doing it would be:
# 
#    mypickle_arr = [
#        BININT2, b'\x39\x05'
#    ]
# 
# The second way would be:
# 
#    mypickle_arr = [
#        binint2(1337)
#    ]
# 
#######################################################################################


from pickle import *
import struct

encoding = 'ASCII' # pickle.loads() default

def compile():
    global encoding
    encoding = 'ASCII' # change here if you want to use a different encoding

    mypickle_arr = [
        ### INSERT BYTES HERE ###
        
        ### END INSERT BYTES ###
    ]

    mypickle = b''.join(mypickle_arr)

    # print to console as hex
    print(mypickle.hex())

    # print to console as bytes
    print(mypickle)

    # uncomment below to write to file
    #with open('my.pickle','wb') as f:
    #    f.write(mypickle)



def _int(num : int|bool):
    if isinstance(num, bool):
        if num:
            return b'I01\n'
        else:
            return b'I00\n'
        
    else:
        return INT + str(num).encode(encoding) + b'\n'
    
def binint(num : int):
    return BININT + struct.pack('<i', num)

def binint1(num : int):
    return BININT1 + struct.pack('<B', num)

def binint2(num : int):
    return BININT2 + struct.pack('<H', num)

def long(num : int):
    return LONG + str(num).encode() + b'L\n'

def long1(num : int):
    if num == 0:
        return LONG1 + b'\x00'
    
    length = 1
    while True:
        try:
            int.to_bytes(num, length=length, byteorder='little', signed=True)
        except OverflowError:
            length += 1
        else:
            break

    return LONG1 + struct.pack('<B', length) + int.to_bytes(num, length=length, byteorder='little', signed=True)

def long4(num : int):
    if num == 0:
        return LONG4 + b'\x00'*4
    
    length = 1
    while True:
        try:
            int.to_bytes(num, length=length, byteorder='little', signed=True)
        except OverflowError:
            length += 1
        else:
            break
        
    return LONG4 + struct.pack('<i', length) + int.to_bytes(num, length=length, byteorder='little', signed=True)

def string(s : str):
    # note - ensure the encoding is correct, otherwise string may not be what you want
    return STRING + b'"' + s.encode(encoding) + b'"\n'

def binstring(s : str):
    # note - ensure the encoding is correct, otherwise string may not be what you want
    return BINSTRING + struct.pack('<i', len(s)) + s.encode(encoding)

def short_binstring(s : str):
    if len(s) > 0xff:
        raise ValueError('short_binstring() argument must be a string of length <= 255')
    
    # note - ensure the encoding is correct, otherwise string may not be what you want
    return SHORT_BINSTRING + int.to_bytes(len(s)) + s.encode(encoding)

def binbytes(b : bytes):
    return BINBYTES + struct.pack('<I', len(b)) + b

def short_binbytes(b : bytes):
    if len(b) > 0xff:
        raise ValueError('short_binbytes() argument must be a bytestring of length <= 255')
    
    return SHORT_BINBYTES + int.to_bytes(len(b)) + b

def binbytes8(b : bytes):
    return BINBYTES8 + struct.pack('<Q', len(b)) + b

def bytearray8(b : bytes|bytearray):
    return BYTEARRAY8 + struct.pack('<Q', len(b)) + b

def next_buffer():
    return NEXT_BUFFER

def readonly_buffer():
    return READONLY_BUFFER

if __name__ == "__main__":
    compile()