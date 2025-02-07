import pygame
import math
import random
from nltk.corpus import words
import nltk

# Ensure words list is available
nltk.download('words')

# Setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65

# Function to generate random colors
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Initialize letters with random colors
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    color = random_color()  # Assign a random color
    letters.append([x, y, chr(A + i), True, color])  # Include color in each letter

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 30)  # Reduced size
WORD_FONT = pygame.font.SysFont('comicsans', 50)    # Reduced size
TITLE_FONT = pygame.font.SysFont('comicsans', 50)   # Reduced size

# Load images
images = []
for i in range(7):
    image = pygame.image.load(f"hangman{i}.png")
    images.append(image)

# Game variables
hangman_status = 0
word_list = [word.upper() for word in words.words() if 3 <= len(word) <= 6]
word = random.choice(word_list)
guessed = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Draw buttons
    for letter in letters:
        x, y, ltr, visible, color = letter
        if visible:
            pygame.draw.circle(win, color, (x, y), RADIUS, 3)  # Use assigned color
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman_status], (150, 120))  # Adjusted y coordinate
    pygame.display.update()


def display_message(message, correct_word=None):
    pygame.time.delay(1000)
    win.fill(WHITE)

    # Display the main message
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 - 30))

    # Display the correct word on a new line (if provided)
    if correct_word:
        correct_word_message = f"The word was: {correct_word}"
        text = WORD_FONT.render(correct_word_message, 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 + 30))

    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible, color = letter
                    if visible:
                        # Corrected distance calculation
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        # Check win
        won = all(letter in guessed for letter in word)
        if won:
            display_message("You WON!")
            break

        # Check loss
        if hangman_status == 6:
            display_message("You LOST!", correct_word=word)
            break


main()
pygame.quit()


