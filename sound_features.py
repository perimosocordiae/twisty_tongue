# -*- coding: utf-8 -*-
"""Distinctive feature matrix for English sounds"""

# adapted from the charts at:
# http://www.slideshare.net/nahsuri/distinctive-feature-matrix-for-english-sounds
# http://hum.uchicago.edu/~jriggle/PhonChart2008.pdf
feature_matrix = {
        'p': '--+--+-------', 'b': '--++-+-------', 't': '--+----+-----',
        'd': '--++---+-----', 'k': '--+------++--', 'g': '--++-----++--',
        'f': '-++--++------', 'v': '-+++-++------', 'θ': '-++---++-----',
        'ð': '-+++--++-----', 's': '-++----+-----', 'z': '-+++---+-----',
        'ʃ': '-++----++-+--', 'ʒ': '-+++---++-+--', 'm': '+-++++-------',
        'n': '+-+++--+-----', 'ŋ': '+-+++----++--', 'l': '+-++---+-----',
        'r': '++++---+-----', 'j': '++-+----+-+--', 'w': '++-+-+---++--',
        'h': '++-----------', 'i': '++-+----+-+-+', 'ɪ': '++-+----+-+--',
        'e': '++-+----+----', 'a': '++-+----+--++', 'ɑ': '++-+-----+-++',
        'ɔ': '++-+-+---+--+', 'ʊ': '++-+-+---++--', 'u': '++-+-+---++-+',
        'ʌ': '++-+-------+-', 'ə': '++-+---------', 'o': '++-+-----+---',
        'ɛ': '++-+--------+',
        'ɝ': '++++---+----+',  # (like 'r', with +tense)
        'ɚ': '++++---+-----',  # (same as 'r')
        'ɾ': '--+----+-----',  # (same as 't')
}
feature_key = ('son','cont','cons','voice','nasal','lab','dent','cor',
               'front','back','high','low','tense')

VOWELS = r'[iɪeaɑɔʊuʌəoɜ]'

try:
    import numpy
    has_numpy = True
except ImportError:
    has_numpy = False


def feature_string(sound):
    """Get a readable representation of a sound's features"""
    return ' '.join(f + k for f, k in zip(feature_matrix[sound], feature_key))


if has_numpy:  # fast version
    numpy_feats = {k: numpy.array([c == '+' for c in v])
                   for k,v in feature_matrix.items()}

    def sound_distance(sound1, sound2):
        """Hamming distance between sound features"""
        arr1, arr2 = numpy_feats[sound1], numpy_feats[sound2]
        return (arr1 != arr2).sum()/arr1.size
else:  # slow version
    def sound_distance(sound1, sound2):
        """Hamming distance between sound features"""
        str1, str2 = feature_matrix[sound1], feature_matrix[sound2]
        num_different = sum(f1 != f2 for f1, f2 in zip(str1, str2))
        return num_different / len(feature_key)


def word_distance(word1, word2, cutoff=None):
    """my variant of Levenshtein distance"""
    len1, len2 = len(word1), len(word2)
    num_features = len(feature_key)
    if cutoff and abs(len1-len2)*num_features > cutoff:
        return cutoff+1  # we don't care about the actual value
    if len1 > len2:
        word1, word2 = word2, word1
        len1, len2 = len2, len1
    current = list(range(len1+1))
    for i in range(1,len2+1):
        previous, current = current, [i]
        for j in range(1,len1+1):
            add = previous[j] + num_features
            delete = current[j-1] + num_features
            change = previous[j-1] + sound_distance(word1[j-1],word2[i-1])
            current.append(min(add, delete, change))
    return current[-1]
