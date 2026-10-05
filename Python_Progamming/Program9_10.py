word = input()
dict = {}
for i in word:
    if i in dict:
        dict[i]+=1
    else:
        dict[i]=1
print(dict)
for i in dict.keys():
    if dict[i] == 1:
        print(i,end='')