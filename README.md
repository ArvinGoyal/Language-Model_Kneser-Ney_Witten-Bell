# Language-Model_Kneser-Ney_Witten-Bell


I have made the my language model which take the below inputs to run 
  1) n-gram = any integer (It will build model dynamically for n-gram, hence can run for bigger than 3-gram also)
  2) smoothing type = k/w (in small later )
  3) input corpus file name = file name (when running from command prompt we need to keep the corpus in current working directory.)

We can run this model either from command line or from any IDE. To make it work from command line or IDE we need to set cmd_prmt = 'Y' 
(or 'N' for running it from IDE). While running it from IDE we need initialize the variables for n-gram, smoothing and corpus file name.

I read the corpus file row by row in sequence and did the below data cleansing:
1) First I analyzed the given corpus file and noticed that when sentence is long it has been splitted in next line and next line starts 
   with four blank spaces. I wrote a regex to join such sentences in single line.
2) All the book titles are starting with '}' or '[', I removed them using regex.
3) I removed all the punctuations (which are not \w or \s).

Then I wrote a custom function which returns the n-gram tokeniser which return the output list of tuples from any given sentence.
I used nltk word tokenizer in this custom function.

I create some default dictionaries to hold the counts. These default dictionaries have three level of nesting. I have use it as dynamic 
variable to keep count of any given n-gram. First order key specifies that that particular count it for which value on n in n-gram. Second key 
specifies the context and third key specify the current word and value keeps either the word count or type count depending on dictionary.

Then after cleaning the data line by line, I am reading it and updating my dictionary data structures with appropriate counts.

I have written the two functions one for Kneser-Ney and one for Witten-Bell. I used recursion so that my model can work on any value of N-GRAM
and it’s not limited to tri-gram.

In both the models when contex count is zero, to avoid divide by zero error, I have taken current n-gram as zero and shifted the weight to lower-gram
in my interpolation. For counting unigram probabilities I have considered MLE and for unknowns I used 1/|V|.

For Witten-Bell I have putted the value of lambdas and solve the equation and used this simplified equation to drive my interpolated probabilities
(with lambda and 1-lemda).

Initially I thought of checking the performance of my model by spliting the corpus in train and test and checking the perplexity on test. However
as we need to have input sentence at run time. I run my models on below four different type of sentences and compare the performance 
of both the models. In input sentence also, I am doing required data cleansing.

  1) Long sentence from corpus: "The young man that wakes deep at night, the hot hand seeking to repress what would master him,"
  2) Small sentence from: "The loving day"
  3) Similar sentence but outside from corpus: "The loving lady"
  4) Sentence from different domain: "Natural language processing is a subfield of linguistics"

My empirical observation from below data (2-gram to 5-gram) show that tri-gram onwards Kneser-Ney model is more stable and give almost same 
perplexity. However in Witten-Bell model is keep decreasing the perplexity for sentences which are from corpus and other sentences (even though 
they are from same domain) keep increasing the perplexity as we increase the n-gram value. As per my understanding Witten-Bell will overfit 
to given corpus more as compare to Kneser-Ney if we increase the  value of N-Gram. 

In Kneser-Ney it always use a fix discount D from higher gram to use interpolation.
However in Witten-Bell it take the portion (lambda) from higher gram likelihood and (1-lembda) for interpolation to lower gram. Lambda will have higher value if higher gram is more likely to come (very small number of types followed the context) and lambda will have small value if higher gram is less likely to come. In that way Witten-Bell higher gram has more contribution if higher gram is more likely to come and vice a versa. 
That’s why Witten-Bell perplexity spread is more than Kneser-Ney. In other word if test sentence is from same corpus, Witten Bell will give less perplexity than Kneser-Ney. 


Below are the perplexity for Kneser-Ney and Witten-Bell from 2-gram to 5-gram

Kneser-Ney perplexity table:
       | Long sentence from corpus | Small sentence from corpus | Similar outside sentence | Out of domain sentence
2-gram | 75.30846937348491         | 127.88101806716283         | 775.0227870402555        | 8947.293048026124
3-gram | 8.45164037137461          | 44.197988561830066         | 564.3237730112528        | 92010.83672654534
4-gram | 6.006845683992455         | 38.67618946100835          | 577.5181745785276        | 259571.31293203
5-gram | 5.090043404665582         | 38.67276359268134          | 579.6445569382404        | 259999.24511696651


Witten-Bell perplexity table:
       | Long sentence from corpus | Small sentence from corpus | Similar outside sentence | Out of domain sentence
2-gram | 55.64683000719808         | 110.98022665262127         | 969.0812802236909        | 9944.300743522172
3-gram | 5.055809380576616         | 36.28798208587483          | 775.2679117910691        | 11868.341398304106
4-gram | 2.696848844739582         | 26.691916639619194         | 889.4995799613472        | 12926.277736819357
5-gram | 1.9830708661066012        | 24.08087186136967          | 1085.2098434800523       | 14093.730769046864
