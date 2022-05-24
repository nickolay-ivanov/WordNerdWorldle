import random
import pygame
import sys
import enchant
import shelve
from five_letter_words import *

WORDS = enchant.Dict("en_US")  # Creates Words dictionary

pygame.init()  # Initialize pygame

# Constants
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("Pictures/Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(980, 300))
ICON = pygame.image.load("Pictures/wordle_logo.png")

pygame.display.set_caption("Wordle")
pygame.display.set_icon(ICON)

GREEN = "#6caf66"
YELLOW = "#ccb658"
GREY = "#808587"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
WHITE = "#FFFFFF"

CORRECT_WORD = random.choice(FIVE_LETTER_WORDS)

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("Fonts/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("Fonts/FreeSansBold.otf", 25)

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

# Global variables
guesses_count = 0
guesses = [[]] * 6  # 2D list that stores the guesses
current_guess = []  # Stores the current guess
current_guess_string = ""
current_letter_bg_x = 773
# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []
game_result = ""


class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 36, self.bg_position[1] + 34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):  # Draws the letter on screen
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):  # Removes a letter
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)  # Draws the square where the letter was deleted
        pygame.display.update()


class Indicator:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = OUTLINE

    def draw(self):  # Draws the indicator on screen
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x + 27, self.y + 30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()


# Drawing the indicators on the screen.

indicator_x, indicator_y = 20, 430

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 100
    if i == 0:
        indicator_x = 50
    elif i == 1:
        indicator_x = 105


def check_guess(guess_to_check):  # Goes through each letter and checks it.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GREY
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()

    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 773

    if guesses_count == 6 and game_result == "":
        game_result = "L"


def play_again():  # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("Fonts/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


def reset():  # Resets all global variables values.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill("white")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    guesses_count = 0
    # A very nice way to find a random 5-letter word, but the developer of the api made it unusable literally on 24.05

    # CORRECT_WORD = "xqx"  # Something so that WORDS.check returns false
    # Gets a random word
    # r = requests.get('https://random-word-api.herokuapp.com/word?length=5', auth=('user', 'pass'))
    # CORRECT_WORD = r.text
    # CORRECT_WORD = CORRECT_WORD[2:-2]  # Removes the symbols before and after the word
    CORRECT_WORD = random.choice(FIVE_LETTER_WORDS)
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()


def create_new_letter():  # Creates a new letter
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 100 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()


def delete_letter():  # Deletes the last letter
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


def get_font(size):  # Font (so unexpected)
    return pygame.font.Font("Fonts/Koulen-Regular.ttf", size)


def print_stats():  # Prints the game stats
    d = shelve.open('stats.txt')  # Opens the file with the statistics
    pygame.draw.rect(SCREEN, "white", (600, 600, 600, 600))
    wordle_played = d['Wordle_Played']
    wordle_wins = d['Wordle_Wins']
    wordle_winstreak = d['Wordle_WinStreak']
    wordle_winpercentage = d['Wordle_WinPercentage']
    wordle_win_in_one = d['Wordle_win_in_one']
    wordle_win_in_two = d['Wordle_win_in_two']
    wordle_win_in_three = d['Wordle_win_in_three']
    wordle_win_in_four = d['Wordle_win_in_four']
    wordle_win_in_five = d['Wordle_win_in_five']
    wordle_win_in_six = d['Wordle_win_in_six']
    statistics = "Played:" + str(wordle_played) + "\nWon: " + str(wordle_wins) + "\nWin%: " + str(wordle_winpercentage)\
                 + "\nWin Streak: " + str(wordle_winstreak) + "\nScore Distribution:""\n 1: " + str(wordle_win_in_one)\
                 + "\n2: " + str(wordle_win_in_two) + "\n3: " + str(wordle_win_in_three) + "\n4: " \
                 + str(wordle_win_in_four) + "\n5: " + str(wordle_win_in_five) + "\n6: " + str(wordle_win_in_six)
    stats_font = pygame.font.Font("Fonts/Koulen-Regular.ttf", 33)
    words = [word.split(' ') for word in statistics.splitlines()]  # 2D array where each row is a list of words.
    space = stats_font.size(' ')[0]  # The width of a space.
    max_width, max_height = 800, 800
    x, y = 10, 10
    for line in words:
        for word in line:
            word_surface = stats_font.render(word, False, GREEN)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = 10  # Reset the x.
                y += word_height  # Start on new row.
            SCREEN.blit(word_surface, (x, y))
            x += word_width + space
        x = 10  # Reset the x.
        y += word_height - 25  # noqa

    pygame.display.update()
    d.close()


def update_stats():
    d = shelve.open('stats.txt')  # Opens the file with the statistics
    d['Wordle_Played'] = d['Wordle_Played'] + 1
    if game_result == 'W':
        d['Wordle_Wins'] = d['Wordle_Wins'] + 1
        d['Wordle_WinStreak'] = d['Wordle_WinStreak'] + 1
        if guesses_count == 1:
            d['Wordle_win_in_one'] = d['Wordle_win_in_one'] + 1
        elif guesses_count == 2:
            d['Wordle_win_in_two'] = d['Wordle_win_in_two'] + 1
        elif guesses_count == 3:
            d['Wordle_win_in_three'] = d['Wordle_win_in_three'] + 1
        elif guesses_count == 4:
            d['Wordle_win_in_four'] = d['Wordle_win_in_four'] + 1
        elif guesses_count == 5:
            d['Wordle_win_in_five'] = d['Wordle_win_in_five'] + 1
        elif guesses_count == 6:
            d['Wordle_win_in_six'] = d['Wordle_win_in_six'] + 1
    else:
        d['Wordle_WinStreak'] = 0
    d['Wordle_WinPercentage'] = round(d['Wordle_Wins'] / d['Wordle_Played'] * 100)
    d.close()


while True:
    if game_result != "":  # Checks if game is finished
        play_again()
    else:
        print_stats()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quits game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    update_stats()
                    reset()
                else:
                    if len(current_guess_string) == 5 and WORDS.check(current_guess_string.lower()):
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:  # Check if backspace is pressed
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":  # Check if user is typing word
                    if len(current_guess_string) < 5:
                        create_new_letter()
            pygame.display.update()
