import riscToken

index = 0

while True:
    text = input('command > ')
    result, error = riscToken.run('<stdin>', text, index)
    index += 1
    
    if error: print(error.as_string())
    else: print(result)