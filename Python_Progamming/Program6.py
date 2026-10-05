a = 5
for i in range(a):
    for j in range(a-i-1):
        print(" ",end="")
    print(((2*i)+1) * '*')

