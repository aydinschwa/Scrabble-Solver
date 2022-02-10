from dawg import *
from board import ScrabbleBoard
import pygame
import sys
import random
import pickle


# returns a list of all words played on the board
def all_board_words(board):
    board_words = []

    # check regular board
    for row in range(0, 15):
        temp_word = ""
        for col in range(0, 16):
            letter = board[row][col].letter
            if letter:
                temp_word += letter
            else:
                if len(temp_word) > 1:
                    board_words.append(temp_word)
                temp_word = ""

    # check transposed board
    for col in range(0, 16):
        temp_word = ""
        for row in range(0, 16):
            letter = board[row][col].letter
            if letter:
                temp_word += letter
            else:
                if len(temp_word) > 1:
                    board_words.append(temp_word)
                temp_word = ""

    return board_words


def refill_word_rack(rack, tile_bag):
    to_add = min([7 - len(rack), len(tile_bag)])
    new_letters = random.sample(tile_bag, to_add)
    rack = rack + new_letters
    return rack, new_letters


def draw_board(board):
    for y in range(15):
        for x in range(15):
            if board[x][y].letter:
                if board[x][y].letter == "I":
                    letter_x_offset = 15
                else:
                    letter_x_offset = 7
                pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])

                letter = tile_font.render(board[x][y].letter, True, (0, 0, 0))
                screen.blit(letter, ((margin + square_width) * x + margin + x_offset + letter_x_offset,
                                     (margin + square_height) * y + margin + y_offset + 7))

                letter_score = modifier_font.render(str(game.point_dict[board[x][y].letter]), True, (0, 0, 0))
                screen.blit(letter_score, ((margin + square_width) * x + margin + x_offset + 31,
                                           (margin + square_height) * y + margin + y_offset + 30))

            elif "3LS" in board[x][y].modifier:
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

            elif "2LS" in board[x][y].modifier:
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

            elif "2WS" in board[x][y].modifier:
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

            elif "3WS" in board[x][y].modifier:
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


def draw_start_screen():
    screen.fill((255, 255, 255))
    intro_text = tile_font.render(f"Scrabble Solver Demonstration", True, (0, 0, 0))
    intro_rect = intro_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(intro_text, intro_rect)

    info_text = tile_font.render(f"Press Space to Generate New Game Once Game is Finished", True, (0, 0, 0))
    info_rect = info_text.get_rect(center=(screen_width // 2, screen_height // 4 + 100))
    screen.blit(info_text, info_rect)

    space_text = tile_font.render("Press Space to Start", True, (0, 0, 0))
    space_rect = space_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(space_text, space_rect)


def draw_rack(rack):
    for i, letter in enumerate(rack):
        if letter == "I":
            letter_x_offset = 15
        else:
            letter_x_offset = 7
        pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * (i + 4) + margin + x_offset,
                                                 700,
                                                 square_width, square_height])

        if letter == "%":
            tile_letter = tile_font.render(" ", True, (0, 0, 0))
        else:
            tile_letter = tile_font.render(letter, True, (0, 0, 0))
        screen.blit(tile_letter, ((margin + square_width) * (i + 4) + margin + x_offset + letter_x_offset,
                                  700 + 7))

        letter_score = modifier_font.render(str(game.point_dict[letter]), True, (0, 0, 0))
        screen.blit(letter_score, ((margin + square_width) * (i + 4) + margin + x_offset + 31,
                                   700 + 30))


def draw_computer_score(word_score_dict):
    x_start = 700
    y_start = 50
    total = 0
    pygame.draw.rect(screen, (210, 180, 140), [x_start, 25, 255, 50])
    score_title = score_font.render("Computer Score", True, (0, 0, 0))
    screen.blit(score_title, (x_start + 50, 25))
    pygame.draw.rect(screen, (210, 180, 140), [x_start, y_start, 255, 700])
    i = 0
    for word, score in word_score_dict.items():
        if y_start * (i+1) > 665:
            x_start += 130
            i = 0
        total += score
        word = score_font.render(word, True, (0, 0, 0))
        score = score_font.render(str(score), True, (0, 0, 0))
        screen.blit(word, (x_start + 2, y_start * (i+1)))
        screen.blit(score, (x_start + 105, y_start * (i+1)))

        i += .35

    total_score = score_font.render(f"Total Score: {total}", True, (0, 0, 0))
    screen.blit(total_score, (705, 700))


if __name__ == "__main__":

    pygame.init()

    # Game-level variables
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    square_width = 40
    square_height = 40
    margin = 3
    mouse_x = 0
    mouse_y = 0
    x_offset = 20
    y_offset = 20
    modifier_font = pygame.font.Font(None, 12)
    tile_font = pygame.font.Font(None, 45)
    score_font = pygame.font.Font(None, 25)
    game_state = "start_screen"

    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
               ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
               ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
               ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

    to_load = open("lexicon/scrabble_words_complete.pickle", "rb")
    root = pickle.load(to_load)
    to_load.close()
    word_rack = random.sample(tile_bag, 7)
    [tile_bag.remove(letter) for letter in word_rack]
    game = ScrabbleBoard(root)
    word_rack = game.get_start_move(word_rack)
    word_rack, new_letters = refill_word_rack(word_rack, tile_bag)
    [tile_bag.remove(letter) for letter in new_letters]

    pygame.display.set_caption("Scrabble")

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "start_screen":
                    game_state = "game_screen"
                if event.key == pygame.K_SPACE and game_state == "end_screen":
                    game_state = "game_screen"
                    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                               ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                               ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                               ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

                    word_rack = random.sample(tile_bag, 7)
                    [tile_bag.remove(letter) for letter in word_rack]
                    game = ScrabbleBoard(root)
                    game.get_start_move(word_rack)
                    word_rack, new_letters = refill_word_rack(word_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

        if game_state == "start_screen":
            draw_start_screen()
            continue

        if game_state == "game_screen":
            screen.fill((0, 0, 0))

            word_rack = game.get_best_move(word_rack)
            word_rack, new_letters = refill_word_rack(word_rack, tile_bag)
            [tile_bag.remove(letter) for letter in new_letters]
            if game.best_word == "":
                # draw new hand if can't find any words
                if len(tile_bag) >= 7:
                    return_to_bag_words = word_rack.copy()
                    word_rack, new_letters = refill_word_rack([], tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                else:
                    game_state = "end_screen"
                    for word in all_board_words(game.board):
                        if not find_in_dawg(word, root) and word:
                            raise Exception(f"Invalid word on board: {word}")

        if game_state == "end_screen":
            draw_board(game.board)
            draw_rack(word_rack)
            draw_computer_score(game.word_score_dict)
            continue

        draw_board(game.board)
        draw_rack(word_rack)
        draw_computer_score(game.word_score_dict)
        pygame.time.wait(75)
