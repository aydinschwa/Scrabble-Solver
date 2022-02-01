from dawg import build_dawg, find_in_dawg
from string import ascii_uppercase

# english_list = open("lexicon/english_words.txt", "r").readlines()
# english_list = [word.strip("\n") for word in english_list]
# root = build_dawg(english_list)


big_list = open("lexicon/scrabble_words_complete.txt", "r").readlines()
big_list = [word.strip("\n") for word in big_list]
root = build_dawg(big_list)

word_score_dict = {}
word_rack = ["A", "R", "E", "N", "U", "T", "K"]


class Square:
    def __init__(self, letter=None):
        self.letter = letter
        self.right_neighbor = None
        self.left_neighbor = None


placed_square = Square("E")
a = Square()
b = Square()
c = Square()
d = Square()
e = Square()
f = Square()
g = Square()
h = Square()

placed_square.right_neighbor = a
a.right_neighbor = b
b.right_neighbor = c
c.right_neighbor = d
d.right_neighbor = e
e.right_neighbor = f
f.right_neighbor = g
g.right_neighbor = h


def score_word(word):
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


def extend_right(start_node, square, rack, word):
    # execute if square is empty
    if not square.letter:
        if start_node.is_terminal:
            word, score = score_word(word)
            word_score_dict[word] = score
        for letter in rack:
            if letter in start_node.children:
                new_node = start_node.children[letter]
                new_rack = rack.copy()
                new_rack.remove(letter)
                new_word = word + letter
                extend_right(new_node, square.right_neighbor, new_rack, new_word)
    else:
        if square.letter in start_node.children:
            new_node = start_node.children[square.letter]
            new_word = word + square.letter
            extend_right(new_node, square.right_neighbor, rack, new_word)


def left_part(start_node, anchor_square, rack, word, limit):
    extend_right(start_node, anchor_square, rack, word)
    if limit > 0:
        for letter in rack:
            if letter in start_node.children:
                new_node = start_node.children[letter]
                new_rack = rack.copy()
                new_rack.remove(letter)
                new_word = word + letter
                left_part(new_node, anchor_square, new_rack, new_word, limit - 1)


# As a start, this function should take an already-filled square with no neighbors and compute
# all possible words using the square and the tiles from the rack
def get_all_words(start_node, square, rack, word):
    # get all words that start with the filled letter
    extend_right(start_node, square, rack, word)

    # try every letter in rack as possible anchor square
    for i, letter in enumerate(rack):
        anchor_square = Square(letter)
        anchor_square.right_neighbor = square
        temp_rack = rack[:i] + rack[i+1:]
        left_part(start_node, anchor_square, temp_rack, "", 5)


get_all_words(root, placed_square, word_rack, "")

out = list(sorted(word_score_dict.items(), key=lambda x: x[1], reverse=True))
[print(elem) for elem in out]

for word in out:
    if not find_in_dawg(word[0], root):
        raise Exception(f"Word generation incorrect: {word[0]} not in lexicon")