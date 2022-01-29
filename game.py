from dawg import build_dawg
from board import Square, ScrabbleBoard, play_scrabble_game, refill_word_rack
import pygame
import sys

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
square_width = 40
square_height = 40
margin = 3
mouse_x = 0
mouse_y = 0
x_offset = 170
y_offset = 50

pygame.init()

modifier_font = pygame.font.Font(None, 12)
tile_font = pygame.font.Font(None, 45)

big_list = open("lexicon/scrabble_words_complete.txt", "r").readlines()
big_list = [word.strip("\n") for word in big_list]
root = build_dawg(big_list)

game = play_scrabble_game(root)
point_dict = game.point_dict
board = game.board

pygame.display.set_caption("Scrabble")
pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
            # print(f"Click: [{mouse_x}, {mouse_y}]")
            # board[(mouse_x - x_offset) // (square_width + margin)][
            #     (mouse_y - y_offset) // (square_height + margin)] = "Green"
    screen.fill((0, 0, 0))
    for y in range(15):
        for x in range(15):
            if board[x][y].letter:
                pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                letter = tile_font.render(board[x][y].letter, True, (0, 0, 0))
                screen.blit(letter, ((margin + square_width) * x + margin + x_offset + 7,
                                     (margin + square_height) * y + margin + y_offset + 7))

                letter_score = modifier_font.render(str(point_dict[board[x][y].letter]), True, (0, 0, 0))
                screen.blit(letter_score, ((margin + square_width) * x + margin + x_offset + 31,
                                           (margin + square_height) * y + margin + y_offset + 30))

            elif board[x][y].modifier == "3LS":
                pygame.draw.rect(screen, (0, 100, 200), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, (0, 0, 0))
                text_mid = modifier_font.render("LETTER", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif board[x][y].modifier == "2LS":
                pygame.draw.rect(screen, (173, 216, 230), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, (0, 0, 0))
                text_mid = modifier_font.render("LETTER", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif board[x][y].modifier == "2WS":
                pygame.draw.rect(screen, (255, 204, 203), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, (0, 0, 0))
                text_mid = modifier_font.render("WORD", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif board[x][y].modifier == "3WS":
                pygame.draw.rect(screen, (237, 28, 36), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, (0, 0, 0))
                text_mid = modifier_font.render("WORD", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            else:
                pygame.draw.rect(screen, (210, 180, 140), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])

    player_position = pygame.mouse.get_pos()
    mouse_x = player_position[0]
    mouse_y = player_position[1]

    pygame.display.update()
    clock.tick(60)
