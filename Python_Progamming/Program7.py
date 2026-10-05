a = int(input())
half = a//2
sum = 0
for i in range(1,half+1):
    if (a%i == 0):
        sum +=1
print('prime' if sum==1 else 'composite')
