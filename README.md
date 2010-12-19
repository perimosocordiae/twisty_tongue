
# Twisty Tongue #

## Dependencies ##
 * A recent-ish *nix system
 * Python 3.x
 * A 'unilex' file, somewhere in your filesystem

### Optional Deps ###
 * numpy
 * nltk (I had to port it to py3k, grab my version here)

## Usage ##
 * `./tongue_twister.py -h` -- Shows the help
 * `./tongue_twister.py` -- Uses all defaults to generate tongue twisters with the feature-based model.
 * `./tongue_twister.py -c brown` -- Uses the brown corpus to train the Markov model, then generates tongue twisters *Note: Requires NLTK*

## Analysis ##
This project presents two models for constructing tongue twisters.
