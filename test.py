from itertools import permutations
import random
cages = []
total_attemp = 0

def generate_board():
    return [[0 for _ in range(4)] for _ in range(4)]

def print_boxes_layout(board):
    for i in range(4):
        print(f" [{i}]", end="")
    print()

    for i in range(4):
        for j in range(4):
            print("+---", end="")
        print("+")

        for j in range(4):
            if board[i][j] == 0:
                print("|   ", end="")
            else:
                print(f"| {board[i][j]} ", end="")
        print(f"| [{i}]")

    for j in range(4):
        print("+---", end="")
    print("+")

texts = [
    "---",
    "Machine Problem 2",
    "4x4 Killer Sudoku using Hill-climb Algorithm",
    "by: Andrew Oloroso",
    "Github Repo: https://github.com/ChugxScript/Killer-Sodoku-using-Local-Search"
]

def get_cage_input(board):
    available_coordinates = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    while True:
        print("Available coordinates:", available_coordinates)
        cage_input = input("Enter cage cells (row,col) separated by space (e.g., 1,1 1,2 2,1 2,2): ")
        cells = [tuple(map(int, cell.split(','))) for cell in cage_input.split()]
        valid_cells = True
        for cell in cells:
            if cell not in available_coordinates:
                print("Invalid cell coordinates or cell already assigned to another cage. Please choose from available coordinates.")
                valid_cells = False
                break
        if valid_cells:
            return cells

def get_cage_sum(board, cells):
    while True:
        print(f"Available cage sum is from [{len(cells)}] to [{len(cells) * 4}]")
        cage_sum = input("Enter the sum for this cage: ")
        if not cage_sum.isdigit():
            print("\n[! INVALID INPUT !]")
            print("Sum must be a positive integer.\n")
        else:
            if (int(cage_sum) > 0 and int(cage_sum) >= len(cells) and int(cage_sum) <= (len(cells) * 4)):
                return int(cage_sum)
            else:
                print("\n[! INVALID INPUT !]")
                print("Sum must be a align with the length of the cage.")
                print(f"Available cage sum is from [{len(cells)}] to [{len(cells) * 4}]\n")
        print("\n\nUpdated board:")
        print_boxes_layout(board)

def generate_cell_num(board, cells, cage_sum, call):
    global cages
    numbers = [1, 2, 3, 4]

    if call == 'main':
        for perm in permutations(numbers, len(cells)):
            if sum(perm) == cage_sum:
                for idx, cell in enumerate(cells):
                    row, col = cell
                    board[row][col] = perm[idx]
                return True
        return False

def solve(board):
    global cages

    # Calculate initial errors
    row_col_errors, duplicates = check_errors(board)
    initial_errors = sum_errors(row_col_errors, duplicates)

    attempt = 0
    modify = 0
    cage_idx = [0] * len(cages)
    modify_cage = [0] * len(cages)
    check_perm(modify_cage)

    while True:
        # Find the cage with the most errors
        max_errors_cage_index = get_max_errors_cage(board, cages, row_col_errors, duplicates, modify)

        # Generate new state by switching numbers in the cage
        new_board = switch_numbers_in_cage(board, cages[max_errors_cage_index], cage_idx, max_errors_cage_index)

        # Calculate errors in the new state
        new_row_col_errors, new_duplicates = check_errors(new_board)
        new_errors = sum_errors(new_row_col_errors, new_duplicates)

        # If the new state has fewer errors, update the board
        if new_errors < initial_errors:
            board = new_board
            row_col_errors = new_row_col_errors
            duplicates = new_duplicates
            initial_errors = new_errors

            if not row_col_errors and not duplicates:
                return board
            attempt = 0

        else:
            if attempt > (sum(modify_cage) - modify_cage[modify]):
                # check if no improvement then modify cell to avoid getting stuck
                new_board = switch_numbers_in_cage(board, cages[modify], cage_idx, modify)
                new_row_col_errors, new_duplicates = check_errors(new_board)
                
                if not new_row_col_errors and not new_duplicates:
                    board = new_board
                    return board
                
                if modify_cage[modify] == cage_idx[modify]:
                    modify += 1
                    if modify >= len(cages):
                        return board
                
                attempt = 0
                    
            else:
                attempt += 1

def get_max_errors_cage(board, cages, row_col_errors, duplicates, modify):
    max_errors = -1
    max_errors_cage_index = -1

    for i, (cage_sum, cells) in enumerate(cages):
        if i != modify:
            cage_errors = count_cage_errors(cells, row_col_errors, duplicates)
            if cage_errors > max_errors:
                max_errors = cage_errors
                max_errors_cage_index = i

    return max_errors_cage_index

def count_cage_errors(cells, row_col_errors, duplicates):
    cage_errors = 0
    for coord in cells:
        if coord in row_col_errors.values():
            cage_errors += 1
    for coord_list in duplicates.values():
        for coord in coord_list:
            if coord in cells:
                cage_errors += 1
    return cage_errors

def switch_numbers_in_cage(board, cage, cage_idx, max_errors_cage_index):
    new_board = [row[:] for row in board]  # Create a copy of the board
    cage_sum, cells = cage
    numbers = [1, 2, 3, 4]
    perm_limit = 0
    perm_idx = 0

    for perm in permutations(numbers, len(cells)):
        if sum(perm) == cage_sum:
            perm_limit += 1

    if perm_limit > cage_idx[max_errors_cage_index]:
        cage_idx[max_errors_cage_index] += 1
    else:
        cage_idx[max_errors_cage_index] = 1

    for perm in permutations(numbers, len(cells)):
        if sum(perm) == cage_sum and perm_idx < cage_idx[max_errors_cage_index]:
            for idx, (row, col) in enumerate(cells):
                new_board[row][col] = perm[idx]
            perm_idx += 1

    return new_board

def check_perm(modify_cage):
    global cages
    numbers = [1, 2, 3, 4]

    for i, (cage_sum, cells) in enumerate(cages):
        for perm in permutations(numbers, len(cells)):
            if sum(perm) == cage_sum:
                modify_cage[i] += 1

def check_errors(board):
    n = len(board)
    row_errors = [0] * n
    col_errors = [0] * n
    row_col_errors = {}
    duplicates = {}

    # get coordinates of errors in each row and column
    for i in range(n):
        row_nums = set()
        col_nums = set()
        row_err = {}
        col_err = {}
        for j in range(n):
            if board[i][j] == 0:
                row_errors[i] += 1
                if board[i][j] in row_col_errors:
                    row_col_errors[board[i][j]].append((i, j))
                else:
                    row_col_errors[board[i][j]] = [(i, j), row_err[board[i][j]]]
            elif board[i][j] in row_nums:
                row_errors[i] += 1
                if board[i][j] in row_col_errors:
                    row_col_errors[board[i][j]].append((i, j))
                else:
                    row_col_errors[board[i][j]] = [(i, j), row_err[board[i][j]]]
            else:
                row_nums.add(board[i][j])
                row_err[board[i][j]] = (i, j)
            
            if board[j][i] == 0:
                col_errors[i] += 1
                if board[j][i] in row_col_errors:
                    row_col_errors[board[j][i]].append((j, i))
                else:
                    row_col_errors[board[j][i]] = [(j, i), col_err[board[j][i]]]
            elif board[j][i] in col_nums:
                col_errors[i] += 1
                if board[j][i] in row_col_errors:
                    row_col_errors[board[j][i]].append((j, i))
                else:
                    row_col_errors[board[j][i]] = [(j, i), col_err[board[j][i]]]
            else:
                col_nums.add(board[j][i])
                col_err[board[j][i]] = (j, i)
    
    # get coordinates of errors in 2x2 subgrid
    for i in range(0, len(board), 2):
        for j in range(0, len(board[0]), 2):
            coord = {}
            subgrid_values = set()
            for x in range(i, i + 2):
                for y in range(j, j + 2):
                    cell_value = board[x][y]
                    if cell_value != 0:
                        if cell_value in subgrid_values:
                            if cell_value in duplicates:
                                duplicates[cell_value].append((x, y))
                            else:
                                duplicates[cell_value] = [(x, y), coord[cell_value]]
                        else:
                            coord[cell_value] = (x, y)
                            subgrid_values.add(cell_value)
    
    return row_col_errors, duplicates

def sum_errors(row_col_errors, duplicates):
    # Calculate total errors from row_col_errors and duplicates
    return sum(len(coords) for coords in row_col_errors.values()) + sum(len(coords) for coords in duplicates.values())

def main():
    board = generate_board()
    print("Welcome to 4x4 Killer Sudoku!")
    print("Please enter the cages:")
    print_boxes_layout(board)

    global cages
    while any(0 in row for row in board):
        print(f"\nCage {len(cages) + 1}:")
        cells = get_cage_input(board)
        cage_sum = get_cage_sum(board, cells)
        if generate_cell_num(board, cells, cage_sum, 'main'):
            cages.append((cage_sum, cells))
        else:
            print("\n[! INVALID CAGE !]\n")
        
        print("\n\nUpdated board:")
        print_boxes_layout(board)

    hill_climb_board = solve(board)
    row_col_errors, duplicates = check_errors(hill_climb_board)

    # Check if there are no errors 
    if not row_col_errors and not duplicates:
        print("\n>>>Solution found:")
        print_boxes_layout(hill_climb_board)
    else:
        print("\n>>>No solution found.")
        print("This is the last attempt of the hill-climb algorithm")
        print_boxes_layout(hill_climb_board)

    for text in texts:
        print(text)

if __name__ == "__main__":
    main()