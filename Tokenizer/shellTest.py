import riscToken

index = 0

while True:
    text = input('command > ')
    result, error = riscToken.run('<stdin>', text, index)
    index += 1

    token_result = []
    for i in range(len(result)):
        token_result.append(result[i])

    if error: print(error.as_string())
    else: print(token_result)

"""
    How to get value.

        -result[0-6].get()
        -result[0-6].get_value(), result[0-6].get_type()
        ex.
            for i in range(len(result)):
                print(result[i].get())
"""