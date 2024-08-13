class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.response = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, keyword, response):
        node = self.root
        for char in keyword:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.response = response

    def search(self, text):
        found_responses = []
        length = len(text)
        for start in range(length):
            node = self.root
            for end in range(start, length):
                char = text[end]
                if char not in node.children:
                    break
                node = node.children[char]
                if node.is_end_of_word:
                    found_responses.append(node.response)
        return found_responses
