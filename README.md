
# Twisty Tongue #

## Dependencies ##
 * Python 3.4+
 * A 'unilex' file, somewhere in your filesystem
   * [Download it here](http://ling-alpha.wustl.edu/CompLing/unilex)

### Optional Deps ###
 * nltk
 * numpy

## Usage ##
 * `./tongue_twister.py -h` -- Shows the help.
 * `./tongue_twister.py` -- Uses all defaults to generate tongue twisters with the feature-based model.
 * `./tongue_twister.py -c brown` -- Uses the brown corpus to train the Markov model, then generates tongue twisters. *Note: Requires NLTK*
 * `./tongue_twister.py -R` -- Generates "tongue twisters" by selecting words at random.

## Analysis ##

This project presents two models for constructing tongue twisters.

The first is completely emiprical,
building a model of word succession frequencies using Markov chains.
This data is used to approxmate the likelihood of a word,
given the word that came before it.
The model then constructs tongue twisters by taking a random first word,
then selecting the *least* likely next word each time.
The main idea is that word sequences that are easy to say will appear more
frequently the corpus, which would make the least likely word sequence the
best choice for a tongue twister.

The second approach uses phonology to define a word <-> word distance metric,
then chooses tongue twisters by selecting words with the smallest (non-zero)
distance from the previous word.
The distance metric is a variation of Levenshtein's edit distance algorithm,
using sound <-> sound distance as the edit cost.
Distances between sounds can be calculated as the Hamming distance between
the sounds' binary feature vectors.
These metrics allow comparison of words at a phonetic level.
Since tongue twisters tend to rely on the confusion associated with pronouncing
similar-yet-different words rapidly, the model selects a sequence of words with minute phonological changes between successive words.

I didn't create an objective way to determine the quality of tongue
twisters, but eyeballing the results of both models shows that the feature-based
model is much more effective.  In fact, the Markov model's results are only
marginally better than word sequences generated at random.  I think this stems
from an issue of undersampling.  The model will avoid choosing commonly used
bigrams, but the task of selecting the *least* likely bigram requires a much
denser sample.  Given how large this space is, it seems that an empirical model
like this one may be infeasible.

## Future Work ##
The framework provided here allows experimentation with a wide array of
generator models and techniques.  Some improvements/additions could be:

 * Using a grammar to generate syntactically valid tongue twisters.
 * Applying a non-uniform weight to sounds when calculating word distances.
   * For example, one could weight the initial consonant higher than the others,
   to produce more alliterative tongue twisters.
 * Using a corpus of sample tongue twisters, then selecting the most likely bigrams.
   * This approach will probably suffer from undersampling as well.
 * Using an A,B,A',B' model (where A and A', B and B' are "twisty" bigrams).
