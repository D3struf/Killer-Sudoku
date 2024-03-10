# Killer Sudoku Problem
# Made by John Paul Monter

# Each row should have numbers 1 to 4 and does not have a duplicate.
# Each column should have numbers 1 to 4 and does not have a duplicate.
# Each row, col, and 2x2 subgrid should have a sum of 10.
# Each group has a sum entered by the user.
# If a group has only one cell then the sum and the number should be the same.
# In a cage no number must appear more than once

from itertools import combinations
from colorama import Fore, Back, Style
import sys
import random

# Sample input
# cages = [([(0, 0), (0, 1)], 6), 
#         ([(0, 2), (0, 3)], 4),
#         ([(1, 0), (2, 0), (2, 1)], 6),
#         ([(1, 1), (1, 2)], 3),
#         ([(1, 3), (2, 3)], 7),
#         ([(3, 0), (3, 1)], 7),
#         ([(2, 2), (3, 2), (3, 3)], 7)]

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

def generateInitialState(matrix):
    while True:
        for cage_coords, target_sum in cages:
            random_numbers = generateRandomNumbers(target_sum, len(cage_coords))
            for i, j in cage_coords:
                matrix[i][j] = random_numbers.pop()

        if checkNumbersFrequency(matrix):
            break
        else:
            matrix = [[0] * 4 for _ in range(4)]

    return matrix

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

def checkNumbersFrequency(matrix):
    count = [0] * 5  # Initialize count array to store frequency of numbers 1 to 4
    for row in matrix:
        for num in row:
            count[num] += 1
    return all(count[i] == 4 for i in range(1, 5))  # Check if each number appears exactly four times

def checkDuplicates(matrix):
    row_duplicates = checkRowDuplicates(matrix)
    col_duplicates = checkColumnDuplicates(matrix)
    subgrid_duplicates = checkSubgridDuplicates(matrix)

    total_duplicates = row_duplicates + col_duplicates + subgrid_duplicates
    return total_duplicates

def checkRowDuplicates(matrix):
    duplicates_count = 0

    for row in matrix:
        unique_numbers = set()
        duplicate_numbers = set()

        for num in row:
            if num in unique_numbers:
                duplicate_numbers.add(num)
            else:
                unique_numbers.add(num)

        duplicates_count += len(duplicate_numbers)

    return duplicates_count

def checkColumnDuplicates(matrix):
    duplicates_count = 0

    for col in range(len(matrix[0])):
        unique_numbers = set()
        duplicate_numbers = set()

        for row in matrix:
            num = row[col]
            if num in unique_numbers:
                duplicate_numbers.add(num)
            else:
                unique_numbers.add(num)

        duplicates_count += len(duplicate_numbers)

    return duplicates_count

def checkSubgridDuplicates(matrix):
    duplicates_count = 0
    subgrid_size = 2

    for start_row in range(0, len(matrix), subgrid_size):
        for start_col in range(0, len(matrix[0]), subgrid_size):
            unique_numbers = set()
            duplicate_numbers = set()

            for row in range(start_row, start_row + subgrid_size):
                for col in range(start_col, start_col + subgrid_size):
                    num = matrix[row][col]
                    if num in unique_numbers:
                        duplicate_numbers.add(num)
                    else:
                        unique_numbers.add(num)

            duplicates_count += len(duplicate_numbers)

    return duplicates_count

def hillClimbing(matrix):
    while True:
        current_duplicates = checkDuplicates(matrix)

        if current_duplicates == 0:
            indicator(Fore.WHITE, Back.YELLOW, "           SOLUTION FOUND!!!           ")
            print()
            print()
            indicator(Fore.WHITE, Back.GREEN, "             KILLER SUDOKU             ") 
            print()
            printMatrixWithCages(matrix, cages)
            break

        # Perform hill climbing by swapping numbers within the cages
        for cage_coords, _ in cages:
            i, j = random.choice(cage_coords)
            swap_i, swap_j = random.choice(cage_coords)
            matrix[i][j], matrix[swap_i][swap_j] = matrix[swap_i][swap_j], matrix[i][j]

        new_duplicates = checkDuplicates(matrix)

        if new_duplicates >= current_duplicates:
            # If the move doesn't improve the situation, undo the swap
            for cage_coords, _ in cages:
                i, j = random.choice(cage_coords)
                swap_i, swap_j = random.choice(cage_coords)
                matrix[i][j], matrix[swap_i][swap_j] = matrix[swap_i][swap_j], matrix[i][j]

def indicator(foreground, background, string):
    print(f"{Style.BRIGHT}{background}{Fore.WHITE}{foreground}{string}{Style.RESET_ALL}", end='')

def printCredentials():
    indicator(Fore.WHITE, Back.BLUE, "   NAME   ")
    indicator(Fore.BLUE, Back.WHITE, " John Paul S. Monter                          ")
    print()
    indicator(Fore.WHITE, Back.LIGHTRED_EX, " SECTION  ")
    indicator(Fore.LIGHTRED_EX, Back.WHITE, " BSCS - 3B                                    ")
    print()
    indicator(Fore.WHITE, Back.LIGHTGREEN_EX , "  COURSE  ")
    indicator(Fore.LIGHTGREEN_EX , Back.WHITE, " Artificial Intelligence                      ")
    print()
    indicator(Fore.WHITE, Back.LIGHTBLUE_EX, "  GITHUB  ")
    indicator(Fore.LIGHTBLUE_EX, Back.WHITE, " https://github.com/D3struf/Killer-Sudoku.git ")


if __name__ == '__main__':
    matrix = initializeMatrix()
    askAgain = 'y'
    
    while True:
        printMatrixWithCages(matrix, cages)
        getCageInput()
        if not getAvailableCoordinates():
            break
    
    indicator(Fore.WHITE, Back.GREEN, "             KILLER SUDOKU             ") 
    print()
    printMatrixWithCages(matrix, cages)
    
    matrix = generateInitialState(matrix)
    indicator(Fore.WHITE, Back.GREEN, " AI finding solution... It will take a while...")
    print()
    hillClimbing(matrix)
    
    result = checkDuplicates(matrix)
    print(f"Number of pairs of duplicates: {result}")
    
    printCredentials()