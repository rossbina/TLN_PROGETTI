import hashlib


import random
from random import randint
from random import seed

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn


def print_frames_with_IDs():
    for x in fn.frames():
        print('{}\t{}'.format(x.ID, x.name))

def get_frams_IDs():
    return [f.ID for f in fn.frames()]


def getFrameSetForStudent(surname, list_len=5):
    nof_frames = len(fn.frames())
    base_idx = (abs(int(hashlib.sha512(surname.encode('utf-8')).hexdigest(), 16)) % nof_frames)
    frames_set=[]
    print('\nstudent: ' + surname)
    framenet_IDs = get_frams_IDs()
    i = 0
    offset = 0
    seed(1)
    while i < list_len:
        fID = framenet_IDs[(base_idx+offset)%nof_frames]
        f = fn.frame(fID)
        fNAME = f.name
        print('\tID: {a:4d}\tframe: {framename}'.format(a=fID, framename=fNAME))
        frames_set.append(f.name)
        offset = randint(0, nof_frames)
        i += 1
    return frames_set


def get_main_term(mwe):
    lemmatizer = WordNetLemmatizer()
    words = mwe.split('_')

    if len(words) == 2:
        if wn.synsets(words[0], pos=wn.VERB) and wn.synsets(words[1], pos=wn.NOUN):
            main_term = lemmatizer.lemmatize(words[0], pos=wn.VERB)
        elif wn.synsets(words[0], pos=wn.NOUN) and wn.synsets(words[1], pos=wn.ADJ):
            main_term = lemmatizer.lemmatize(words[0], pos=wn.NOUN)
        else:
            main_term = words[0]
    else:
        main_term = words[0]

    return main_term

from nltk.corpus import wordnet as wn

def get_context(synsets):
    #print("getcontext()")
    context = []

    # Aggiungi definizioni dei synset contenenti il termine
    for s in synsets:
        #print("synsets",": ", s)
        definitions = s.definition()
        #print("definizioni trovate:",definitions)
        context.append(definitions)
        #print("contesto :",context)

    # Aggiungi esempi dei synset contenenti il termine
    for synset in synsets:
        examples = synset.examples()
        #print("examples :", examples)
        #print("context afted exapmples: ",context)
        for example in examples:
            if example != []:
                context.append(example)

    # Restituisci il contesto come una lista di frasi
    return context


def calculate_score(synset, context):

    #print("CALCULATE SCORE: \n")
    #print("CONTEXT : ",context)
    score = 0
    for sentence in context:
        #print("FRASE ", sentence)
        if isinstance(sentence, list):
            sentence = sentence[0]

        words= sentence.split(" ")
        for word in words:
            word_synsets = wn.synsets(word)
            for word_synset in word_synsets:
                if word_synset == synset:
                 score += 1
    return score


def disambiguate_term(synsets):

    if len(synsets) == 1:
        return synsets[0]
    elif len(synsets) > 1:
        context = get_context(synsets)  # Implementa la logica per ottenere il contesto del termine
        #print("context : ",context)
        best_score = 0
        selected_synset = None

        for synset in synsets:
            score = calculate_score(synset, context)  # Implementa la logica per calcolare lo score di ogni synset

            if score > best_score:
                best_score = score
                selected_synset = synset

        return selected_synset

    return None

if __name__ == '__main__':
    frames_set_Borra = getFrameSetForStudent('Borra')
    frames_set_Gino = getFrameSetForStudent('Gino')
    synset_borra = []
    synset_gino= []
    i = 0
    j = 0
    for f in frames_set_Borra:
        synset_borra.append(wn.synsets(get_main_term(f)))
    for f in frames_set_Gino:
        synset_gino.append(wn.synsets(get_main_term(f)))
    for f in frames_set_Gino:

        for i in range(len(synset_gino)):

            print("FRAME NAME : ", frames_set_Gino[i],"\nTRA I SENSI : ",synset_gino[i],' \nSYNSET MAPPATO -->' , disambiguate_term(synset_gino[i]))

    for f in frames_set_Borra:
        for i in range(len(synset_borra)):
            print("FRAME NAME : ", frames_set_Borra[i],"\nTRA I SENSI : ",synset_borra[i],' \nSYNSET MAPPATO -->' , disambiguate_term(synset_borra[i]))








