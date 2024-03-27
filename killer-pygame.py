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
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 50
GRID_SIZE = 10
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30

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
    pygame.display.set_caption("Grid Buttons")
    
    buttons = []
    
    number = 0
    for i in range(5):
        for j in range(2):
            number += 1
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            buttons.append((x, y, CELL_SIZE, CELL_SIZE, str(number), False))

    while True:
        screen.fill(WHITE)
        
        for button in buttons:
            draw_button(screen, *button)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    bx, by, bw, bh, _, selected = button
                    if bx <= x < bx + bw and by <= y < by + bh:
                        # Toggle the selected state of the clicked button
                        button[5] = not selected
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
