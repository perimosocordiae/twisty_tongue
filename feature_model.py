"""feature_model.py - Class for the feature-based tongue twister model.
CJ Carey, Fall 2010
"""
from re import sub
from random import choice
from sound_features import word_distance, VOWELS

class FeatureModel:
    """Theory-based model of tongue twisters"""
    def __init__(self, unilex):
        self.unilex = unilex
    
    def score_sentence(self, sentence):
        raise NotImplementedError("Feature-based model doesn't do sentence scoring (yet)")

    def make_twister(self, num_words, twist_type='normal'):
        """A stochastic, feature-based tongue twister generator."""
        assert twist_type == 'normal', "FeatureModel only does regular twisters for now"
        template = [None] * num_words  # possible extension: use a POS template
        twister = []
        for pos in template:
            twister.append(self.twistiest_word(twister, pos))
        return twister, [self.unilex[w].spelling for w in twister]

    def twistiest_word(self, prev_words, pos):
        if not prev_words:  # first word
            return choice(list(self.filter_words(pos, prev_words)))
        words = []
        min_nonzero = 999999 # something large
        # vowels don't tend to make very twisty words
        last_word = sub(VOWELS,'',prev_words[-1])
        for w in self.filter_words(pos, prev_words):
            d = word_distance(sub(VOWELS,'',w),last_word,min_nonzero)
            if 0 < d < min_nonzero:
                min_nonzero = d
                words = [w]
            elif d == min_nonzero:
                words.append(w)
        return choice(words)
    
    def filter_words(self, pos, blacklist):
        if not pos:
            constraints = lambda w: w not in blacklist and len(w) < 8
        else:
            constraints = lambda w: (w not in blacklist and len(w) < 8 and
                                    pos in self.unilex[w].pos)
        return filter(constraints,self.unilex.keys())
