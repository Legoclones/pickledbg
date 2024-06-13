###########
# 
# A simple tool to compare the output of different pickle implementations
# 
###########

# imports
from pickle import _Unpickler
import _pickle
from io import BytesIO
from pickletools import dis


# edit here
payload = b'].'
encoding = 'utf-8'


# pickle
print('pickle:       ',end='')
try:
    print(_Unpickler(BytesIO(payload),encoding=encoding).load())
except Exception as e:
    print('FAILURE',e)
    

# _pickle.c
print('_pickle.c:    ',end='')
try:
    print(_pickle.loads(payload,encoding=encoding))
except Exception as e:
    print('FAILURE',e)
    

# pickletools
print('pickletools:  ')
try:
    dis(payload)
except Exception as e:
    print('pickletools failed',e)