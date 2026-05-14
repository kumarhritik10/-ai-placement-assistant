"""
auto_correct.py
---------------
Enhanced Norvig Probabilistic Spell-Corrector
with College Placement Vocabulary Awareness.

Algorithm (Peter Norvig, 2007):
  P(word)      = freq(word) / total_words   -- unigram language model
  candidates() = known words within edit-distance 1 or 2
  correction() = argmax P(candidate)

Enhancements:
  1. Placement vocab injected with high frequency so domain
     terms (CTC, LPA, ReactJS, etc.) are never mis-corrected.
  2. Auto-downloads big.txt corpus if missing (one-time ~6 MB).
  3. correct_with_diff() returns per-word change metadata for UI.
  4. get_spelling_score() returns a 0-100 accuracy metric.
"""

import re
import os
import urllib.request
from collections import Counter
from dataclasses import dataclass, field

_DIR        = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(_DIR, "big.txt")
CORPUS_URL  = "https://norvig.com/big.txt"


def _ensure_corpus() -> None:
    """Download the Norvig corpus if it is not already present (~6 MB)."""
    if not os.path.exists(CORPUS_PATH):
        urllib.request.urlretrieve(CORPUS_URL, CORPUS_PATH)


def _tokenize(text: str) -> list:
    return re.findall(r"\w+", text.lower())


_ensure_corpus()

with open(CORPUS_PATH, encoding="utf-8") as _f:
    WORDS: Counter = Counter(_tokenize(_f.read()))

# Inject placement vocabulary with very high frequency — never mis-corrected
try:
    from placement_vocab import PLACEMENT_WORDS as _PV
    for _w in _PV:
        WORDS[_w.lower()] += 200_000
except ImportError:
    pass

_N = sum(WORDS.values())


# ---------------------------------------------------------------------------
# Core Norvig Functions
# ---------------------------------------------------------------------------

def prob(word: str) -> float:
    """Unigram probability P(word)."""
    return WORDS[word.lower()] / _N


def known(word_set) -> set:
    """Return the subset of words that appear in the corpus."""
    return {w for w in word_set if w.lower() in WORDS}


def edits1(word: str) -> set:
    """All strings within edit-distance 1."""
    letters    = "abcdefghijklmnopqrstuvwxyz"
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:]                for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]            for L, R in splits if R for c in letters]
    inserts    = [L + c + R                for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word: str) -> set:
    """All strings within edit-distance 2."""
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}


def candidates(word: str) -> set:
    """Generate the best set of correction candidates."""
    return (
        known([word])
        or known(edits1(word))
        or known(edits2(word))
        or {word}
    )


def correction(word: str) -> str:
    """Return the most probable spelling correction for a single word."""
    # 1. If it contains a number, don't correct (e.g. "B2B", "O2")
    if any(c.isdigit() for c in word):
        return word
        
    # 2. If it is entirely uppercase and > 1 character, don't correct (Acronyms like HTML, PHP)
    if word.isupper() and len(word) > 1:
        return word
        
    # 3. If it has mixed case inside the word, don't correct (e.g. OpenCV, ReactJS)
    if len(word) > 1 and any(c.isupper() for c in word[1:]):
        return word

    # 4. Standard Norvig correction on lowercase
    best = max(candidates(word.lower()), key=prob)
    
    # 5. Restore original capitalization
    if word.istitle():
        return best.capitalize()
    elif word.isupper():
        return best.upper()
    return best


# ---------------------------------------------------------------------------
# Sentence-Level Functions
# ---------------------------------------------------------------------------

def correct_sentence(sentence: str) -> str:
    """Correct all words in a sentence and return the corrected string."""
    return " ".join(correction(w) for w in sentence.split())


@dataclass
class WordChange:
    """Holds metadata about a single token and whether it was corrected."""
    original:  str
    corrected: str
    changed:   bool = field(init=False)

    def __post_init__(self):
        self.changed = self.original.lower() != self.corrected.lower()


def correct_with_diff(sentence: str):
    """
    Correct a sentence and return a word-level diff.

    Returns:
        corrected_sentence : str
        changes            : list[WordChange]
    """
    changes      = []
    output_words = []

    for token in sentence.split():
        # Separate leading/trailing punctuation from the alphabetic core
        prefix, suffix, stripped = "", "", token
        while stripped and not stripped[0].isalpha():
            prefix  += stripped[0]
            stripped = stripped[1:]
        while stripped and not stripped[-1].isalpha():
            suffix   = stripped[-1] + suffix
            stripped = stripped[:-1]

        if stripped:
            fixed = correction(stripped)
            changes.append(WordChange(original=stripped, corrected=fixed))
            output_words.append(prefix + fixed + suffix)
        else:
            changes.append(WordChange(original=token, corrected=token))
            output_words.append(token)

    return " ".join(output_words), changes


def get_spelling_score(sentence: str) -> int:
    """Return 0-100 spelling accuracy score. 100 = no errors detected."""
    tokens = sentence.split()
    if not tokens:
        return 100
    _, changes = correct_with_diff(sentence)
    errors = sum(1 for c in changes if c.changed)
    return max(0, round(100 * (1 - errors / len(tokens))))
