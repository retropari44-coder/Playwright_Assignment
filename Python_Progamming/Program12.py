number = [19,12,23,8,10]
# number.sort()
# print(number)
# print(number.sort(reverse=True))   
# print(number)
j = len(number)
min = []
while(j!=0):
    min_number = number[0]
    for i in number:
        if i < min_number:
            min_number =  i
    min.append(min_number)
    number.remove(min_number)
    j=j-1
print("Min ordered list:",min)

number = [19,12,23,8,10]
max = []
j = len(number)
while(j!=0):
    max_number = number[0]
    for i in number:
        if i > max_number:
            max_number =  i
    max.append(max_number)
    number.remove(max_number)
    j=j-1
print("Max ordered list:", max)

