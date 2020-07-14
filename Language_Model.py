
# coding: utf-8

# In[74]:


import sys
from collections import defaultdict
from nltk import word_tokenize
import re
import os


# In[86]:


cmd_prmt = 'Y'

if cmd_prmt =='Y':
    order = sys.argv[1]
    smoothing = sys.argv[2]
    corpus = sys.argv[3]
else:
    order = 3
    smoothing = 'k'
    os.chdir( 'D:\\Arvin\\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Assignments\\Assignment 1')
    corpus = 'corpus.txt'
    #os.chdir( 'D:\\Arvin\\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Arvin')
    #corpus = 'shakespeare.txt'

if order < 1:
      print('Kindly enter number of grams 1 or more')
      sys.exit()
if smoothing =='w' or smoothing =='k':
    pass
else:
    print('Please enter k for KneserNey or w for Witten Bell.')
    sys.exit()
    
if order >3:
    print("this assignment is for upto Tri-Gram, anyway go ahead:")

model     = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
cnt_fwd   = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
cnt_back  = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
total_ngram_types = defaultdict(lambda: 0)
vocab_count = defaultdict(lambda: 0)

f = open(corpus,'r',encoding='ascii')
data = f.readlines()


# In[87]:


def cust_ngrams(line,order, left_pad = True):
    if left_pad ==True:
        pad_lst = ''
        for r in range (order-1):
            pad_lst = pad_lst + 'start_pedding ' 
        line = pad_lst + line
    token = word_tokenize(line)
    
    if order > 1:
        ngrams = zip(*[token[i:] for i in range(order)])
        ngrams = list(tuple(ngrams))
    else:
        ngrams = token
    
    return ngrams     


# In[78]:


def calculate_counts(line):
    #line = '<s1> <s2>' + line
    line = line.lower()
    #line = line.split()
    
    for r in range (2,order+1):
        w=''
        for w in cust_ngrams(line, r, left_pad=True):
            model[r][w[:-1]][w[-1]]  += 1
            cnt_fwd[r][w[:-1]][w[-1]]  = 1
            cnt_back[r][w[-1]][w[:-1]] = 1          
    
    if order == 1:
        for w in cust_ngrams(line, 1, left_pad=False):
            vocab_count[w] += 1
            #vocab_size +=1
            


# In[88]:


re_cont_sent = re.compile ('^   .*')
re_book_name = re.compile ("^[}\[].*")
re_punctuation = re.compile("[^\w\s]")

pre_sentence = ''
for sentence in data:
    match1 = re.findall(re_cont_sent,sentence)
    if len(match1) > 0:
        pre_sentence = pre_sentence + sentence               # if current sentence start with four space its the continuation from previous sentence
    else:
        match2 = re.findall(re_book_name,sentence)
        if len(match2) > 0:                                  # if sentence is starting from } or [, its name of book, its meta data, hence skipping it
            pre_sentence = ''
        else:
            pre_sentence = re_punctuation.sub('', pre_sentence)
            
            if pre_sentence.strip() != '':
                calculate_counts(pre_sentence)
            pre_sentence = sentence
                #print (pre_sentence)

calculate_counts(pre_sentence)

vocab_size=0


for r in range(2,order+1):
    for word in set(cnt_fwd[r]):
        total_ngram_types[r] = total_ngram_types[r] + len(set(cnt_fwd[r][word]))
        if r==2:
            vocab_size+=1
            
if order ==1:
    vocab_size= float(sum(vocab_count.values()))
    
    


# In[89]:


def kn_probability(w,r,high_order='N'):
    if high_order =='Y' and r == 1:
        count = vocab_count[w]
        pre_count = vocab_size
        
    elif high_order =='Y':
        count = model[r][w[:-1]][w[-1]]
        pre_count = float(sum(model[r][w[:-1]].values()))
        print('N-GramIs:',r,'WordIs:',w, 'CountOf',w[:-1],':', w[-1], 'Is: ', count, 'ContextCountIs:', pre_count)
        
    else:
        count = len(set(cnt_back[r+1][w[-1]]))       # how many words r+1 grams ends with last word w.
        pre_count = total_ngram_types[r+1]          # total number of r+1 gram types. 
        
    
    if pre_count >0:
        disc_prb = (count - d)/pre_count
        if disc_prb <0:
            disc_prb = 0
        lembda = (d/(pre_count)) * (len(set(cnt_fwd[r][w[:-1]])))
    else:
        disc_prb = 0
        lembda = 1
    
    if r >1:
        kn_lower = kn_probability(w[1:],r-1)
    else:
        kn_lower = lembda/vocab_size
    
    return (disc_prb + (lembda * kn_lower))     


# In[90]:


def wb_probability(w,r):
    count = model[r][w[:-1]][w[-1]]
    pre_count = float(sum(model[r][w[:-1]].values()))
    N1plus = (len(set(cnt_fwd[r][w[:-1]])))
    
    if r>1:
        lower_gram_prob = wb_probability(w[1:],r-1)
        if pre_count >0:
            wb_prob = (count + (N1plus * lower_gram_prob))/(N1plus + pre_count)
        else:
            wb_prob = lower_gram_prob
    else:
        if count < 1:
            count = 1
        wb_prob = count/vocab_size
    
    return (wb_prob)      


# In[93]:


d = .75   #constant discount 
probability = 1

input_str = input("Provide input sentence:")
raw_input = input_str
input_str = re_punctuation.sub('', input_str)

input_str = input_str.lower()
#input_str = input_str.split()
#print(input_str)

if smoothing == 'k':
    for w in cust_ngrams(input_str, order, left_pad = True):
        kn_prob = kn_probability(w,order,high_order='Y')
        probability = probability*kn_prob

if smoothing == 'w':
    for w in cust_ngrams(input_str, order, left_pad = True):
        prob = wb_probability(w,order)
        probability = probability* prob  
        

print ('probability of sentence ',raw_input,' is:', probability)


