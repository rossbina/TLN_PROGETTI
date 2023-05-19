import hashlib


import random
from random import randint
from random import seed

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn
from nltk.tokenize import word_tokenize
frame = fn.frame_by_name("Commitment")
FE_= frame.FE
#print(type(FE_))
#print(sorted([x for x in FE_]))
for f in FE_:
    print(FE_[f].definition,'\n')

#for fe in FE_:
    #print(fe)
    #print(fn.frames(FE_[fe]))
