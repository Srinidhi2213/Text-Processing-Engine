import heapq

class LevenshteinCorrector:
    """
    Spell corrector using Levenshtein (edit) distance.
    Suggests the closest words from a vocabulary.
    """
    def __init__(self, trie):
        self._trie = trie
        self._vocab = []

    def build_vocab(self, words):
        """ Populate both the Trie and the flat vocab list. """
        for word in words:
            w = word.lower()
            self._trie.insert(w)
            self._vocab.append(w)

    @staticmethod
    def distance(s1, s2):
        """
        Compute the Levenshtein edit distance between s1 and s2.
        Space-optimised to O(min(|s1|, |s2|)) using two rolling rows.
        """
        # Ensure s1 is the shorter string for space optimisation
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        m, n = len(s1), len(s2)
        prev = list(range(m + 1))

        for j in range(1, n + 1):
            curr = [j] + [0] * m
            for i in range(1, m + 1):
                if s1[i - 1] == s2[j - 1]:
                    curr[i] = prev[i - 1] # No operation
                else:
                    curr[i] = 1 + min([
                        prev[i],        # Delete  from s2
                        curr[i - 1],    # Insert  into s2
                        prev[i - 1]     # Replace in s2
                    ])
            prev = curr

        return prev[m]

    @staticmethod
    def full_matrix(s1, s2):
        """
        Return the full DP matrix.
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min([dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]])
        return dp

    def suggest(self, word, max_distance=2, max_suggestions=5):
        """
        Return up to 'max_suggestions' words from vocabulary sorted by edit distance from 'word'.  
        Only words within 'max_distance' are returned.

        Uses a min-heap to keep only the top-k suggestions efficiently.
        Time: O(V × L) where V = vocab size, L = average word length.
        """
        word = word.lower()

        # If exact match exists, no correction needed
        if self._trie.search(word):
            return [(word, 0)]

        heap = []
        for candidate in self._vocab:
            dist = self.distance(word, candidate)
            if dist <= max_distance:
                heapq.heappush(heap, (dist, candidate))

        results = []
        while heap and len(results) < max_suggestions:
            dist, candidate = heapq.heappop(heap)
            results.append((candidate, dist))

        return results
