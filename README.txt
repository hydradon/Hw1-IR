This is the README file for A0099878W's submission

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

The script consists of two main functions: build_LM and test_LM:

- build_LM(...) takes input.train.txt and reads line by line. At the start,
an empty language model LM is initialised together with 2 dictionaries. One is
total_count that contains the sum of counts of occurences of all 4grams before
smoothing. The other is num_4gram that contains number of unique 4grams (both
seen and unseen in a language). Reading each line, the script first separates 
the label and then ngram-izes the actual string following the label into 4gram 
using ngrams and FreqDist functions of nltk library. Then, the script loop 
through the LM dictionary to find all 4grams that are unique in a
specific language and add them to the other 2 languages. Finally, smoothing+1
is applied to all 4grams and probability is calculated and converted to
logarithm base-10 scale because the probability is very small which could result
in 0 probability during testing.

- test_LM(...) takes input.test.txt file to test and outputs prediction to
input.predict.txt. An initial dictionary containing probability in logarithm 
base-10 result for each language is initialised to 0. Similar to build_LM, 
each line of input is ngram-ized. Then the script loops through LM to find the
logarithm value of each 4grams and add together for each language. Finally,
the language with the highest log value will be the prediction. To account for
"alien" language, it is observed that "alien" language will have very few known
4grams in it. Therefore, a threshold is set and above which, the prediction will
be "other". In this case, the threshold is set to -70.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

1. build_test_LM.py : contains the main script of the algorithm
2. eval.py : contains the script that evaluate accuracy of prediction of
test data
3. ESSAY.txt : answers to essay questions
4. input.train.txt : 898 lines of training data with correct label
5. input.test.txt : 20 lines of test data with no label
6. input.predict.txt : 20 lines of test data with predicted label
7. input.correct.txt : 20 lines of test data with correct label
8. README.txt : description of the program

== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0000000X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
