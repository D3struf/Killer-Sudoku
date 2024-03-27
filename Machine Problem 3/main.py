import sys
from itertools import combinations
import random

cages = []

# cages = [([(0, 0), (0, 1)], 7), 
#         ([(0, 3), (1, 3)], 4),
#         ([(2, 1), (2, 2)], 5),
#         ([(1, 0), (2, 0), (3, 0)], 7),
#         ([(0, 2), (1, 1), (1, 2)], 7),
#         ([(2, 3), (3, 1), (3, 2), (3, 3)], 10)]

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
        elif prompt == 'cageSum':
            ask = int(input("Please Enter Cage Sum: "))
            return ask
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()

def getCageInput():
    availableCoords = getAvailableCoordinates()
    print("FORMAT: (row, col)")
    print("Available coordinates: ", availableCoords)
    print("NOTE: Just press Enter to close the cage prompt.")
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

    sumCage = getCageSum(len(list_cage))
    cages.append((list_cage, sumCage))

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
            elif (int(x), int(y)) not in availableCoords:
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
    used_coordinates = set(coords for cage, _ in cages for coords in cage)
    available_coordinates = all_coordinates - used_coordinates
    sorted_coordinates = sorted(list(available_coordinates))
    return sorted_coordinates

def getPossibleSums(cellCount):
    numbers = [1, 2, 3, 4]
    all_combinations = list(combinations(numbers, cellCount))
    possible_sums = set()

    for combination in all_combinations:
        possible_sums.add(sum(combination))

    return sorted(list(possible_sums))

def getCageSum(cellCount):
    availableSums = getPossibleSums(cellCount)
    print(" Available Cage Sum: ", availableSums)

    while True:
        askUserCageSum = promptAgain("cageSum")
        if askUserCageSum in availableSums:
            print(" Sum: ", askUserCageSum)
            return askUserCageSum
        else:
            print(" Invalid sum for cage, Try again...")

def generateNumber():
    for cage_coords, target_sum in cages:
            random_numbers = generateRandomNumbers(target_sum, len(cage_coords))
            for i, j in cage_coords:
                matrix[i][j] = random_numbers.pop()

def generateRandomNumbers(target_sum, num_elements):
    while True:
        # Generate a list of random numbers that sum up to the target sum
        random_numbers = [random.randint(1, 4) for _ in range(num_elements - 1)]
        target = target_sum - sum(random_numbers)
        # The target should still satisfy the constraints of the sudoku
        unique_numbers = set(random_numbers + [target])
        if target > 0 and target <= 4 and len(unique_numbers) == num_elements:
            break

    random_numbers.append(target)
    random.shuffle(random_numbers)
    return random_numbers

def printMatrix(matrix):
    def getCageId(coord, cages):
        for idx, (cage_coords, cageSum) in enumerate(cages):
            if coord in cage_coords:
                return cageSum
        return 0

    print("    0       1       2       3")
    print('---------------------------------')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print('|', end=' ')
            cell_value = matrix[i][j]
            cage_id = getCageId((i, j), cages)
            print(f'{cell_value} ({cage_id})', end=' ')
        print('|', end='   ')
        print(i)
        print('---------------------------------')


def solveSudoku(matrix):
    empty_cell = findEmptyCell(matrix)
    if not empty_cell:
        return True  # Puzzle solved successfully
    row, col = empty_cell

    for num in range(1, 5):  # Try numbers 1 to 4
        if isValidMove(matrix, row, col, num):
            matrix[row][col] = num
            if solveSudoku(matrix):
                return True
            matrix[row][col] = 0  # Backtrack if the current assignment does not lead to a solution
    return False

def findEmptyCell(matrix):
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                return (i, j)  # Return the coordinates of the first empty cell
    return None

def isValidMove(matrix, row, col, num):
    return not usedInRow(matrix, row, num) and \
            not usedInCol(matrix, col, num) and \
            not usedInBox(matrix, row - row % 2, col - col % 2, num) and \
            not violatesCageSum(matrix, row, col, num)

def usedInRow(matrix, row, num):
    return num in matrix[row] 

def usedInCol(matrix, col, num):
    return any(row[col] == num for row in matrix)

def usedInBox(matrix, startRow, startCol, num):
    for i in range(2):
        for j in range(2):
            if matrix[i + startRow][j + startCol] == num:
                return True
    return False

def violatesCageSum(matrix, row, col, num):
    for cage_coords, target_sum in cages:
        if (row, col) in cage_coords:
            current_sum = sum(matrix[i][j] for i, j in cage_coords) + num
            if current_sum > target_sum:
                return True
    return False

if __name__ == '__main__':
    matrix = initializeMatrix()
    askAgain = 'y'
    while True:
        getCageInput()
        print("Cages: ", cages)
        if not getAvailableCoordinates():
            break
        
    solveSudoku(matrix)
    printMatrix(matrix)
