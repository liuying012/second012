import pygame
import random
import os
import pygame.mixer
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ICON_SIZE = 64
ICON_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\图标'
ICON_COUNT = 10  # Number of unique icons
GRID_SIZE = 5  # Number of slots in the grid
INITIAL_ICON_MULTIPLIER = 3  # Each icon appears 3 times
NUM_ICONS_X = 6
NUM_ICONS_Y = 4
COUNTDOWN_TIME = 30  # Countdown time in seconds
SUCCESS_SCORE = 300  # Score needed to win

pygame.mixer.init()

# Load sound effects
success_sound = pygame.mixer.Sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏通关.mp3')
failure_sound = pygame.mixer.Sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏失败.mp3')

# Load sound effects
CLICK_SOUND_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\点击音效.mp3'
ELIMINATION_SOUND_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\消除音效.mp3'


def load_icons():
    icons = []
    for i in range(1, ICON_COUNT + 1):
        icon_path = os.path.join(ICON_PATH, f'图标{i}.jpg')
        icon_image = pygame.image.load(icon_path)
        icon_image = pygame.transform.scale(icon_image, (ICON_SIZE, ICON_SIZE))
        icons.append(icon_image)
    return icons


def draw_game_over(screen, success):
    screen.fill((0, 0, 0))  # Clear screen

    if success:
        success_sound.play()  # Play success sound
        background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\通关啦.jpg'
    else:
        failure_sound.play()  # Play failure sound
        background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏结束.jpg'

    # Load and display background image
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))

    # Load and display buttons
    restart_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\重新开始.jpg'
    exit_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\退出游戏.jpg'
    restart_image = pygame.image.load(restart_image_path)
    exit_image = pygame.image.load(exit_image_path)
    restart_image = pygame.transform.scale(restart_image, (150, 60))
    exit_image = pygame.transform.scale(exit_image, (150, 60))

    # Get positions to center the buttons horizontally and place them vertically one after another
    restart_x = SCREEN_WIDTH // 2 - restart_image.get_width() // 2
    restart_y = SCREEN_HEIGHT // 2 - restart_image.get_height() // 2 - 30
    exit_x = SCREEN_WIDTH // 2 - exit_image.get_width() // 2
    exit_y = SCREEN_HEIGHT // 2 - exit_image.get_height() // 2 + 90

    screen.blit(restart_image, (restart_x, restart_y))
    screen.blit(exit_image, (exit_x, exit_y))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if '重新开始' (Restart) button is clicked
                if pygame.Rect(restart_x, restart_y, restart_image.get_width(), restart_image.get_height()).collidepoint(mouse_pos):
                    return 'restart'

                # Check if '退出游戏' (Exit Game) button is clicked
                if pygame.Rect(exit_x, exit_y, exit_image.get_width(), exit_image.get_height()).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("拼图游戏 - 困难模式")
    clock = pygame.time.Clock()

    # Load sound effects
    click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)
    elimination_sound = pygame.mixer.Sound(ELIMINATION_SOUND_PATH)

    def start_game():
        # Load icons and initialize variables
        icons = load_icons()
        icon_pool = icons * INITIAL_ICON_MULTIPLIER  # 3 of each icon
        random.shuffle(icon_pool)

        icon_grid = [None] * GRID_SIZE  # Initialize empty slots at the bottom
        score = 0
        countdown = COUNTDOWN_TIME  # Initialize countdown timer

        # Generate random positions for the icons
        positions = []
        grid_area_y = SCREEN_HEIGHT - ICON_SIZE - 20  # Bottom grid area y coordinate
        for _ in range(len(icon_pool)):
            while True:
                x = random.randint(0, SCREEN_WIDTH - ICON_SIZE)
                y = random.randint(0, SCREEN_HEIGHT - ICON_SIZE - 100)  # Limit y to avoid bottom grid
                if y < grid_area_y - ICON_SIZE:  # Ensure icons don't overlap with bottom grid
                    positions.append((x, y))
                    break

        clicked_icons = []  # To store already clicked icons
        selected_icon = None

        def draw_game():
            screen.fill((0, 0, 0))  # Clear screen
            background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏背景.jpg'
            background_image = pygame.image.load(background_image_path)
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(background_image, (0, 0))

            # Draw icons at their positions
            for i, (x, y) in enumerate(positions):
                if i < len(icon_pool) and i not in clicked_icons:
                    screen.blit(icon_pool[i], (x, y))

            # Draw grid slots at the bottom
            for i in range(GRID_SIZE):
                rect = pygame.Rect(i * (ICON_SIZE + 10) + (SCREEN_WIDTH - GRID_SIZE * ICON_SIZE) // 2,
                                   SCREEN_HEIGHT - ICON_SIZE - 20, ICON_SIZE, ICON_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border for grid slots
                if icon_grid[i]:
                    screen.blit(icon_grid[i], rect.topleft)

            # Draw score
            font = pygame.font.SysFont('simsun', 40)
            score_text = font.render(f'分数: {score}', True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

            # Draw countdown timer
            countdown_text = font.render(f'倒计时: {int(countdown)}', True, (255, 0, 0))
            screen.blit(countdown_text, (10, 10))

            pygame.display.flip()

        def check_for_matches():
            nonlocal score
            icon_count = {}

            # Count icons in the grid
            for icon in icon_grid:
                if icon:
                    if icon not in icon_count:
                        icon_count[icon] = 0
                    icon_count[icon] += 1

            # Find icons with count 3 or more
            for icon, count in icon_count.items():
                if count >= 3:
                    # Clear all occurrences of this icon
                    for i in range(GRID_SIZE):
                        if icon_grid[i] == icon:
                            icon_grid[i] = None  # Clear icon from grid
                    score += count * 10  # Add points for each cleared icon
                    elimination_sound.play()  # Play elimination sound

        running = True
        while running:
            draw_game()

            # Update countdown timer
            countdown -= 1 / 30  # Decrease countdown every second (30 FPS)
            if countdown <= 0:
                countdown = 0
                if not icon_pool and all(icon is None for icon in icon_grid):
                    result = draw_game_over(screen, success=False)
                    if result == 'restart':
                        return  # Restart game
                elif score < SUCCESS_SCORE:
                    result = draw_game_over(screen, success=False)
                    if result == 'restart':
                        return  # Restart game

            # Check if the game is won
            if score >= SUCCESS_SCORE:
                result = draw_game_over(screen, success=True)
                if result == 'restart':
                    return  # Restart game

            # Check if game is over (all slots are filled and no place to put new icons)
            if all(icon_grid):
                result = draw_game_over(screen, success=False)
                if result == 'restart':
                    return  # Restart game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Check if player clicked an icon for selection
                    for i in reversed(range(len(positions))):  # Check from topmost to bottommost
                        x, y = positions[i]
                        if i < len(icon_pool) and i not in clicked_icons and pygame.Rect(x, y, ICON_SIZE,
                                                                                         ICON_SIZE).collidepoint(
                                mouse_pos):
                            selected_icon = icon_pool[i]
                            clicked_icons.append(i)  # Mark this icon as clicked
                            click_sound.play()  # Play click sound
                            break

                    # Place selected icon in the first empty slot in the bottom grid
                    if selected_icon:
                        for i in range(GRID_SIZE):
                            if icon_grid[i] is None:
                                icon_grid[i] = selected_icon
                                selected_icon = None  # Reset selection
                                break
                        check_for_matches()

            clock.tick(30)

    start_game()


pygame.quit()
