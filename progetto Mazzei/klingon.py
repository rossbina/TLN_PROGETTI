import os
import numpy as np
import pandas as pd


# concatenation of cells for comparison with grammar
def create_cell(first, second):
    res = set()
    if first == set() or second == set():
        return set()
    elif first == "-" or second == "-":
        return set()
    for f in first:
        for s in second:
            res.add(f + " " + s)
    return res


def read_grammar(filename="./grammar.txt"):
    filename = os.path.join(os.curdir, filename)
    with open(filename) as grammar:
        rules = grammar.readlines()
        v_rules = []
        t_rules = []

        for rule in rules:
            left, right = rule.split(" -> ")

            # for two or more results from a variable
            right = right[:-1].split(" | ")
            for ri in right:

                # it is a terminal
                if rule.find("|") > 0:
                    t_rules.append([left, ri])

                # it is a variable
                else:
                    v_rules.append([left, ri])
        return v_rules, t_rules


def get_duplicates(sentence):
    duplicates = []
    for s in sentence:
        flag = s[0]
        for s1 in sentence:
            if s != s1:
                if flag == s1[0] or (s1[1] in s[1]) or (s[1] in s1[1]):
                    duplicates.append(s1)
    return duplicates


def read_input(filename="./input.txt"):
    # reads the inputs from a text file
    filename = os.path.join(os.curdir, filename)
    with open(filename) as inp:
        # inputs = inp.read().split()
        sentence = [(0, "-")]

        with open("./dictionary.txt") as dic:
            dictionary = dic.read().split()
            inputs = inp.read()
            for d in dictionary:
                indexstart = inputs.find(d)
                if indexstart != -1:
                    sentence.append(((indexstart + 1), (inputs[indexstart:indexstart + (len(d))])))
    print("Sentence before get_duplicatea()", sentence)
    duplicates = get_duplicates(sentence)
    print("List of duplicates get_duplicates()", duplicates)


    for l, r in duplicates:
        for l1, r1 in duplicates:
            if r1 != r and r in r1:
                sentence.remove((l, r))

    sorted_sentence = sorted(sentence, key=lambda x: x[0])
    final_sentence = []
    for s in sorted_sentence:
        final_sentence.append(s[1])
    print("Sentence after get_duplicates()",final_sentence)
    return final_sentence


def cky(v, t, inp):
    n = len(inp)

    var0 = [va[0] for va in v]
    var1 = [va[1] for va in v]
    table = [[set() if j >= i + 1 else "-" for j in range(n)] for i in range(n - 1)]
    index_count = 0
    for j in range(1, n):
        for te in t:
            if inp[j] == te[1]:
                table[j - 1][j].add(te[0])
        for i in reversed(range(0, j - 1)):
            for k in range(i + 1, j):
                cell = create_cell(table[i][k], table[k][j])
                for c in cell:
                    index_count = 0
                    for v in var1:
                        index_count = index_count + 1
                        if c in v:
                            table[i][j].add(var0[index_count - 1])

                for c in cell:
                    if inp[j] == te[1]:
                        table[j - 1][j].add(te[0])

    return table


def show_result(t, inp):
    d = dict()

    for k in range(1, len(inp)):
        d[inp[k]] = []

    for r in range(0, len(t)):
        for c in range(1, len(t) + 1):
            d[inp[c]].append(t[r][c])
    df = pd.DataFrame.from_dict(d)
    print(df.to_string(index=False))
    if "S" in t[0][len(t)]:
        print("OK , the sentence is consistent with the grammar!")
    else:
         print("NO , the sentence is not consistent with the grammar!")

if __name__ == '__main__':
    # reading grammar and saving variables and terminals
    varies, terms = read_grammar()
    # reading and saving input
    input = read_input()
    table = cky(varies, terms, input)
    show_result(table, input)
