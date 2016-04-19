#!/usr/bin/python
import nltk
import sys
import getopt

from collections import Counter
from math import log

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    LM = {"malaysian" : Counter(),
          "indonesian": Counter(),
          "tamil"     : Counter()
          }

    #total_count before smoothing
    total_count = {"malaysian" : 0,
                   "indonesian": 0,
                   "tamil"     : 0
                  }
    num_4gram = {"malaysian" : 0,
                 "indonesian": 0,
                 "tamil"     : 0
                }

    with open(in_file, 'r') as f:
        #scan line by line to collect 4grams counts
        for line in f:
            label = line.split()[0]                                     #get the label
            string = rm_nonalphabet_char(line.split(' ', 1)[1].lower()) #get the actual text after the label

            fourgram = nltk.ngrams(string, 4)      #4grams
            fourgramDist = nltk.FreqDist(fourgram)
            LM[label] += fourgramDist
            # LM[label] += Counter([string[i:i+ngramL].lower() for i in range(0, len(string) - ngramL) if string[i:i+ngramL]])

        #add unseen 4grams from other languages to a specific language
        for label in LM.keys():
            other_labels  = [k for k in LM.keys() if k != label]

            for other in other_labels:
                #get all 4grams in table[other] but not in table[label] and give them value 0
                add_dict = {k: 0 for k in LM[label].keys() if not k in [other_k for other_k in LM[other].keys()]}
                #add all above 4grams to table[label]
                LM[other].update(add_dict)

        #total_count before smoothing
        total_count["malaysian"] = sum(LM["malaysian"].values())
        total_count["indonesian"] = sum(LM["indonesian"].values())
        total_count["tamil"] = sum(LM["tamil"].values())

        #number of unique 4grams in each label before smoothing
        num_4gram["malaysian"] = len(LM["malaysian"])
        num_4gram["indonesian"] = len(LM["indonesian"])
        num_4gram["tamil"] = len(LM["tamil"])

        #smoothing + 1 and convert to log base10 scale
        for label in LM.keys():
            for k in LM[label].keys():
                LM[label][k] = log(LM[label][k] + 1, 10) - log(total_count[label] + num_4gram[label], 10)

    return LM
#-------------------------------------------------------------------------------

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    infile = file(in_file, 'r')
    outfile = file(out_file, 'w')

    prob_log = {"malaysian" : 0,
                "indonesian": 0,
                "tamil"     : 0
                }

    for line in infile:
        string = rm_nonalphabet_char(line)

        #create 4grams and their counts from the test file
        fourgram = nltk.ngrams(string, 4)
        fourgramDist = nltk.FreqDist(fourgram)

        #initialise all starting logarithm-10 of probability to 0 (meaning all has 1 probability)
        prob_log['malaysian'] = prob_log['indonesian'] = prob_log['tamil'] = 0

        #loop through the generated counts and add up logarithm-10 of probability
        for k in fourgramDist:
            for label in prob_log:
                if k in LM[label]:
                    prob_log[label] += (LM[label][k] * fourgramDist[k])

        #get the label with highest logarithm-10
        predict = max(prob_log, key=prob_log.get)

        # print prob_log

        #to account for "other" language, its logarithm-10 is most likely highest
        #because the line contains very few of known 4grams.
        if prob_log[predict] >= -70:   #threshold to detect aline language = 70
            predict = "other"

        outfile.write(predict + " " + line)

    infile.close()
    outfile.close()

#-------------------------------------------------------------------------------
#this function remove non-alphabetical char except space
#then tokenise the line and rebuild the line to reduce any continuous
#space to one space
def rm_nonalphabet_char(line):
    for char in line:
        if not(char == " " or char.isalpha()):
            line = line.replace(char, " ")
    line = " ".join(line.split()) #remove coninuous space and replace with one space
    return line
#-------------------------------------------------------------------------------

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
