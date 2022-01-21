from dawg import build_dawg, find_in_dawg
from string import ascii_uppercase
# first just define a function that creates valid words from a rack of tiles and a starting letter

big_list = open("lexicon/scrabble_words_complete.txt", "r").readlines()
big_list = [word.strip("\n") for word in big_list]
root = build_dawg(big_list)

word_score_dict = {}
word_rack = ["S", "N", "E", "D", "K", "C", "R"]


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


def get_valid_right_words(start, rack, word):
    if start.is_terminal:
        word, score = score_word(word)
        word_score_dict[word] = score
    for letter in rack:
        if letter in start.children:
            new_node = start.children[letter]
            new_rack = rack.copy()
            new_rack.remove(letter)
            new_word = word + letter
            get_valid_right_words(new_node, new_rack, new_word)


for letter in ascii_uppercase:
    start_node = root.children[letter]
    get_valid_right_words(start_node, word_rack, letter)

print(list(sorted(word_score_dict.items(), key=lambda x: x[1], reverse=True)))
