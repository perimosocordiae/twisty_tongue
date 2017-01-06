#!/usr/bin/env python3
"""tongue_twister.py - An empirically-derived tongue twister generator.
CJ Carey, Fall 2010
"""
from __future__ import print_function
from re import sub
from sys import stderr, stdin
from pickle import load
from os.path import basename
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from subprocess import Popen, PIPE
from collections import namedtuple

from markov_model import MarkovModel
from random_model import RandomModel
from feature_model import FeatureModel


def load_pronunciation_markov(fname):
    NON_IPA = '[<>{}ˈˌ$%s-]' % chr(809)  # nasty unicode
    w2p, p2w = {}, {}
    for line in open(fname):
        parts = line.split(':')
        word = parts[0]
        sylls = tuple(sub(NON_IPA, '', parts[3]).split('.'))
        w2p[word] = sylls
        p2w[sylls] = word
    return w2p, p2w


def load_pronunciation_feature(fname):
    Word = namedtuple('Word', ('spelling','pos'))
    unilex = {}
    NON_IPA = '[<>{}ˈˌ$%s.-]' % chr(809)  # nasty unicode
    for line in open(fname):
        parts = line.split(':')
        spell = parts[0]
        pos, pron = parts[2:4]
        pron = sub(NON_IPA, '', pron)
        unilex[pron] = Word(spell, pos.split('/'))
    return unilex


def main(opts):
    if opts.random:
        print('Loading dictionary...', file=stderr)
        pronunc_dict = load_pronunciation_feature(opts.pronounce)
        model = RandomModel(pronunc_dict)
    elif opts.model:
        print('Loading cached model...', file=stderr)
        model = load(open(opts.model, 'rb'))
    elif opts.corpus:
        print('Loading dictionary...', file=stderr)
        spell2sylls, sylls2spell = load_pronunciation_markov(opts.pronounce)
        print('Training model...', file=stderr)
        name = '_'.join((basename(opts.corpus), str(opts.training_size)))
        model = MarkovModel(opts.corpus, opts.training_size,
                            spell2sylls, sylls2spell)
        print('Dumping {}.pyz for later use'.format(name), file=stderr)
        model.save(name+'.pyz')
    else:
        print('Loading dictionary...', file=stderr)
        pronunc_dict = load_pronunciation_feature(opts.pronounce)
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


def locate_unilex():
    out,_ = Popen('locate unilex', shell=True, stdout=PIPE).communicate()
    paths = [p for p in out.decode().splitlines() if basename(p) == 'unilex']
    if not paths:
        print("Error: couldn't locate unilex", file=stderr)
        exit(-1)
    return paths[0]


def parse_opts():
    ap = ArgumentParser(description=__doc__,
                        formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument('-c', '--corpus', help='Text to train on')
    ap.add_argument('-m', '--model', help='Pre-trained model')
    ap.add_argument('-p', '--pronounce',
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
    if not opts.pronounce and not opts.model:
        opts.pronounce = locate_unilex()
    if opts.training_size < 0:  # use all of the corpus
        opts.training_size = None
    if opts.num_twisters < 0:
        ap.error('Must provide a number of twisters > 0')
    return opts

if __name__ == '__main__':
    main(parse_opts())
