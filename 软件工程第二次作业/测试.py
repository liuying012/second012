import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Text Test')

# Set up font
try:
    font = pygame.font.SysFont(None, 55)
    text_color = (255, 255, 255)  # White
    text = font.render('Hello World', True, text_color)
except Exception as e:
    print(f"Error loading font: {e}")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the text
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Update the display
    pygame.display.flip()
