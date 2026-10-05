def list_compare_values(list_of_number):
    new_list=[]
    for i in range(len(list_of_number[0])):
        if (list_of_number[0][i]  == list_of_number[1][i]):
            new_list.append(list_of_number[0][i])
    print(new_list)

list_of_number1 = [1,2,6,8,9]
list_of_number2 = [2,2,6,7,8]
list_compare_values(list_of_number=[list_of_number1,list_of_number2])