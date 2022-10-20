from cgitb import text
import riscToken
import os

fileName = './Tokenizer/testfile.txt'

def readFile(fileDir):
    result_arr = []

    # Using readlines()
    file1 = open(fileDir, 'r')
    Lines = file1.readlines()
    
    # Strips the newline character
    
    index = 0
    for line in Lines:
        #arr.append(line.strip())
        text = line.strip()
    
        result, error = riscToken.run('<stdin>', text, index)
        index += 1
    
        token_result = []
        for i in range(len(result)):
            token_result.append(result[i])
    
        if error: print(error.as_string())
        else: result_arr.append(token_result)

    return result_arr

print(readFile(fileName))
    

