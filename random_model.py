from random import choice


class RandomModel:
    def __init__(self, unilex):
        self.unilex = unilex

    def make_twister(self, num_words, twist_type='normal'):
        all_words = list(self.unilex.keys())
        twister = [choice(all_words) for _ in range(num_words)]
        return twister, [self.unilex[w].spelling for w in twister]

    def score_sentence(self, sentence):
        raise NotImplementedError("Random model doesn't do sentence scoring")
