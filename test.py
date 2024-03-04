import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INNER_BORDER_COLOR = (100, 100, 255)
OUTER_BORDER_COLOR = (0, 0, 0)

# Initialize the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Killer Sudoku Grid")

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

# Function to draw inner borders for selected groups
def draw_inner_borders(selected_groups):
    for group in selected_groups:
        for cell in group:
            pygame.draw.rect(screen, INNER_BORDER_COLOR, (cell["col"] * CELL_SIZE, cell["row"] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

# Function to draw outer borders for the entire grid
def draw_outer_borders():
    pygame.draw.rect(screen, OUTER_BORDER_COLOR, (0, 0, WIDTH, HEIGHT), 4)

# Function to get user input for the sum
def get_user_input():
    input_box = pygame.Rect(150, 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return int(text) if text.isdigit() else None
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    color = color_active

        screen.fill(WHITE)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

# Function to save the Sudoku board to a JSON file
def save_board(board):
    with open("killer_sudoku_board.json", "w") as file:
        json.dump(board, file)

# Function to load the Sudoku board from a JSON file
def load_board():
    try:
        with open("killer_sudoku_board.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# Main game loop
def main():
    killer_board = load_board()
    if killer_board is None:
        killer_board = [
            [{"value": 0, "group": None} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
        ]

    assigned_groups = []
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
                    if all(cell not in assigned_groups for cell in [{"row": selected_row, "col": selected_col}] + selected_cells):
                        selected_cells.append({"row": selected_row, "col": selected_col})
            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:  # Left mouse button is pressed
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_col = mouse_x // CELL_SIZE
                current_row = mouse_y // CELL_SIZE
                if current_row < GRID_SIZE and current_col < GRID_SIZE:
                    if not any(cell == {"row": current_row, "col": current_col} for cell in assigned_groups + selected_cells):
                        selected_cells.append({"row": current_row, "col": current_col})
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and selected_cells:
                    sum_value = int(event.unicode)
                    for cell in selected_cells:
                        killer_board[cell["row"]][cell["col"]]["value"] = sum_value
                        killer_board[cell["row"]][cell["col"]]["group"] = selected_cells.copy()
                    assigned_groups.append(selected_cells)
                    selected_cells = []
                elif event.key == pygame.K_SPACE and selected_cells:
                    # Prompt the user for the sum
                    user_sum = get_user_input()
                    if user_sum is not None:
                        for cell in selected_cells:
                            killer_board[cell["row"]][cell["col"]]["value"] = user_sum
                            killer_board[cell["row"]][cell["col"]]["group"] = selected_cells.copy()
                        assigned_groups.append(selected_cells)
                        selected_cells = []
                elif event.key == pygame.K_s:
                    # Save the current state of the board
                    save_board(killer_board)

        # Draw the grid
        screen.fill(WHITE)
        draw_outer_borders()
        draw_grid()

        # Draw inner borders for selected groups
        draw_inner_borders(assigned_groups)

        # Draw numbers in cells
        draw_numbers(killer_board)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
