
from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
import random
import nltk
# nltk.download('semcor')
# nltk.download('punct')
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.wsd import lesk


def remove_punctuation(tokenized_sentence):
    context = []
    for w in tokenized_sentence:
        if w.isalpha():
            context.append(w)
    return context

# set of words in the gloss and examples of sense


def get_signature(sense):
    gloss = remove_punctuation(word_tokenize(sense.definition()))
    examples = sense.examples()

    scomposed_exemples = []

    for e in examples:
        scomposed_exemples += remove_punctuation(word_tokenize(e))

    return (gloss + scomposed_exemples)

# calcolo l'overlap tra due liste di token


def compute_overlap(sig, cont):

    sig_set = set(sig)
    cont_set = set(cont)

    return len(sig_set.intersection(cont_set))


def remove_stop_words(token_list):
    stops = set(sw.words('english'))
    clear_tokens = []

    for t in token_list:
        if t not in stops:
            clear_tokens.append(t)
    return clear_tokens


def lesk(word, sentence):
    syns_word = wn.synsets(word)

    if len(syns_word) == 0:
        return None

    context = remove_punctuation(sentence)
    context = remove_stop_words(context)
    max_overlap = 0

    best_sense = syns_word[0]

    for sense in syns_word:
        signature = get_signature(sense)
        overlap = compute_overlap(signature, context)

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


if __name__ == '__main__':
    num_sentences = 50
    sentences = random.sample(list(semcor.sents()), num_sentences)

    for s in sentences:
        # s = remove_punctuation(s)
        # s = remove_stop_words(s)
        print("SENTENCE: ", s)
        for w in s:
            # i = random.randint(0, len(clear_sent)-1)
            best_sense = lesk(w, s)
            if best_sense is not None:
                if ".n." in best_sense.name():
                    print(w, "->", best_sense, "|", best_sense.definition())
