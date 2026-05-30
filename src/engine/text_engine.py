import re
import os
from src.algorithms.trie import Trie
from src.algorithms.kmp import KMPMatcher
from src.algorithms.levenshtein import LevenshteinCorrector

class TextProcessingEngine:
    """
    High-level structure:
    - Trie: Prefix autocomplete.
    - KMP: Pattern matching inside file content.
    - Levenshtein DP: Spell correction.
    """
    def __init__(self):
        self._trie = Trie()
        self._corrector = LevenshteinCorrector(self._trie)
        self._file_cache = {}

    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().replace('\n', ' ')

    def load_text(self, text, source_name="<memory>"):
        words = re.findall(r"[a-zA-Z']+", text)
        for w in words:
            self._trie.insert(w.lower())
        self._corrector._vocab = list(set(
            self._corrector._vocab + [w.lower() for w in words]
        ))
        self._file_cache[source_name] = text

    def autocomplete(self, prefix, max_results=10):
        return self._trie.autocomplete(prefix, max_results)

    def pattern_search(self, pattern, case_sensitive=False, naive=False):
        if not case_sensitive:
            pattern = pattern.lower()

        if naive:
            pass

        matcher = KMPMatcher(pattern)
        results = {}
        for fpath, content in self._file_cache.items():
            text = content if case_sensitive else content.lower()
            hits = matcher.search(text)
            if hits:
                results[os.path.basename(fpath)] = hits

        return results

    def correct(self, word, max_distance=2, max_suggestions=5):
        if self._trie.search(word.lower()):
            return []
        return self._corrector.suggest(word, max_distance, max_suggestions)
