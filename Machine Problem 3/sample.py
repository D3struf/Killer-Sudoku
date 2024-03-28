try:
    ask = int(input("Please Enter coordinates (Ex. x,y): "))
    if ask == '':
        print('error!!')
    print('Ask: ', ask)
except ValueError:
    print('Value Error!!')