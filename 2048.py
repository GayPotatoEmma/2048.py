import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (187, 173, 160)

# Game settings
GRID_SIZE = 4
TILE_SIZE = 100
GRID_MARGIN = 10

# Tile colors
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (238, 228, 218),
    8192: (242, 177, 121),
    16384: (245, 149, 99),
    32768: (246, 124, 95),
    65536: (246, 94, 59),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(((TILE_SIZE + GRID_MARGIN) * GRID_SIZE + GRID_MARGIN,
                                 (TILE_SIZE + GRID_MARGIN) * GRID_SIZE + GRID_MARGIN))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)


# Game Logic Functions
def initialize_game():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid


def add_random_tile(grid):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 2 if random.random() < 0.9 else 4


def move_and_merge(grid, direction):
    moved = False
    if direction == "up":
        for col in range(GRID_SIZE):
            merged_col = move_and_merge_row_or_col([grid[row][col] for row in range(GRID_SIZE)])
            for row in range(GRID_SIZE):
                if grid[row][col] != merged_col[row]:
                    moved = True
                    grid[row][col] = merged_col[row]
    elif direction == "down":
        for col in range(GRID_SIZE):
            merged_col = move_and_merge_row_or_col([grid[row][col] for row in reversed(range(GRID_SIZE))])
            for row in range(GRID_SIZE - 1, -1, -1):
                if grid[row][col] != merged_col[GRID_SIZE - 1 - row]:
                    moved = True
                    grid[row][col] = merged_col[GRID_SIZE - 1 - row]
    elif direction == "left":
        for row in range(GRID_SIZE):
            merged_row = move_and_merge_row_or_col(grid[row])
            for col in range(GRID_SIZE):
                if grid[row][col] != merged_row[col]:
                    moved = True
                    grid[row][col] = merged_row[col]
    elif direction == "right":
        for row in range(GRID_SIZE):
            merged_row = move_and_merge_row_or_col(grid[row][::-1])
            for col in range(GRID_SIZE - 1, -1, -1):
                if grid[row][col] != merged_row[GRID_SIZE - 1 - col]:
                    moved = True
                    grid[row][col] = merged_row[GRID_SIZE - 1 - col]
    return moved


def move_and_merge_row_or_col(row_or_col):
    new_row_or_col = [x for x in row_or_col if x != 0]
    i = 0
    while i < len(new_row_or_col) - 1:
        if new_row_or_col[i] == new_row_or_col[i + 1]:
            new_row_or_col[i] *= 2
            del new_row_or_col[i + 1]
        i += 1
    new_row_or_col += [0] * (GRID_SIZE - len(new_row_or_col))
    return new_row_or_col


def move_up(grid):
    return move_and_merge(grid, "up")


def move_down(grid):
    return move_and_merge(grid, "down")


def move_left(grid):
    return move_and_merge(grid, "left")


def move_right(grid):
    return move_and_merge(grid, "right")


def game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True


# Drawing Functions
def draw_grid(grid):
    screen.fill(BACKGROUND)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = TILE_COLORS[value]
            pygame.draw.rect(screen,
                             color,
                             [(GRID_MARGIN + TILE_SIZE) * col + GRID_MARGIN,
                              (GRID_MARGIN + TILE_SIZE) * row + GRID_MARGIN,
                              TILE_SIZE,
                              TILE_SIZE])
            if value != 0:
                text = font.render(str(value), True, WHITE)
                text_rect = text.get_rect(center=((GRID_MARGIN + TILE_SIZE) * col + GRID_MARGIN + TILE_SIZE // 2,
                                                  (GRID_MARGIN + TILE_SIZE) * row + GRID_MARGIN + TILE_SIZE // 2))
                screen.blit(text, text_rect)


def draw_button(text, x, y, width, height, color, hover_color, text_color=BLACK, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=((x + width // 2), (y + height // 2)))
    screen.blit(text_surface, text_rect)

def draw_start_screen():
    screen.fill(BACKGROUND)
    text = large_font.render("2048", True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(text, text_rect)

    button_width = 150
    button_height = 50
    button_x = screen.get_width() // 2 - button_width // 2
    button_y = screen.get_height() // 2 + 50
    draw_button("Start Game", button_x, button_y, button_width, button_height, WHITE, (200, 200, 200), action=start_game)
    pygame.display.flip()

def draw_game_over_screen():
    screen.fill(BACKGROUND)
    text = large_font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(text, text_rect)

    button_width = 100
    button_height = 50
    button_x = screen.get_width() // 2 - button_width // 2 - 100
    button_y = screen.get_height() // 2 + 50
    draw_button("Restart", button_x, button_y, button_width, button_height, WHITE, (200, 200, 200), action=start_game)

    button_x = screen.get_width() // 2 - button_width // 2 + 100
    draw_button("Quit", button_x, button_y, button_width, button_height, WHITE, (200, 200, 200), action=quit_game)
    pygame.display.flip()

# Main game loop
def start_game():
    global grid, game_state
    grid = initialize_game()
    game_state = "play"

def quit_game():
    global running
    running = False

game_state = "start"
grid = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "play" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):  # Check if arrow key
                if event.key == pygame.K_UP:
                    moved = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    moved = move_down(grid)
                elif event.key == pygame.K_LEFT:
                    moved = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    moved = move_right(grid)

                if moved:
                    add_random_tile(grid)

                if game_over(grid):
                    game_state = "game_over"

    if game_state == "start":
        draw_start_screen()
    elif game_state == "play":
        draw_grid(grid)
        pygame.display.flip()
    elif game_state == "game_over":
        draw_game_over_screen()

pygame.quit()