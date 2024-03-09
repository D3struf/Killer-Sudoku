from itertools import combinations
import sys
import random

cages = []

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

def printMatrixWithCages(matrix, cages):
    def getCageId(coord, cages):
        for idx, (cage_coords, cageSum) in enumerate(cages):
            if coord in cage_coords:
                return cageSum
        return 0

    print("MATRIX:")
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

def fillInitialCells(matrix):
    # Randomly fill some cells with valid numbers
    for i in range(4):
        for j in range(4):
            if random.random() < 1:  # Adjust the probability as needed
                valid_numbers = getValidNumbers(matrix, i, j)
                if valid_numbers:
                    matrix[i][j] = random.choice(valid_numbers)

def getValidNumbers(matrix, row, col):
    # Get numbers that can be placed in a cell without violating Killer Sudoku rules
    valid_numbers = list(range(1, 5))

    # Check row and column constraints
    for i in range(4):
        if matrix[row][i] in valid_numbers:
            valid_numbers.remove(matrix[row][i])
        if matrix[i][col] in valid_numbers:
            valid_numbers.remove(matrix[i][col])

    # Check 2x2 subgrid constraints
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for i in range(start_row, start_row + 2):
        for j in range(start_col, start_col + 2):
            if matrix[i][j] in valid_numbers:
                valid_numbers.remove(matrix[i][j])

    # Shuffle the list of valid numbers
    random.shuffle(valid_numbers)

    return valid_numbers

def calculateScore(matrix, cages):
    score = 0
    for cage_coords, target_sum in cages:
        cage_sum = sum(matrix[i][j] for i, j in cage_coords)
        score += abs(cage_sum - target_sum)
    return score

def hillClimbing(matrix, cages):
    current_score = calculateScore(matrix, cages)

    while True:
        best_move_found = False
        for i in range(4):
            for j in range(4):
                # Create a copy of the matrix for modification
                temp_matrix = [row[:] for row in matrix]  # Slice copying for better performance
                valid_numbers = getValidNumbers(temp_matrix, i, j)
                for num in valid_numbers:
                    original_value = temp_matrix[i][j]
                    temp_matrix[i][j] = num
                    new_score = calculateScore(temp_matrix, cages)
                    if new_score < current_score:
                        current_score = new_score
                        best_move_found = True
                        matrix = temp_matrix.copy()  # Update original matrix only if improved
                    else:
                        temp_matrix[i][j] = original_value  # Undo move if it doesn't improve (not strictly necessary here)
        if not best_move_found:
            break

if __name__ == '__main__':
    matrix = initializeMatrix()
    askAgain = 'y'
    
    while True:
        printMatrixWithCages(matrix, cages)
        getCageInput()
        print("Cages: ", cages)
        if not getAvailableCoordinates():
            break
    
    fillInitialCells(matrix)
    print("Initial Matrix:")
    printMatrixWithCages(matrix, cages)

    hillClimbing(matrix, cages)

    print("\nFinal Matrix after Hill Climbing:")
    printMatrixWithCages(matrix, cages)
    print("Final Score:", calculateScore(matrix, cages))