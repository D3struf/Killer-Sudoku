# Killer Sudoku Problem
# Made by John Paul Monter

# matrix = ([1, 2, 3, 4],
#             [4, 3, 2, 1],
#             [3, 4, 1, 2],
#             [2, 1, 4, 3])
# Each row should have numbers 1 to 4 and does not have a duplicate.
# Each column should have numbers 1 to 4 and does not have a duplicate.
# Each row, col, and 2x2 subgrid should have a sum of 10.
# Each group has a sum entered by the user.
# If a group has only one cell then the sum and the number should be the same.
import sys
cages = []

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
        
def checkDuplicate(matrix, x, y, value, check):
    if check == 'row':
        return value in matrix[int(x)]
    elif check == 'col':
        return value in [matrix[i][int(y)] for i in range(4)]
    elif check == 'subgrid':
        subgrid_values = [matrix[i][j] for i in range(2 * (int(x) // 2), 2 * (int(x) // 2) + 2) for j in range(2 * (int(y) // 2), 2 * (int(y) // 2) + 2)]
        return value in subgrid_values

def getValue(matrix, x, y):
    try:
        askUserValue = userValue()
        if not checkDuplicate(matrix, x, y, askUserValue, 'row') and \
            not checkDuplicate(matrix, x, y, askUserValue, 'col') and \
            not checkDuplicate(matrix, x, y, askUserValue, 'subgrid'):
            matrix[int(x)][int(y)] = askUserValue
            return askUserValue
        else:
            print("Duplicate number found in row, column, or subgrid. Try again.")
            return getValue(matrix, x, y)
    except ValueError:
        print("Please Enter a Number")
        return getValue(matrix, x, y)

def userValue():
    try:
        value = int(promptAgain('userVal'))
        if (value > 4):
            print("Please Enter Number less than 4")
            return userValue()
        elif (value == 0):
            print("Please Enter a Number from 1 to 4")
            return userValue()
        return value
    except ValueError:
        print("Please Enter a Number")
        return userValue()

def getCoords():
    coords = ''
    try:
        while len(coords) != 3:
            coords = promptAgain('coords')
            x, y = coords.split(',')
            
            if coords[1] != ',' or (int(x) >= 4 or int(y) >= 4):
                print("Invalid Coordinates!! Try Again...")
                return getCoords()
            elif matrix[int(x)][int(y)] != 0:
                print("Cell already has a number. Try again.")
                return getCoords()
        else: return x, y
    except ValueError:
        print("Invalid Coordinates!! Try Again...")
        return getCoords()
    
def initializeMatrix():
    return [[0 for _ in range(4)] for _ in range(4)]

def promptAgain(prompt):
    try:
        if prompt == 'again':
            # Continue when Enter key is pressed
            ask = input("Would you like to enter another Value? (y or n): ") or 'y'
            if ask == 'y' or ask == 'n':
                return ask
            promptAgain('again')
        elif prompt == 'coords':
            ask = input("Please Enter coordinates (Ex. x,y): ")
            return ask
        elif prompt == 'userVal':
            ask = input("Please Enter Value: ")
            return ask
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
        
def getCageInput():
    availableCoords = getAvailableCoordinates()
    print("Available coordinates: ", availableCoords)
    print("FORMAT: (row, col)")
    print("NOTE: Just press Enter to close the cage input.")
    cage_sets = []
    while True:
        cages_input = cagePrompt(availableCoords)
        if cages_input == '':
            break
        cage_sets.append(cages_input)

    list_cage = []
    for cage_set in cage_sets:
        cells = tuple(map(int, cage_set.split(",")))
        list_cage.append(cells)

    cages.append(list_cage)
    print("Cages:", cages)
    
def cagePrompt(availableCoords):
    try:
        while True:
            coords = input('Enter Cage Cell: ')
            if not coords:
                return ''
            
            x, y = coords.split(',')
            if len(coords) != 3 and coords[1] != ',' or (int(x) >= 4 or int(y) >= 4):
                print("Invalid Coordinates!! Try Again...")
                return cagePrompt(availableCoords)
            elif (int(x),int(y)) not in availableCoords:
                print("Coordinate already been selected in other cage, Try Again!")
                return cagePrompt(availableCoords)
            else: 
                return coords
                
    except ValueError:
        print("Invalid Coordinates!! Try Again...")
        return cagePrompt(availableCoords)
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
        
def getAvailableCoordinates():
    all_coordinates = set((i, j) for i in range(4) for j in range(4))
    used_coordinates = set(cells for cage in cages for cells in cage)
    available_coordinates = all_coordinates - used_coordinates
    return available_coordinates

if __name__ == '__main__':
    matrix = initializeMatrix()
    askAgain = 'y'
    
    while True:
        getCageInput()
        if not getAvailableCoordinates():
            break
    
    # while askAgain == 'y':
    #     printMatrix(matrix)
        
    #     x, y = getCoords();
        
    #     print("Value: ", getValue(matrix, x, y))
    #     printMatrix(matrix)
        
    #     askAgain = promptAgain('again')