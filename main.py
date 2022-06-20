import pygame
import sys
from button import Button

pygame.init()
# Constants
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Pictures/menu_background.jpg")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Fonts/Koulen-Regular.ttf", size)


def wordle():
    while True:
        WORDLE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        WORDLE_TEXT = get_font(45).render("Tuk shte ima wordle.", True, "Black")
        WORDLE_RECT = WORDLE_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(WORDLE_TEXT, WORDLE_RECT)

        WORDLE_BACK = Button(image=None, pos=(80, 650),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        WORDLE_BACK.changeColor(WORDLE_MOUSE_POS)
        WORDLE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WORDLE_BACK.checkForInput(WORDLE_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def worldle():
    while True:
        WORLDLE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        WORLDLE_TEXT = get_font(45).render("Tuk shte ima worldle.", True, "Black")
        WORLDLE_RECT = WORLDLE_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(WORLDLE_TEXT, WORLDLE_RECT)

        WORLDLE_BACK = Button(image=None, pos=(80, 650),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        WORLDLE_BACK.changeColor(WORLDLE_MOUSE_POS)
        WORLDLE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WORLDLE_BACK.checkForInput(WORLDLE_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN = pygame.display.set_mode((1280, 720))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Welcome!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        WORDLE_BUTTON = Button(image=pygame.image.load("Pictures/button_wordle.jpg"), pos=(640, 250),
                             text_input="WORDLE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        WORLDLE_BUTTON = Button(image=pygame.image.load("Pictures/button_worldle.png"), pos=(640, 400),
                             text_input="WORLDLE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Pictures/button_quit.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [WORDLE_BUTTON, WORLDLE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WORDLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    wordle()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if WORLDLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    worldle()
        pygame.display.update()


main_menu()