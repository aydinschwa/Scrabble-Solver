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


# Define a node to be stored in DAWG
class Node:
    next_id = 0

    def __init__(self):
        self.is_terminal = False
        self.id = Node.next_id
        Node.next_id += 1
        self.children = {}

    def __str__(self):
        out = [f"Node {self.id}\nChildren:\n"]
        letter_child_dict = self.children.items()
        for letter, child in letter_child_dict:
            out.append(f" {letter} -> {child.id}\n")
        return " ".join(out)


# returns length of common prefix
def length_common_prefix(prev_word, word):
    shared_prefix_length = 0
    for letter1, letter2 in (zip(prev_word, word)):
        if letter1 == letter2:
            shared_prefix_length += 1
        else:
            return shared_prefix_length
    return shared_prefix_length


# minimization function
def minimize(curr_node, num_steps, minimized_nodes, non_minimized_nodes):

    for _ in range(num_steps):

        # TODO: make less ugly
        if not non_minimized_nodes:
            break

        parent, letter, child = non_minimized_nodes.pop()

        duplicate_node = False
        for node in minimized_nodes:
            if (child.is_terminal == node.is_terminal) and (child.children == node.children):
                parent.children[letter] = child
                duplicate_node = True
                break

        if not duplicate_node:
            minimized_nodes.append(child)

        curr_node = parent

    return curr_node


def build_dawg(lexicon):
    minimized_nodes = []
    non_minimized_nodes = []
    root = Node()
    curr_node = root
    prev_word = ""
    for word in lexicon:

        # get common prefix of new word and previous word
        common_prefix_length = length_common_prefix(prev_word, word)

        # backtrack n times where n is difference between length of word and length of common prefix
        to_backtrack = len(word) - common_prefix_length

        # minimization step
        if non_minimized_nodes:
            curr_node = minimize(curr_node, to_backtrack, minimized_nodes, non_minimized_nodes)

        # adding new nodes after the common prefix
        for letter in word[common_prefix_length:]:
            next_node = Node()
            curr_node.children[letter] = next_node
            non_minimized_nodes.append((curr_node, letter, next_node))
            curr_node = next_node

        # by the end of this process, curr_node should always be a terminal node
        curr_node.is_terminal = True
        prev_word = word

    [print(node) for node in minimized_nodes]
    print(root)
    return root


build_dawg(word_list)
