from riscToken import *

while True:
    text = input('command > ')
    result, error = basic.run('<stdin>', text)
    
    if error: print(error.as_string())
    else: print(resutl)