from dawg import build_dawg, find_in_dawg
import copy

big_list = open("lexicon/scrabble_words_complete.txt", "r").readlines()
big_list = [word.strip("\n") for word in big_list]
root = build_dawg(big_list)

word_score_dict = {}
word_rack = ["E", "O", "U", "C", "T", "A", "E"]


class Square:
    # default behavior is blank square, no score modifier, all cross-checks valid
    def __init__(self, letter=None, modifier=None, sentinel=1):
        self.letter = letter
        self.cross_checks = [sentinel] * 26
        self.modifier = modifier
        self.visible = True
        if sentinel == 0:
            self.visible = False

    def __str__(self):
        if not self.visible:
            return ""
        if not self.letter:
            return "_"
        else:
            return self.letter


class ScrabbleBoard:
    def __init__(self):

        row_1 = \
            [Square(modifier="3WS"), Square(), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="3WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(modifier="3WS"),
             Square(sentinel=0)]
        row_15 = copy.deepcopy(row_1)

        row_2 = \
            [Square(), Square(modifier="2WS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="2WS"), Square(),
             Square(sentinel=0)]
        row_14 = copy.deepcopy(row_2)

        row_3 = \
            [Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(sentinel=0)]
        row_13 = copy.deepcopy(row_3)

        row_4 = \
            [Square(modifier="2LS"), Square(), Square(), Square(modifier="2WS"), Square(),
             Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(), Square(modifier="2WS"), Square(), Square(), Square(modifier="2LS"),
             Square(sentinel=0)]
        row_12 = copy.deepcopy(row_4)

        row_5 = \
            [Square(), Square(), Square(), Square(), Square(modifier="2WS"),
             Square(), Square(), Square(), Square(), Square(),
             Square(modifier="2WS"), Square(), Square(), Square(), Square(),
             Square(sentinel=0)]
        row_11 = copy.deepcopy(row_5)

        row_6 = \
            [Square(), Square(modifier="3LS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="3LS"), Square(),
             Square(sentinel=0)]
        row_10 = copy.deepcopy(row_6)

        row_7 = \
            [Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(sentinel=0)]
        row_9 = copy.deepcopy(row_7)

        row_8 = \
            [Square(modifier="3WS"), Square(), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="START"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(modifier="3WS"),
             Square(sentinel=0)]

        row_16 = [Square(sentinel=0) for _ in range(15)]

        self.board = [row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,
                      row_9, row_10, row_11, row_12, row_13, row_14, row_15, row_16]
        self.word_score_dict = {}

    def print_board(self):
        for row in self.board:
            [print(square, end=" ") for square in row]
            print()
        print()

    # method to insert words into board by row and column number
    # using 1-based indexing for user input
    def insert_word(self, row, col, word):
        row -= 1
        col -= 1
        if len(word) + col > 15:
            print(f'Cannot insert word "{word}" at column {col + 1}, not enough space')
            return
        curr_col = col
        for i, letter in enumerate(word):
            curr_square_letter = self.board[row][curr_col].letter
            # if current square already has a letter in it, check to see if it's the same letter as
            # the one we're trying to insert. If not, insertion fails, undo any previous insertions
            if curr_square_letter:
                if curr_square_letter == letter:
                    curr_col += 1
                else:
                    print(f'Failed to insert letter "{letter}" of "{word}" at column {curr_col + 1}, '
                          f'column is occupied by letter "{curr_square_letter}"')
                    for _ in range(i):
                        curr_col -= 1
                        self.board[row][curr_col].letter = None

                    return
            else:
                self.board[row][curr_col].letter = letter
                curr_col += 1

    # transpose method that modifies self.board inplace
    def transpose(self):
        # https://datagy.io/python-transpose-list-of-lists/
        transposed_tuples = copy.deepcopy(list(zip(*self.board)))
        self.board = [list(sublist) for sublist in transposed_tuples]

    def _score_word(self, word):
        score = 0
        point_dict = {"A": 1, "B": 3, "C": 3, "D": 2,
                      "E": 1, "F": 4, "G": 2, "H": 4,
                      "I": 1, "J": 8, "K": 5, "L": 1,
                      "M": 3, "N": 1, "O": 1, "P": 3,
                      "Q": 10, "R": 1, "S": 1, "T": 1,
                      "U": 1, "V": 4, "W": 4, "X": 8,
                      "Y": 8, "Z": 10}

        for letter in word:
            score += point_dict[letter]
        return word, score

    def _extend_right(self, start_node, square_row, square_col, rack, word):
        square = self.board[square_row][square_col]
        if start_node.is_terminal:
            word, score = self._score_word(word)
            self.word_score_dict[word] = score

        # execute if square is empty
        if not square.letter:
            for letter in rack:
                if letter in start_node.children:
                    new_node = start_node.children[letter]
                    new_rack = rack.copy()
                    new_rack.remove(letter)
                    new_word = word + letter
                    self._extend_right(new_node, square_row, square_col + 1, new_rack, new_word)
        else:
            if square.letter in start_node.children:
                new_node = start_node.children[square.letter]
                new_word = word + square.letter
                self._extend_right(new_node, square_row, square_col + 1, rack, new_word)

    # TODO: FIX
    def _left_part(self, start_node, anchor_square_row, anchor_square_col, rack, word, limit):
        self._extend_right(start_node, anchor_square_row, anchor_square_col, rack, word)
        if limit > 0:
            for letter in rack:
                if letter in start_node.children:
                    new_node = start_node.children[letter]
                    new_rack = rack.copy()
                    new_rack.remove(letter)
                    new_word = word + letter
                    self._left_part(new_node, anchor_square_row, anchor_square_col, new_rack, new_word, limit - 1)

    # gets all words that can be made using a selected filled square and the current word rack
    # TODO: implement cross-checks to prevent overlapping nonsense words
    def get_all_words(self, start_node, square_row, square_col, rack, word):
        square_row -= 1
        square_col -= 1
        # get all words that start with the filled letter
        self._extend_right(start_node, square_row, square_col, rack, word)

        # try every letter in rack as possible anchor square
        for i, letter in enumerate(rack):
            temp_rack = rack[:i] + rack[i + 1:]
            self.board[square_row][square_col - 1].letter = letter
            self._left_part(start_node, square_row, square_col - 1, temp_rack, "", 5)


scrabble_board = ScrabbleBoard()
scrabble_board.insert_word(7, 1, "POUTED")
scrabble_board.insert_word(2, 1, "GOATS")
scrabble_board.insert_word(1, 6, "OPERATION")
scrabble_board.transpose()
scrabble_board.board[5][5].letter = "E"
scrabble_board.print_board()
scrabble_board._left_part(root, 5, 5, word_rack[1:], "", 5)
# scrabble_board.get_all_words(root, 6, 7, word_rack, "")
# for i, row in enumerate(scrabble_board.board):
#     for j, square in enumerate(row):
#         print(f"Row {i}, Column {j}, Letter {square.letter}")


out = list(sorted(scrabble_board.word_score_dict.items(), key=lambda x: x[1], reverse=True))
[print(elem) for elem in out]

for word in out:
    if not find_in_dawg(word[0], root):
        raise Exception(f"Word generation incorrect: {word[0]} not in lexicon")