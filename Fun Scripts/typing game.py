import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

# Turret settings
turret_x = WIDTH // 2
turret_y = HEIGHT - 50
turret_speed = 5


# Ship settings
ships = []
ship_speed = 2

# Word list
word_list = ["ship1", "ship2", "ship3", "ship4"]  # Add more words as needed

# Function to create a new ship
def create_ship():
    word = random.choice(word_list)
    x = random.randint(0, WIDTH)
    y = 0
    ships.append({"word": word, "x": x, "y": y})

# Game loop
running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the turret
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and turret_x > 0:
        turret_x -= turret_speed
    if keys[pygame.K_RIGHT] and turret_x < WIDTH:
        turret_x += turret_speed

    # Create new ships at random intervals
    if random.randint(1, 100) == 1:
        create_ship()

    # Move and draw ships
    for ship in ships:
        ship["y"] += ship_speed
        text_surface = FONT.render(ship["word"], True, WHITE)
        screen.blit(text_surface, (ship["x"], ship["y"]))

    # Remove ships that have gone off the screen
    ships = [ship for ship in ships if ship["y"] < HEIGHT]

    # Check for collisions with the turret
    for ship in ships:
        if ship["y"] + text_surface.get_height() >= turret_y:
            input_word = ""
            current_word = ""
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_word == ship["word"]:
                            ships.remove(ship)
                            score += 1
                    elif event.key == pygame.K_BACKSPACE:
                        input_word = input_word[:-1]
                    else:
                        current_word += event.unicode
                        input_word = current_word.lower()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the turret
    pygame.draw.rect(screen, WHITE, (turret_x, turret_y, 20, 20))

    # Draw the score
    score_text = FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
