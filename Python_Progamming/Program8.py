word1 = input()
reverse_word =''
length = len(word1)
while(length!=0):
    reverse_word += word1[length-1]
    length-=1
print(reverse_word)
