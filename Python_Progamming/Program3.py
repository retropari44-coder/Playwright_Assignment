def find_max_diffeence(list_of_number):
    max=0
    length = len(list_of_number)-1
    for i in range(length):
        difference = abs(list_of_number[i]-list_of_number[i+1])
        if(difference>max):
            max = difference
    print(max)

list_of_number = [1,2,6,8,9]
find_max_diffeence(list_of_number=list_of_number)