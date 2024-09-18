import pygame
import os
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

    # Define game rules
    rules = [
        '游戏规则:',
        '1. 选择一个图标并放入底部的格子。',
        '2. 如果底部的格子中有3个或更多相同的图标，它们将被消除。',
        '3. 消除图标会获得分数。',
        '4. 当所有图标消除或时间耗尽，游戏结束。',
        '5. 分数达到240分将显示成功界面。'
    ]

    # Render and display each rule
    text_y = 50
    for rule in rules:
        rule_text = font.render(rule, True, BLACK)  # Change text color to black
        screen.blit(rule_text, (20, text_y))
        text_y += font.get_height() + 10  # Move down for the next line

    pygame.display.flip()

def draw_main_menu(screen):
    screen.fill((0, 0, 0))  # Clear screen
    background_image_path = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\游戏背景.jpg'
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))

    font = pygame.font.SysFont('simsun', 55)
    title = font.render('选择模式', True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - title.get_height() // 2 - 150))

    options = ['困难模式', '游戏说明', '退出游戏']
    for i, option in enumerate(options):
        option_text = font.render(option, True, (255, 255, 255))
        screen.blit(option_text, (
            SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 - option_text.get_height() // 2 + i * 60))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, option in enumerate(options):
                    option_text = font.render(option, True, (255, 255, 255))
                    rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                        SCREEN_HEIGHT // 2 - option_text.get_height() // 2 + i * 60,
                        option_text.get_width(),
                        option_text.get_height()
                    )
                    if rect.collidepoint(mouse_pos):
                        if option == '困难模式':
                            return 'start_game'
                        elif option == '游戏说明':
                            draw_instructions(screen)
                        elif option == '退出游戏':
                            pygame.quit()
                            sys.exit()

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("拼图游戏")

    while True:
        result = draw_main_menu(screen)
        if result == 'start_game':
            # Start the game (you need to implement the game logic)
            pass
