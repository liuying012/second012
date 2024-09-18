import pygame
from constants import *
import sys

# Define button rectangles globally or pass them around as needed
BUTTON_RECTANGLES = {}

def draw_main_menu(screen):
    # Load and display background image
    background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏界面.jpg'
    try:
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Unable to load image at {background_image_path}. Error: {e}")
        screen.fill(BLACK)  # Fallback to a black screen if the image can't be loaded

    # Load button images
    try:
        simple_mode_image = pygame.image.load(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\简单模式.jpg')
        hard_mode_image = pygame.image.load(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\困难模式.jpg')
        rules_image = pygame.image.load(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏说明.jpg')

        # Scale images to button size
        simple_mode_image = pygame.transform.scale(simple_mode_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
        hard_mode_image = pygame.transform.scale(hard_mode_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
        rules_image = pygame.transform.scale(rules_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
    except pygame.error as e:
        print(f"Error loading button images: {e}")
        return

    # Set vertical spacing
    vertical_spacing = 80
    initial_y = SCREEN_HEIGHT // 2 - (vertical_spacing * 2) // 2

    global BUTTON_RECTANGLES  # Use the global variable to store button rectangles
    BUTTON_RECTANGLES = {}  # Initialize the button rectangles dictionary

    # Define button positions
    buttons = [
        ("简单模式", simple_mode_image, initial_y),
        ("困难模式", hard_mode_image, initial_y + vertical_spacing),
        ("游戏说明", rules_image, initial_y + 2 * vertical_spacing),
    ]

    for item, image, y_pos in buttons:
        # Create button rectangle
        button = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT)
        BUTTON_RECTANGLES[item] = button  # Store the rectangle
        screen.blit(image, (button.x, button.y))  # Draw the button image

def draw_game_screen(screen, tiles):
    # Load and display background image
    background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏界面.jpg'
    try:
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Unable to load image at {background_image_path}. Error: {e}")
        screen.fill(BLACK)  # Fallback to a black screen if the image can't be loaded

    # Draw tiles
    for y in range(NUM_TILES_Y):
        for x in range(NUM_TILES_X):
            color = (255, 0, 0) if tiles[y][x] == 'A' else (0, 255, 0) if tiles[y][x] == 'B' else (0, 0, 255) if tiles[y][x] == 'C' else (255, 255, 0)
            pygame.draw.rect(screen, color, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

def draw_game_over(screen):
    # Use default font
    font = pygame.font.SysFont('simsun', 55)  # Use default font
    # Draw game over text
    game_over_text = font.render('Game Over', True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

def draw_countdown(screen, time_left):
    # Use default font
    font = pygame.font.SysFont('simsun', 40)  # Use default font

    # Draw countdown timer
    countdown_text = font.render(f'Time Left: {time_left}s', True, WHITE)
    screen.blit(countdown_text, (10, 10))

def check_button_click(mouse_pos):
    """
    Check if the mouse click is within any of the menu buttons.
    """
    for item, rect in BUTTON_RECTANGLES.items():
        if rect.collidepoint(mouse_pos):
            return item
    return None

def draw_game_rules(screen):
    # Load and display background image
    background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏界面.jpg'
    try:
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Unable to load image at {background_image_path}. Error: {e}")
        screen.fill(BLACK)  # Fallback to a black screen if the image can't be loaded

    # Use default font
    font = pygame.font.SysFont('simsun', 40)

    # Display game rules
    rules = [
        "游戏规则:",
        "简单模式：连连看",
        "困难模式：",
        "1. 选择图标并放置在底部的空格中。",
        "2. 三个相同的图标会被消除。",
        "3. 游戏倒计时30秒，时间到则游戏结束。",
        "4. 所有图标消除后则游戏成功。",
    ]

    y_offset = SCREEN_HEIGHT // 4
    for line in rules:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()

    # Wait for user to click to return to main menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
