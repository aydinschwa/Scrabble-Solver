word_list = open("lexicon/test_lexicon", "r").readlines()
word_list = [word.strip("\n") for word in word_list]


# first just define a trie data structure
def build_trie(lexicon):
    trie = {0: {}}
    next_node = 1
    for word in lexicon:
        curr_node = 0
        for let in word:
            # if letter is present, move down its edge to next node
            if let in trie[curr_node]:
                edge_dict = trie[curr_node]
                curr_node = edge_dict[let]
            # otherwise, create new node and store its edge in current node
            # then move to it
            else:
                trie[next_node] = {}
                trie[curr_node][let] = next_node
                curr_node = next_node
                next_node += 1
        trie[curr_node]["END"] = True

    return trie


# function to check validity if word is in trie
def check_valid(word, trie):
    curr_node = 0
    for letter in word:
        if letter in trie[curr_node]:
            curr_node = trie[curr_node][letter]
        else:
            return False
    if "END" in trie[curr_node]:
        return True
    else:
        return False


def build_dawg(lexicon):
    dawg = {0: {}}
    next_node = 1
    for word in lexicon:
        curr_node = 0
        for i, letter in enumerate(word):
            # if letter is present, move down its edge to next node
            if letter in dawg[curr_node]:
                edge_dict = dawg[curr_node]
                curr_node = edge_dict[letter]

            # see if next letter is already present in the dawg and create edge to that node
            else:
                found = False
                num_edges = len(dawg[curr_node].values())
                # only check if not on the last letter and node has edges
                if (i != len(word) - 1) and (num_edges > 0):
                    next_letter = word[i + 1]
                    child_nodes = list(dawg[curr_node].values())
                    for node in child_nodes:
                        if next_letter in dawg[node]:
                            dawg[curr_node][letter] = node
                            curr_node = node
                            found = True
                            break
                if not found:
                    # if next letter is not in the edges of child nodes, then create new node and store
                    # its edge in current node
                    dawg[next_node] = {}
                    dawg[curr_node][letter] = next_node
                    curr_node = next_node
                    next_node += 1

        dawg[curr_node]["END"] = True

    return dawg


print(build_dawg(word_list[::-1]))
print(build_trie(word_list))