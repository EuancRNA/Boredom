
from itertools import permutations
import pandas as pd
import numpy as np
import sys

# Convert string of letters to a list and find all possible permutations
letters = sys.argv[1].lower() # String of letters as input
input_letters = list(letters)

# Count number of occurances of each letter
def CountChar(string):
    dictionary = dict()
    for char in string:
        dictionary[char] = string.count(char)
    return dictionary


# Get all possible unique permutations of input letters
letter_permuts = list()
idx_letters = len(input_letters)+1
for i in range(0,idx_letters):
    for j in range(0,idx_letters):
        if (i != j and i < j):
            letter_permuts = letter_permuts + \
                [''.join(p) for p in permutations(input_letters[i:j])]

letter_permuts = set(letter_permuts)


# Read in dictionary of all english words as a set
def LoadFile(filename):
    with open(filename) as word_file:
        valid_words = set(word_file.read().split("\n"))
    return valid_words

word_set = LoadFile('words_alpha.txt')


# Identify actual words in the set of all possible letter permutations
possible_words = [ word for word in letter_permuts if word in word_set ]
# Count number of occurances of each letter in string and possible words
# and remove words shorter than 2 letters
letter_count = CountChar(input_letters)
possible_count = [ CountChar(word) for word in possible_words \
                                                    if len(word) > 1 ]
possible_count = possible_count[0:-1]
# Check and remove words with duplicates of letters in (ie if extra a's)
for char in letter_count:
    for word in possible_count:
        if char in word.keys() and \
           word[char] != letter_count[char]:
            del(word)

# Get list of lists of letters and list of possible words
possible_lists = [ list(word.keys()) for word in possible_count ]
possible_words = [ "".join(word) for word in possible_count ]


# Read in the scrabble tile scores, index as letters, 1st col as score
scrabble_scores = pd.read_csv("scrabble_tile_values.txt",
                                  sep="\t",header=None,index_col=0)
scrabble_scores.index = scrabble_scores.index.str.lower()
scrabble_scores.columns = ['SCORE']
# Create a dataframe of 0s of height #letters, width #words
blank_cols = pd.DataFrame(0, index=np.arange(len(scrabble_scores)),
                             columns=possible_words)
# Get dictionary of index number : letter for use as colnames
idx_names=dict(zip(list(range(0,len(scrabble_scores))),
                   list(scrabble_scores.index)))
blank_cols = blank_cols.rename(index=idx_names)
# Join columns together
scrabble_scores = pd.concat([scrabble_scores,blank_cols], axis=1)


# Iterate over rows and cols and append value of SCORE to the respective
# element (col,row) that corresponds to the word and letter
for index, row in scrabble_scores.iterrows():
    for (colname, coldata) in scrabble_scores.iteritems():
        if (str(index) in str(colname)):
            scrabble_scores.loc[[index],colname] = row.loc["SCORE"]

# Calculate colsums for total word score and format the output
word_scores = scrabble_scores.sum(axis=0)
word_scores = word_scores.to_frame().iloc[1:len(word_scores)]
word_scores = word_scores.sort_values(by=0, ascending=[False])

# Print the output in descending score
print("\n\nWORD\tSCORE\n")
for index, row in word_scores.iterrows():
    print(index, "\t", int(row))
print("\n")
