Your task for this assignment is to create a Hidden Markov Model (HMM) for POS tagging, including：

- Training probability tables (i.e., initial, transition and emission) for HMM from training files containing text-tag pairs
- Performing inference with your trained HMM to predict appropriate POS tags for untagged text. 

You can run the POS tagger by typing the following at a command line:

$ python3 tagger.py -d <training files> -t <test file> -o <output file>
