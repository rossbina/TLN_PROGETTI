from nltk.corpus import wordnet as wn

import pandas as pd

def simPath(word1, word2):
    syns1= getsynSet(word1)
    syns2= getsynSet(word2)

    sim= []
    for s1 in syns1:
        for s2 in syns2:
            print(s1,s2)
            if isinstance(s1, list):
                s1= s1[0]
            if isinstance(s2, list):
                s2= s2[0]
            depth_max = max(s1.max_depth(),s2.max_depth())
            print(depth_max)
            path_len = s1.shortest_path_distance(s2)

            if path_len is None or path_len == 0:
                # Se i due synset sono uguali o non sono collegati, simpath(s1, s2) è il valore massimo di 2 * depth_max
                sim.append( 2 * depth_max)
            elif path_len == 2 * depth_max:
                # Se la lunghezza del percorso è pari a 2 * depth_max, simpath(s1, s2) è il valore minimo di 0
                sim.append(0)
            else:
                # Calcola la similarità del percorso utilizzando la formula: simpath(s1, s2) = 1 - (len(s1, s2) / (2 * depth_max))
                sim.append(2 * depth_max - path_len)

    return sim

# Definizione della funzione di similarità
def provaWUePALMER(word1,word2):
    cs = []
    syns1=getsynSet(word1)
    syns2=getsynSet(word2)
    print("syn1: ", syns1, "syn2: ",syns2 )
    for i in range(len(syns1)):
        for j in range(len(syns2)):
            depths1 = getDepth(syns1[i])
            depths2 = getDepth(syns2[j])
            print(syns1[i],syns2[j])
            LCS = getLCS(syns1[i],syns2[j])
            print(LCS)
            depthLCS = getDepth(LCS)
            cs.append(2 * depthLCS / (depths1 + depths2))
    return cs


def getsynSet(word):
    return  wn.synsets(word)

def getDepth(syns):
    root = wn.synset('entity.n.01')
    print("cerco depth di: ", syns, root)
    if isinstance(syns, list):
        syns= syns[0]
    return syns.path_similarity(root)

def getLCS(synset1,synset2):
    if synset1 and synset2:
        lca_synset = synset1.lowest_common_hypernyms(synset2)
        if len(lca_synset) == 0:
             # I due sensi non hanno nessun iperonimo in comune, la loro LCS è la radice della gerarchia
            lca_synset = wn.synset('entity.n.01')
    return lca_synset

def read_wordSense353():

    df = pd.read_csv('./WordSim353.txt', sep='	', header=None, names=['Word1', 'Word2', 'similarity'])
    # crea una matrice con le colonne col1, col2 e col3
    tableWords = df[['Word1', 'Word2', 'similarity']].values

    return tableWords

if __name__ == '__main__':
     wordSense =  read_wordSense353()
     #cs = provaWUePALMER(wordSense[0][0],wordSense[0][1])
     shoretest_path = simPath(wordSense[0][0],wordSense[0][1])
    # print(cs, wordSense[0][2],'\n')
     print(shoretest_path)
     #for i in range(len(wordSense)):
         #print(cs[i],wordSense[i][3])
#


