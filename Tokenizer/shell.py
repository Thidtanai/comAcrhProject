import riscToken

while True:
    text = input('command > ')
    result, error = riscToken.run('<stdin>', text)
    
    if error: print(error.as_string())
    else: print(result)