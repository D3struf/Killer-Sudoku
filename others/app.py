import pygame
import sys
from pygame.locals import *

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define constants
WIDTH = 500
HEIGHT = 400
CELL_SIZE = 100
GRID_SIZE = 4
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
BUTTON_COLOR = (50, 150, 50)
BUTTON_TEXT_COLOR = WHITE
MAX_CELLS_PER_CLICK = 4

def draw_grid(screen, selected_cells, cages):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if (i, j) in selected_cells:
                pygame.draw.rect(screen, BLUE, rect)
            for cage in cages:
                if (i, j) in cage:
                    pygame.draw.rect(screen, RED, rect)  # Draw cells within cages in red

def draw_button(screen, button_rect):
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Collect", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def getAvailableCoordinates(cages):
    all_coordinates = set((i, j) for i in range(4) for j in range(4))
    used_coordinates = set(coords for cage in cages for coords in cage)
    available_coordinates = all_coordinates - used_coordinates
    sorted_coordinates = sorted(list(available_coordinates))
    return sorted_coordinates

def draw_button(screen, x, y, width, height, text, selected=False):
    if selected:
        color = BLUE
    else:
        color = GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))  # Draw the button background
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Killer Sudoku")
    icon = pygame.image.load('./assets/Killer Sudoku Icon.png')
    pygame.display.set_icon(icon)

    selected_cells = set()
    cages = []

    button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)

    buttons = []
    number = 0
    for i in range(5):
        for j in range(2):
            number += 1
            x = j * 50
            y = i * 50
            buttons.append((x, y, 50, 50, str(number), False))
    
    while True:
        screen.fill(GRAY)
        draw_grid(screen, selected_cells, cages)
        draw_button(screen, button_rect)
        
        for button in buttons:
            draw_button(screen, *button)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                    print("Selected Cells:", selected_cells)
                    if len(selected_cells) < MAX_CELLS_PER_CLICK:
                        cages.append(selected_cells.copy())  # Append a copy of selected_cells to cages
                        print("Cages:", cages)
                    selected_cells.clear()  # Clear the set of selected cells
                else:
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    cell = (row, col)
                    if cell not in getAvailableCoordinates(cages):
                        # If the cell is within a cage, don't add it to selected_cells
                        continue
                    if len(selected_cells) < MAX_CELLS_PER_CLICK:  # Check if the limit is reached
                        if cell in selected_cells:
                            selected_cells.remove(cell)
                        else:
                            selected_cells.add(cell)

        pygame.display.flip()

if __name__ == "__main__":
    main()
