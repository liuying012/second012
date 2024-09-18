import pygame
import sys
from ui import draw_main_menu, check_button_click, draw_game_rules
import simple_mode
import hard_mode


# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
CLICK_SOUND_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\点击音效.mp3'
BGM_PATH = r'C:\Users\ASUS\Desktop\软件工程\软件工程第二次作业\背景音乐.mp3'

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module
click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Matching Game")

# Load and play background music (loop indefinitely)
pygame.mixer.music.load(BGM_PATH)
pygame.mixer.music.play(-1)  # Play background music in a loop

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))   # Clear screen with black
        draw_main_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button_clicked = check_button_click(mouse_pos)
                if button_clicked:
                    click_sound.play()  # Play click sound
                if button_clicked == '简单模式':
                    result = simple_mode.run_game()
                    if result == 'exit':
                        running = False   # Exit the main loop
                elif button_clicked == '困难模式':
                    result = hard_mode.run_game()
                    if result == 'exit':
                        running = False   # Exit the main loop
                elif button_clicked == '游戏说明':
                    draw_game_rules(screen)

        clock.tick(30)

if __name__ == "__main__":
    main()
