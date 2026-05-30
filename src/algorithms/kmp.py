class KMPMatcher:
    """ Knuth-Morris-Pratt (KMP) Pattern Matching Engine. """
    def __init__(self, pattern):
        self.pattern = pattern
        self.lps = self._build_lps(pattern)

    @staticmethod
    def _build_lps(pattern):
        """
        Build the Longest Proper Prefix-Suffix (LPS) array.
        lps[i] = length of the longest proper prefix of pattern[0..i] that is also a suffix of that substring.
        """
        m = len(pattern)
        lps = [0 for _ in range(m)]
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def search(self, text):
        """
        Find all starting indices where 'pattern' occurs in 'text.
        Returns a list of 0-based indices.
        Time: O(N + M); Space: O(M)  for the LPS array
        """
        n, m = len(text), len(self.pattern)
        if m == 0:
            return []

        indices: list[int] = []
        i = 0 # Index for text
        j = 0 # Index for pattern

        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:
                indices.append(i - j) 
                j = self.lps[j - 1]
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        return indices

    def count(self, text: str) -> int:
        return len(self.search(text))
