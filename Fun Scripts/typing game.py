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
turret_width, turret_height = 20, 20
turret_x = WIDTH // 2 - turret_width // 2
turret_y = HEIGHT - 50
turret_speed = 5

# Ship settings
ships = []
ship_speed = .1

# Word list
word_list = [
    "apple", "banana", "carrot", "elephant", "giraffe", "umbrella", "mountain", "ocean", 
    "sunshine", "firefly", "treasure", "whisper", "happiness", "laughter", "courage", 
    "infinity", "serendipity", "harmony", "tranquility", "effervescent"
]  # Add more words as needed

# Function to create a new ship
def create_ship():
    word = random.choice(word_list)
    x = random.randint(0, WIDTH - FONT.size(word)[0])
    y = 0
    ships.append({"word": word, "x": x, "y": y, "width": FONT.size(word)[0], "height": FONT.size(word)[1]})

# Game loop
running = True
score = 0
input_word = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the turret
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and turret_x > 0:
        turret_x -= turret_speed
    if keys[pygame.K_RIGHT] and turret_x < WIDTH - turret_width:
        turret_x += turret_speed

    # Check for collisions with the turret
    for ship in ships:
        if (
            turret_x < ship["x"] + ship["width"]
            and turret_x + turret_width > ship["x"]
            and turret_y < ship["y"] + ship["height"]
            and turret_y + turret_height > ship["y"]
        ):
            if input_word == ship["word"]:
                ships.remove(ship)
                score += 1
            input_word = ""

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_word = ""
            elif event.key == pygame.K_BACKSPACE:
                input_word = input_word[:-1]
            else:
                input_word += event.unicode.lower()

    # Create new ships at random intervals
    if random.randint(1, 100) == 1:
        create_ship()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the turret
    pygame.draw.rect(screen, WHITE, (turret_x, turret_y, turret_width, turret_height))

    # Move and draw ships
    for ship in ships:
        ship["y"] += ship_speed
        text_surface = FONT.render(ship["word"], True, WHITE)
        screen.blit(text_surface, (ship["x"], ship["y"]))

    # Remove ships that have gone off the screen
    ships = [ship for ship in ships if ship["y"] < HEIGHT]

    # Draw the score
    score_text = FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw the typed word
    input_text = FONT.render(input_word, True, WHITE)
    screen.blit(input_text, (turret_x, turret_y + turret_height))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
