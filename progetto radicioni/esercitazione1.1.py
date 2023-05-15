
from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.wsd import lesk

def leak_Algorithm(word,sentence):
    print(word)
    syns_word = wn.synsets(word)

    #syns_word.lemmas("eng")
    #print(syns_word)
   #ciao = syns_word.lemma_names()
   # print(ciao)
    max_overlap = 0
    return max_overlap

if __name__ == '__main__':
    num_sentences = 50
    sentences = semcor.sents()[:num_sentences]
    for s in sentences:
       i = random.randint(0,len(s)-1)
       leak_Algorithm(s[i],s)
