#!/usr/bin/env python3
"""tongue_twister.py - An empirically-derived tongue twister generator.
CJ Carey, Fall 2010
"""
from __future__ import print_function
import os
import re
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections import namedtuple
from pickle import load
from sys import stderr, stdin

from feature_model import FeatureModel
from markov_model import MarkovModel
from random_model import RandomModel


def main(opts):
    if opts.model:
        print('Loading cached model...', file=stderr)
        model = load(open(opts.model, 'rb'))
    else:
        print('Loading dictionary...', file=stderr)
        pronunc_dict = load_unilex(opts.pronounce)
        if opts.random:
            model = RandomModel(pronunc_dict)
        elif opts.corpus:
            print('Training markov model...', file=stderr)
            model = MarkovModel(opts.corpus, opts.training_size, pronunc_dict)
            fname = '%s_%s.pyz' % (os.path.basename(opts.corpus),
                                   opts.training_size)
            print('Dumping', fname, 'for later use', file=stderr)
            model.save(fname)
        else:
            model = FeatureModel(pronunc_dict)

    if opts.score:
        print('Scoring sentences from stdin...', file=stderr)
        print('(note: first one takes longer than the rest)', file=stderr)
        try:
            for line in stdin:
                print_score(model, line)
        except (KeyboardInterrupt, EOFError):
            print('Cleaning up...', file=stderr)
    else:
        print('Making {:d} twisters...'.format(opts.num_twisters), file=stderr)
        twist_type = 'reverse' if opts.reverse_twist else 'normal'
        for _ in range(opts.num_twisters):
            print_twister(model, opts.words_per_twister, twist_type)


def load_unilex(fname):
    Word = namedtuple('Word', ('spelling', 'pos'))
    NON_IPA = re.compile('[<>{}ˈˌ$%s-]' % chr(809))
    unilex = {}
    for line in open(fname):
        parts = line.split(':')
        pron = tuple(NON_IPA.sub('', parts[3]).split('.'))
        unilex[pron] = Word(spelling=parts[0], pos=parts[2].split('/'))
    return unilex


def print_score(model, line):
    try:
        score = model.score_sentence(line)
        print(line.strip(), '=>', score)
    except KeyError as e:
        print('Unknown word:',e.args[0])


def print_twister(model, num_words, twist_type):
    phons, words = model.make_twister(num_words, twist_type)
    print(*words, end=' ==> ')
    print(' '.join(''.join(p) for p in phons))


def parse_opts():
    unilex_path = os.path.join(os.path.dirname(__file__), 'unilex')
    ap = ArgumentParser(description=__doc__,
                        formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument('-c', '--corpus', help='Text to train on')
    ap.add_argument('-m', '--model', help='Pre-trained model')
    ap.add_argument('-p', '--pronounce', default=unilex_path,
                    help='Spelling/pronunciation dictionary')
    ap.add_argument('-t', '--training-size', type=int, default=10000,
                    help=('Number of words from the corpus to train on,'
                          ' -1 -> all words'))
    ap.add_argument('-n', '--num-twisters', type=int, default=5,
                    help='Number of tongue twisters to output')
    ap.add_argument('-w', '--words-per-twister', type=int, default=2,
                    help='Number of words per generated twister')
    ap.add_argument('-r', '--reverse-twist', action='store_true',
                    help='Generate especially non-twisty phrases')
    ap.add_argument('-R', '--random', action='store_true',
                    help='Generate phrases at random (for testing)')
    ap.add_argument('-s', '--score', action='store_true',
                    help='Use the model to score sentences from stdin')
    opts = ap.parse_args()
    if opts.training_size < 0:  # use the whole corpus
        opts.training_size = None
    if opts.num_twisters < 0:
        ap.error('Must provide a number of twisters > 0')
    return opts

if __name__ == '__main__':
    main(parse_opts())
