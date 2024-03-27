# Pygame integration for Killer Sudoku

import pygame
import sys

# Color Pallete 
WHITE = (255, 255, 255)
LIGHTGRAY = (206, 212, 218)
BLACK = (0, 0, 0)
SELECTED_COLOR = (100, 100, 255)

# Sizes
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = 600 // GRID_SIZE

# Matrix
def initializeMatrix():
    return [[0 for _ in range(4)] for _ in range(4)]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Killer Sudoku")
icon = pygame.image.load('./assets/Killer Sudoku Icon.png')
pygame.display.set_icon(icon)

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        # Draw vertical lines
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        # Draw horizontal lines
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

# Function to draw numbers in cells
def draw_numbers(board):
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j]["value"] != 0:
                number = font.render(str(board[i][j]["value"]), True, BLACK)
                screen.blit(number, (j * CELL_SIZE + CELL_SIZE // 2 - 10, i * CELL_SIZE + CELL_SIZE // 2 - 15))

# Function to highlight selected cells
def draw_selected_cells(selected_cells):
    for cell in selected_cells:
        pygame.draw.rect(screen, SELECTED_COLOR, (cell["col"] * CELL_SIZE, cell["row"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

if __name__ == "__main__":
    killer_board = [
        [{"value": 0, "group": None} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
    ]
    
    running = True
    selected_cells = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_col = mouse_x // CELL_SIZE
                selected_row = mouse_y // CELL_SIZE
                if selected_row < GRID_SIZE and selected_col < GRID_SIZE:
                    selected_cells.append({"row": selected_row, "col": selected_col})
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and selected_cells:
                    sum_value = int(event.unicode)
                    for cell in selected_cells:
                        killer_board[cell["row"]][cell["col"]]["value"] = sum_value
                        killer_board[cell["row"]][cell["col"]]["group"] = selected_cells.copy()
                    selected_cells = []

        # Draw the grid
        screen.fill(WHITE)
        draw_grid()

        # Highlight selected cells
        draw_selected_cells(selected_cells)

        # Draw numbers in cells
        draw_numbers(killer_board)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()