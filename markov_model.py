"""markov_model.py - Class and helpers for the Markov tongue twister model.
CJ Carey, Fall 2010
"""

from pickle import dump
from random import choice
from itertools import chain, islice, tee
from collections import deque, Counter, defaultdict

STREAM_BREAK = 0xDEAD

choosers = {
    'normal':  lambda model, prefix: model.most_likely_next(prefix),
    'reverse': lambda model, prefix: model.least_likely_next(prefix),
    'random':  lambda model, prefix: model.random()
}


class MarkovModel:
    """Empirical model of tongue twisters, based on a corpus of 'normal text'
    and pair of mappings: spelling <-> syllable pronunciations"""

    def __init__(self, corpus_name, num_words, unilex):
        self.spell2sylls = {}
        self.sylls2spell = {}
        for sylls, word in unilex.items():
            self.spell2sylls[word.spelling] = sylls
            self.sylls2spell[sylls] = word.spelling
        # set up markov chains of length two: only considers the last element
        self.sylls = MarkovChain(2)
        self.chars = MarkovChain(2)
        # fill the markov chains
        for word in load_corpus(corpus_name, num_words):
            if word not in self.spell2sylls:
                self.sylls.add(STREAM_BREAK)
                self.chars.add(STREAM_BREAK)
            else:
                for syl in self.spell2sylls[word]:
                    self.sylls.add(syl)
                    for char in syl:
                        self.chars.add(char)

    def make_twister(self, num_words, twist_type='normal'):
        """A stochastic tongue twister generator. Makes greedy word choices,
        based on the frequency data in the model."""
        all_words = list(self.sylls2spell.keys())
        twister = [choice(all_words)]  # any one will do to start
        chooser = choosers[twist_type]
        for _ in range(num_words-1):
            prefix = twister[-1]  # we only care about the last word
            word_choices = self._word_choices(chooser, prefix, all_words)
            twister.append(choice(word_choices))
        return twister, map(self.sylls2spell.__getitem__, twister)

    def _word_choices(self, chooser, prefix, all_words):
        next_syll = chooser(self.sylls, prefix)
        if next_syll:
            return [w for w in all_words if w[0] == next_syll]
        next_sound = chooser(self.chars, prefix)
        if next_sound:
            return [w for w in all_words if w[0][0] == next_sound]
        return all_words

    def score_sentence(self, sentence):
        """An attempt to assign 'twistiness' scores to a sentence.
        Uses the empirical frequency data, but is largely arbitrary"""
        from nltk import word_tokenize  # import only on demand, takes forever
        parts = list(chain.from_iterable(self.spell2sylls[w.lower()]
                                         for w in word_tokenize(sentence)))
        syll_score, count = 0, 0
        for prefix, x in pairwise(parts):
            syll_score += (self.sylls.likelihood(prefix, x) or 0)
            count += 1
        if count > 0:
            syll_score /= count

        char_score, count = 0, 0
        for prefix, x in pairwise(chain.from_iterable(parts)):
            char_score += (self.chars.likelihood(prefix, x) or 0)
            count += 1
        if count > 0:
            char_score /= count

        return syll_score + (char_score / 10)

    def save(self, fname):
        """Serialize this model as a pickle, in a file called 'fname'"""
        with open(fname, 'wb') as modelcache:
            dump(self, modelcache, -1)


class MarkovChain:
    """Generic class for contructing Markov Chains of strings"""

    def __init__(self, kmer_len):
        self.buf = deque(maxlen=kmer_len)
        self.freqs = defaultdict(Counter)

    def add(self, x):
        if x == STREAM_BREAK:
            self.buf.clear()
        else:
            if len(self.buf) == self.buf.maxlen:
                self.buf.popleft()  # shuffle one out
                prefix = '|'.join(self.buf)
                self.freqs[prefix][x] += 1
            self.buf.append(x)

    def __get_freqs_for(self, prefix):
        if len(prefix) + 1 < self.buf.maxlen:
            return
        return self.freqs['|'.join(prefix[-self.buf.maxlen+1:])]

    def random(self):
        return choice(list(self.freqs.keys()))

    def least_likely_next(self, prefix):
        freqs = self.__get_freqs_for(prefix)
        if freqs:
            return min(freqs, key=freqs.__getitem__)

    def most_likely_next(self, prefix):
        freqs = self.__get_freqs_for(prefix)
        if freqs:
            return max(freqs, key=freqs.__getitem__)

    def likelihood(self, prefix, x):
        freqs = self.__get_freqs_for(prefix)
        if freqs:
            return float(freqs[x]) / sum(c for c in freqs.values())

    def __len__(self):
        return self.buf.maxlen


def pairwise(seq):
    """Taken from the itertools recipes page.
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(seq)
    next(b, None)
    return zip(a, b)


def load_corpus(corpus_name, num_words=None):
    """Load a corpus from the NLTK sets"""
    # import here, because it takes forever
    from nltk import corpus, download
    download(corpus_name)
    wordstream = getattr(corpus, corpus_name).words
    if num_words:
        return islice(wordstream(), num_words)
    return wordstream()
