import hashlib


import random
from random import randint
from random import seed

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn
from nltk.tokenize import word_tokenize

from esercitazione1_1 import remove_punctuation


def print_frames_with_IDs():
    for x in fn.frames():
        print('{}\t{}'.format(x.ID, x.name))


def get_frams_IDs():
    return [f.ID for f in fn.frames()]


def getFrameSetForStudent(surname, list_len=5):
    nof_frames = len(fn.frames())
    base_idx = (
        abs(int(hashlib.sha512(surname.encode('utf-8')).hexdigest(), 16)) % nof_frames)
    frames_set = []
    print('\nstudent: ' + surname)
    framenet_IDs = get_frams_IDs()
    i = 0
    offset = 0
    seed(1)
    while i < list_len:
        fID = framenet_IDs[(base_idx+offset) % nof_frames]
        f = fn.frame(fID)
        fNAME = f.name
        print('\tID: {a:4d}\tframe: {framename}'.format(
            a=fID, framename=fNAME))
        frames_set.append(f)
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


def ctx_sense(sense):
    gloss = remove_punctuation(word_tokenize(sense.definition()))
    examples = sense.examples()

    scomposed_exemples = []

    for e in examples:
        scomposed_exemples += remove_punctuation(word_tokenize(e))

    return (gloss + scomposed_exemples)


def calculate_score(synset, context):

    #print("CALCULATE SCORE: \n")
    #print("CONTEXT : ",context)
    score = 0
    for sentence in context:
        #print("FRASE ", sentence)
        if isinstance(sentence, list):
            sentence = sentence[0]

        words = sentence.split(" ")
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
        # Implementa la logica per ottenere il contesto del termine
        context = get_context(synsets)
        #print("context : ",context)
        best_score = 0
        selected_synset = None

        for synset in synsets:
            # Implementa la logica per calcolare lo score di ogni synset
            score = calculate_score(synset, context)

            if score > best_score:
                best_score = score
                selected_synset = synset

        return selected_synset

    return None

# w = FName


def ctx(w):
    return remove_punctuation(word_tokenize(w.definition))


def score(sig, cont):

    sig_set = set(sig)
    cont_set = set(cont)

    return (len(sig_set.intersection(cont_set))+1)

if __name__ == '__main__':
    frames_set_Borra = getFrameSetForStudent('Borra')
    frames_set_Gino = getFrameSetForStudent('Gino')

    synset_borra_fname = {}
    synset_borra_FE = {}
    frameset_borra_FE = {}
    synset_borra_LU = {}
    fe_borra = []
    lu_borra = []

    synset_gino = []
    fe_gino = []
    lu_gino = []

    cw_borra = []
    cw_borra_FE= []
    cs_borra = []

    i = 0
    j = 0

    for f in frames_set_Borra:
        fe_borra = []
        synset_borra_fname[f.name] = (wn.synsets(get_main_term(f.name)))
        fe_borra.append(f.FE)
        lu_borra.append(f.lexUnit)

        cw_borra = ctx(f)

        best_sense = None
        best_score = 0

        for s in synset_borra_fname[f.name]:
            cs_borra = ctx_sense(s)
            temp_score = score(cs_borra, cw_borra)

            if temp_score > best_score:
                best_score = temp_score
                best_sense = s
        print("-----------------------------------------------------")
        print("FRAME NAME : ", f.name,' \n**Mapping**:\n *Sense*: ', best_sense, '\n *Score* : ', best_score)
        print("-----------------------------------------------------")
        print("FE OF", f.name)
        i = 0
        for fe in fe_borra:

            for f1 in fe:
                i=i+1
                print(" n°: ",i ," ---> ",f1)
                synset_borra_FE[f1] = (wn.synsets(get_main_term(f1)))
                frameset_borra_FE[f1]= fe[f1]
                best_sense_FE = None
                best_score_FE = 0
                temp_score_FE = 0


                for frame in frameset_borra_FE[f1]:
                    cw_borra_FE = ctx(frameset_borra_FE[f1])
                    for s in synset_borra_FE[f1]:
                        temp_score_FE = score(ctx_sense(s), cw_borra_FE)
                        if temp_score_FE > best_score_FE:
                            best_score_FE = temp_score_FE
                            best_sense_FE = s

                print(" **Mapping**: \n", f1, " *Best Sense*: ", best_sense_FE, "\n *Score*: ", best_score_FE,"\n")
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")

        # print(set(cs_borra))
        # print(set(cw_borra))

        #print("FRAME NAME : ", f.name, "\nTRA I SENSI : ",
              #synset_borra_fname[f.name], ' \nSYNSET MAPPATO -->', best_sense, 'con Score: ', best_score)

    #cs_borra = ctx(s)

    # for f in frames_set_Gino:
    #   synset_gino.append(wn.synsets(get_main_term(f.name)))
    #  fe_gino.append(f.FE)
    # lu_gino.append(f.lexUnit)

    # for f in frames_set_Gino:
    # synset_gino.append(wn.synsets(get_main_term(f.name)))
    # for f in frames_set_Gino:

    # for i in range(len(synset_gino)):

    #print("FRAME NAME : ", frames_set_Gino[i],"\nTRA I SENSI : ",synset_gino[i],' \nSYNSET MAPPATO -->' , disambiguate_term(synset_gino[i]))

    # for f in frames_set_Borra:
    # for i in range(len(synset_borra)):
    #print("FRAME NAME : ", frames_set_Borra[i],"\nTRA I SENSI : ",synset_borra[i],' \nSYNSET MAPPATO -->' , disambiguate_term(synset_borra[i]))
