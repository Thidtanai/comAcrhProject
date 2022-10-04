
def tokenizer(src) :
    result = src.split()
    print(result)


## test 
f = open("inputTest.txt", "r")
code = f.read()
print(f.read())
tokenizer(code)