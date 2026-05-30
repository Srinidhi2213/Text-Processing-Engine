class TrieNode:
    """ A single node in the Trie. """
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0 # How often this word was inserted

class Trie:
    """
    Prefix Tree for O(L) insert/search and fast autocomplete.
    Stores a dictionary of words with insertion frequencies so autocomplete results can be ranked by popularity.
    """
    def __init__(self):
        self.root = TrieNode()
        self._word_count = 0

    def insert(self, word):
        """ Insert a word (O(L) time, O(L) space). """
        word = word.lower()
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end_of_word:
            self._word_count += 1
        node.is_end_of_word = True
        node.frequency += 1

    def search(self, word):
        """ Return True if the exact word exists in the Trie. """
        node = self._get_node(word.lower())
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix):
        """ Return True if any word starts with the given prefix. """
        return self._get_node(prefix.lower()) is not None

    def autocomplete(self, prefix, max_results=10):
        """
        Return up to 'max_results' words that begin with 'prefix',
        sorted by insertion frequency (most common first).
        Time: O(P + N) where N = nodes under prefix subtree.
        """
        prefix = prefix.lower()
        node = self._get_node(prefix)
        if node is None:
            return []

        # DFS to collect all words under this prefix node
        results = []
        self._dfs_collect(node, prefix, results)

        # Sort by frequency descending, then alphabetically
        results.sort(key=lambda x: (-x[0], x[1]))
        return [word for _, word in results[:max_results]]

    # Helpers
    def _get_node(self, prefix):
        """ Walk the trie and return the node at the end of prefix, or None. """
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _dfs_collect(self, node, current, results):
        """ DFS traversal to collect (frequency, word) pairs. """
        if node.is_end_of_word:
            results.append((node.frequency, current))
        for ch, child in node.children.items():
            self._dfs_collect(child, current + ch, results)

    @property
    def word_count(self):
        return self._word_count

    def __repr__(self):
        return f"Trie (Words = {self._word_count})"
