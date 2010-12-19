
# Twisty Tongue #

## Dependencies ##
 * A recent-ish *nix system
 * Python 3.x
 * A 'unilex' file, somewhere in your filesystem
   * [Download it here](http://ling-alpha.wustl.edu/CompLing/unilex)

### Optional Deps ###
 * nltk (I had to port it to py3k, grab my version [here](http://dl.dropbox.com/u/11839105/install_nltk_py3k.sh))

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

