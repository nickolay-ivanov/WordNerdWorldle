import pygame
import random
from countries import countries

pygame.init()
WIDTH, HEIGHT = 640, 720
GAME_WON = False
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
COLOR_INACTIVE = pygame.Color('red')
COLOR_ACTIVE = pygame.Color('aqua')
COLOR_FILLED = pygame.Color('Grey')
FONT = pygame.font.Font("Fonts/Koulen-Regular.ttf", 25)
AVAIABLE_COUNTRIES = countries
CURRENT_ANSWER = ""
CORRECT_COUNTRY = random.choice(list(AVAIABLE_COUNTRIES))
FIRST_GUESS = ""
GUESSES = [[]] * 6
NUM_OF_GUESSES_MADE = 0
AVAILABLE_COUNTRIES_1 = "AVAILABLE COUNTRIES:\nAfghanistan\nAlbania\nAlgeria\nAndorra\nAngola\nArgentina\nArmenia\n" \
                        "Australia\nAustria\nAzerbaijan\nBahrain\nBelarus\nBelgium\nBolivia\nBosnia\nBrazil\n" \
                        "Bulgaria\nBurkina Faso\nBurma\nBurundi\nCambodia"
AVAILABLE_COUNTRIES_2 = "Cameroon\nCanada\nCape Verde\nChile\nChina\nCosta Rica\nCroatia\nCuba\nCyprus\n" \
                        "Czech Republic\nDenmark\nEcuador\nEgypt\nGeorgia\nGermany\nGhana\nGibraltar\nIvory Coast\n" \
                        "Macedonia\nRomania\nRussia"


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.filled = False
        self.checked = False

    def handle_event(self, event):
        if self.filled is False:  # Checks if box is empty
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):  # If the user clicked on the input_box rect.
                    self.active = not self.active  # Toggle the active variable.
                else:
                    self.active = False
                if self.active:
                    self.color = COLOR_ACTIVE  # Change the color of the input box to active.
                else:
                    self.color = COLOR_INACTIVE  # Change the color of the input box to inactive.
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN and self.text.title() in countries:
                        self.filled = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]  # Deletes the last letter with backspace
                    elif self.txt_surface.get_width() <= 210 and event.key != pygame.K_RETURN:
                        self.text += event.unicode  # Adds new letter
                    self.txt_surface = FONT.render(self.text, True, self.color)  # Re-renders the text.
        else:
            self.color = COLOR_FILLED

    def update(self):
        # Resize the box if the text is too long.
        if self.txt_surface.get_width() + 10 <= 230:
            width = max(200, self.txt_surface.get_width() + 10)
            self.rect.w = width

    def draw(self, SCREEN):
        # Blit the text.
        SCREEN.blit(self.txt_surface, (self.rect.x + 5, self.rect.y - 5))
        # Blit the rect.
        pygame.draw.rect(SCREEN, self.color, self.rect, 2)


def print_countries_list(countries_to_print, start_x, start_y):
    countries_font = pygame.font.Font("Fonts/Koulen-Regular.ttf", 20)
    words = [word.split(' ') for word in countries_to_print.splitlines()]  # 2D array in each row is a list of words.
    space = countries_font.size(' ')[0]  # The width of a space.
    max_width, max_height = 800, 800
    x = start_x
    y = start_y
    for line in words:
        for word in line:
            word_surface = countries_font.render(word, False, "white")
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:  # If end is reached, start a new row
                x = start_x  # Reset
                y += start_y  # New Row
            SCREEN.blit(word_surface, (x, y))
            x += word_width + space
        # Start a new row with the new line
        x = start_x  # Reset
        y += word_height - 20  # noqa


def calculate_distance(box):
    if box.checked is False:
        if box.text.title() in countries:
            CURRENT_ANSWER = box.text.title()
        else:
            CURRENT_ANSWER = ""
        if CURRENT_ANSWER in countries and box.filled:
            if CURRENT_ANSWER == CORRECT_COUNTRY:
                text = "BINGO! You won the game!"
                global GAME_WON
                GAME_WON = True
            else:
                if AVAIABLE_COUNTRIES[CURRENT_ANSWER][0] > AVAIABLE_COUNTRIES[CORRECT_COUNTRY][0]:
                    if AVAIABLE_COUNTRIES[CURRENT_ANSWER][1] > AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1]:
                        text = "The country is %d degrees South and %d degrees East to %s!" % \
                               ((AVAIABLE_COUNTRIES[CURRENT_ANSWER][0] - AVAIABLE_COUNTRIES[CORRECT_COUNTRY][0]),
                                (AVAIABLE_COUNTRIES[CURRENT_ANSWER][1] - AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1]),
                                (CURRENT_ANSWER))
                    else:
                        text = "The country is %d degrees South and %d degrees West to %s!" % \
                               ((AVAIABLE_COUNTRIES[CURRENT_ANSWER][0] - AVAIABLE_COUNTRIES[CORRECT_COUNTRY][0]),
                                (AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1] - AVAIABLE_COUNTRIES[CURRENT_ANSWER][1]),
                                (CURRENT_ANSWER))
                else:
                    if AVAIABLE_COUNTRIES[CURRENT_ANSWER][1] > AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1]:
                        text = "The country is %d degrees North and %d degrees East to %s!" % \
                               ((AVAIABLE_COUNTRIES[CORRECT_COUNTRY][0] - AVAIABLE_COUNTRIES[CURRENT_ANSWER][0]),
                                (AVAIABLE_COUNTRIES[CURRENT_ANSWER][1] - AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1]),
                                (CURRENT_ANSWER))
                    else:
                        text = "The country is %d degrees North and %d degrees West to %s!" % \
                               ((AVAIABLE_COUNTRIES[CORRECT_COUNTRY][0] - AVAIABLE_COUNTRIES[CURRENT_ANSWER][0]),
                                (AVAIABLE_COUNTRIES[CORRECT_COUNTRY][1] - AVAIABLE_COUNTRIES[CURRENT_ANSWER][1]),
                                (CURRENT_ANSWER))

            box.checked = True
            global NUM_OF_GUESSES_MADE
            global GUESSES
            GUESSES[NUM_OF_GUESSES_MADE] = CURRENT_ANSWER
            NUM_OF_GUESSES_MADE = NUM_OF_GUESSES_MADE + 1
            return text


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 40, 140, 32)
    input_box2 = InputBox(400, 80, 140, 32)
    input_box3 = InputBox(400, 120, 140, 32)
    input_box4 = InputBox(400, 160, 140, 32)
    input_box5 = InputBox(400, 200, 140, 32)
    input_box6 = InputBox(400, 240, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5, input_box6]
    done = False
    while done is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        SCREEN.fill((30, 30, 30))
        print_countries_list(AVAILABLE_COUNTRIES_1, 10, 10)
        print_countries_list(AVAILABLE_COUNTRIES_2, 140, 30)
        results_font = pygame.font.Font("Fonts/Koulen-Regular.ttf", 22)

        for box in input_boxes:
            box.draw(SCREEN)

        text_1 = calculate_distance(input_box1)
        if text_1 is not None:
            first = text_1
        if input_box1.filled:
            print_text_1 = results_font.render(first, True, "aqua")  # noqa
            text_1Rect = print_text_1.get_rect()
            text_1Rect.center = (WIDTH // 2, HEIGHT // 2 + 70)
            SCREEN.blit(print_text_1, text_1Rect)

        text_2 = calculate_distance(input_box2)
        if text_2 is not None:
            second = text_2
        if input_box2.filled:
            print_text_2 = results_font.render(second, True, "aqua")  # noqa
            text_2Rect = print_text_2.get_rect()
            text_2Rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
            SCREEN.blit(print_text_2, text_2Rect)

        text_3 = calculate_distance(input_box3)
        if text_3 is not None:
            third = text_3
        if input_box3.filled:
            print_text_3 = results_font.render(third, True, "aqua")  # noqa
            text_3Rect = print_text_3.get_rect()
            text_3Rect.center = (WIDTH // 2, HEIGHT // 2 + 130)
            SCREEN.blit(print_text_3, text_3Rect)

        text_4 = calculate_distance(input_box4)
        if text_4 is not None:
            fourth = text_4
        if input_box4.filled:
            print_text_4 = results_font.render(fourth, True, "aqua")  # noqa
            text_4Rect = print_text_4.get_rect()
            text_4Rect.center = (WIDTH // 2, HEIGHT // 2 + 160)
            SCREEN.blit(print_text_4, text_4Rect)

        text_5 = calculate_distance(input_box5)
        if text_5 is not None:
            fifth = text_5
        if input_box5.filled:
            print_text_5 = results_font.render(fifth, True, "aqua")  # noqa
            text_5Rect = print_text_5.get_rect()
            text_5Rect.center = (WIDTH // 2, HEIGHT // 2 + 190)
            SCREEN.blit(print_text_5, text_5Rect)

        text_6 = calculate_distance(input_box6)
        if text_6 is not None:
            sixth = text_6
        if input_box6.filled:
            print_text_6 = results_font.render(sixth, True, "aqua")  # noqa
            text_6Rect = print_text_6.get_rect()
            text_6Rect.center = (WIDTH // 2, HEIGHT // 2 + 220)
            SCREEN.blit(print_text_6, text_6Rect)

        if input_box1.filled and input_box2.filled and input_box3.filled and input_box4.filled and \
                input_box5.filled and input_box6.filled and GAME_WON is False:
            game_over = results_font.render("You Lost!", True, "aqua")  # noqa
            game_overRect = game_over.get_rect()
            game_overRect.center = (WIDTH // 2, HEIGHT // 2 + 270)
            SCREEN.blit(game_over, game_overRect)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()
