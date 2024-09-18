import pygame
import random
import os
import pygame.mixer
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ICON_SIZE = 64
NUM_ICONS_X = 6
NUM_ICONS_Y = 4
TIME_LIMIT = 30   # Seconds
INITIAL_SCORE = 0
ICON_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\图标'
ICON_COUNT = 8   # Number of unique icons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
pygame.mixer.init()

# Load sound effects
success_sound = pygame.mixer.Sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏通关.mp3')
failure_sound = pygame.mixer.Sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏失败.mp3')

# Load icons
def load_icons():
    icons = []
    for i in range(1, ICON_COUNT + 1):
        icon_path = os.path.join(ICON_PATH, f'图标{i}.jpg')
        try:
            icon_image = pygame.image.load(icon_path)
            icon_image = pygame.transform.scale(icon_image, (ICON_SIZE, ICON_SIZE))
            icons.append(icon_image)
        except pygame.error as e:
            print(f"Unable to load icon image at {icon_path}. Error: {e}")
    return icons

def create_icon_grid(icons):
    icon_pairs = icons * 2   # Each icon appears twice
    random.shuffle(icon_pairs)   # Shuffle to randomize icon positions
    return icon_pairs

def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Unable to play sound at {file_path}. Error: {e}")

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
    pygame.display.set_caption("拼图游戏 - 简单模式")
    clock = pygame.time.Clock()

    # Load icons and initialize variables
    icons = load_icons()
    if not icons:
        print("No icons loaded, exiting.")
        pygame.quit()
        sys.exit()

    icon_images = create_icon_grid(icons)

    # Position icons randomly with overlap
    positions = [(random.randint(0, SCREEN_WIDTH - ICON_SIZE), random.randint(0, SCREEN_HEIGHT - ICON_SIZE))
                 for _ in range(NUM_ICONS_X * NUM_ICONS_Y)]
    icon_rects = [pygame.Rect(x, y, ICON_SIZE, ICON_SIZE) for x, y in positions]

    selected_icons = []
    score = INITIAL_SCORE
    start_time = pygame.time.get_ticks()

    def draw_game():
        screen.fill((0, 0, 0))   # Clear screen
        background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏背景.jpg'
        try:
            background_image = pygame.image.load(background_image_path)
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(background_image, (0, 0))
        except pygame.error as e:
            print(f"Unable to load background image at {background_image_path}. Error: {e}")
            screen.fill((0, 0, 0))  # Fallback to a black screen if the image can't be loaded

        # Draw icons
        for rect, image in zip(icon_rects, icon_images):
            if image:   # Only draw visible icons
                screen.blit(image, rect.topleft)

        # Draw score and countdown timer
        font = pygame.font.SysFont('simsun', 40)
        time_left = max(0, TIME_LIMIT - (pygame.time.get_ticks() - start_time) // 1000)
        score_text = font.render(f'分数: {score}', True, (255, 255, 255))
        countdown_text = font.render(f'剩余时间: {time_left}s', True, (255, 255, 255))

        # Draw text on screen
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        screen.blit(countdown_text, (10, 10))

        pygame.display.flip()
        return time_left

    running = True
    while running:
        time_left = draw_game()

        # Handle game over conditions
        if time_left == 0 and any(icon_images):
            play_sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\点击音效.mp3')
            result = draw_game_over(screen, success=False)
            if result == 'restart':
                return 'restart'   # Restart game
            elif result == 'exit':
                pygame.quit()
                sys.exit()
        elif not any(icon_images):  # No more icons means the game is complete
            play_sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\点击音效.mp3')
            result = draw_game_over(screen, success=True)
            if result == 'restart':
                return 'restart'   # Restart game
            elif result == 'exit':
                pygame.quit()
                sys.exit()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse click to select icons
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\点击音效.mp3')
                mouse_pos = event.pos
                clicked = False
                for i, rect in enumerate(icon_rects):
                    if rect.collidepoint(mouse_pos):  # Check if click is on an icon
                        clicked = True
                        if len(selected_icons) == 0:
                            selected_icons.append(i)  # Select the first icon
                        elif len(selected_icons) == 1:
                            second_selection = i
                            if selected_icons[0] != second_selection and icon_images[selected_icons[0]] == icon_images[second_selection]:
                                score += 10  # Add points if icons match
                                # Remove matched icons
                                for idx in sorted([selected_icons[0], second_selection], reverse=True):
                                    icon_images[idx] = None
                                # Play elimination sound
                                play_sound(r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\消除音效.mp3')
                                # Reset selection after match
                                selected_icons = []
                            else:
                                selected_icons = []  # Reset if no match
                        break

        clock.tick(30)

    pygame.quit()
