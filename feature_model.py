"""feature_model.py - Class for the feature-based tongue twister model.
CJ Carey, Fall 2010
"""
from random import choice

from sound_features import word_distance, VOWELS


class FeatureModel:
    """Theory-based model of tongue twisters"""
    def __init__(self, unilex):
        self.unilex = unilex

    def score_sentence(self, sentence):
        raise NotImplementedError(
            "Feature-based model doesn't do sentence scoring (yet)")

    def make_twister(self, num_words, twist_type='normal'):
        """A stochastic, feature-based tongue twister generator."""
        if twist_type != 'normal':
            raise ValueError("FeatureModel only does regular twisters for now")
        template = [None] * num_words  # possible extension: use a POS template
        twister = []
        for pos in template:
            twister.append(self.twistiest_word(twister, pos))
        return twister, [self.unilex[w].spelling for w in twister]

    def twistiest_word(self, prev_words, pos):
        if not prev_words:  # first word
            words = list(self.filter_words(pos, prev_words))
        else:
            words = []
            min_nonzero = float('inf')
            # vowels don't tend to make very twisty words
            last_word = VOWELS.sub('', ''.join(prev_words[-1]))
            for w in self.filter_words(pos, prev_words):
                this_word = VOWELS.sub('', ''.join(w))
                d = word_distance(this_word, last_word, min_nonzero)
                if 0 < d < min_nonzero:
                    min_nonzero = d
                    words = [w]
                elif d == min_nonzero:
                    words.append(w)
        return choice(words)

    def filter_words(self, pos, blacklist):
        words = (w for w in self.unilex if len(w) < 8 and w not in blacklist)
        if pos:
            words = (w for w in words if pos in self.unilex[w].pos)
        return words
