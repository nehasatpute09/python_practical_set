f = open("data.txt","r")
string = f.read()
print(string)
count = 0
for text in f:
    a = text.split(" ")
    length = len(a)
    print(length)
    print(a)
    count += length
print(count)
f.close()