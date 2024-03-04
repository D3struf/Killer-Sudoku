# Killer Sudoku Problem
# Made by John Paul Monter

# matrix = ([1, 2, 3, 4],
#             [4, 3, 2, 1],
#             [3, 4, 1, 2],
#             [2, 1, 4, 3])
# Each row or col has a sum of 10 
# Each group has a sum
# If a group of 1 is the same as the number

def printMatrix(matrix):
    print("MATRIX: ")
    count = 0
    for i in range(len(matrix)):
        if i == 2:
            print('---------')
        for j in matrix[i]:
            count += 1
            if count == 3:
                print('|', end=' ')
            print(j, end=" ")
        count = 0
        print()

def getValue (matrix, x, y):
    for i in range(len(matrix)):
        if i == int(x):
            for j in range(len(matrix)):
                if j == int(y):
                    askUserValue = userValue()
                    matrix[i][j] = askUserValue
                    return askUserValue
                
def userValue():
    try:
        value = int(input("Please Enter Value: "))
        if (value > 4):
            print("Please Enter Number less than 4")
            return userValue()
        return value
    except ValueError:
        print("Please Enter a Number")
        return userValue()
                
def getCoords():
    coords = ''
    try:
        while len(coords) != 3:
            coords = input("Please Enter coordinates (Ex. x,y): ")
            x, y = coords.split(',')

            if coords[1] != ',' or (int(x) > 4 or int(y) > 4):
                print("Invalid Coordinates!! Try Again...")
                return getCoords()
        else: return x, y
    except ValueError:
        print("Invalid Coordinates!! Try Again...")
        return getCoords()

if __name__ == '__main__':
    # Initialize the 4x4 matrix
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    askAgain = 'y'
    
    while askAgain == 'y':
        printMatrix(matrix)
        
        x, y = getCoords();
        
        print("Value: ", getValue(matrix, x, y))
        printMatrix(matrix)
        
        askAgain = input("Would you like to enter another Value? (y or n): ")