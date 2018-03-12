import json
import sys
import collections
from nltk.corpus import brown, treebank, masc_tagged, conll2000

if len(sys.argv) != 3:
    print "Usage: python HMM.py <corpus_index> <tagset_index>"
    print "Corpus:          Tagset: "
    print "1. brown           1. Default"
    print "2. treebank        2. Universal"
    print "3. masc_tagged"
    print "4. conll2000"
    exit(0)
else:
    index = int(sys.argv[1])
    tagset = int(sys.argv[2])
    if index == 1 and tagset == 1:
        sents = brown.tagged_sents()
    elif index == 1 and tagset == 2:
        sents = brown.tagged_sents(tagset='universal')
    elif index == 2 and tagset == 1:
        sents = treebank.tagged_sents()
    elif index == 2 and tagset == 2:
        sents = treebank.tagged_sents(tagset='universal')
    elif index == 3 and tagset == 1:
        sents = masc_tagged.tagged_sents()
    elif index == 3 and tagset == 2:
        sents = masc_tagged.tagged_sents(tagset='universal')
    elif index == 4 and tagset == 1:
        sents = conll2000.tagged_sents()
    elif index == 4 and tagset == 2:
        sents = conll2000.tagged_sents(tagset='universal')
    else:
        print "Usage: python HMM.py <corpus_index> <tagset_index>"
        print "Corpus:          Tagset: "
        print "1. brown           1. Default"
        print "2. treebank        2. Universal"
        print "3. masc_tagged"
        print "4. conll2000"
        exit(0)

# Read trained model from file
print "Loading model"
emf = open('Emission.json', 'r')
emission = json.load(emf)
trf = open('Transition.json', 'r')
tr = json.load(trf)
transition = {}
# Process the key in transitions due to type
for key in tr:
    t_key = key[3: len(key) - 2].split('u')
    transition[(t_key[0][:-1-2], t_key[1][1:])] = tr[key]
# Set testing sets
test_length = int(0.1 * len(sents))
testing_sents = []
for sent in sents[len(sents) - test_length: len(sents)]:
    testing_sents.append(sent)

# Collect pairs of tags
pairs = []
for token in transition:
    pairs.append(token)


# Apply Viterbi algorithm
def viterbi(emissions, transitions, test_sents):
    print "Running Viterbi algorithm"
    vtb = collections.OrderedDict()
    vtbs = []
    maxp = -1
    temp_key2 = ''
    for sent in test_sents:
        i = 0
        for token in sent:
            if i == 0:
                if token[0] in emissions:
                    for key in emissions[token[0]]:
                        probability = emissions[token[0]][key] * transitions[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START', key)] = probability
                        else:
                            vtb[i][(u'START', key)] = probability
                else:
                    for key in emissions['UNK']:
                        probability = emissions['UNK'][key] * transitions[(u'START', key)]
                        # probability = 1 * transitions[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START', key)] = probability
                        else:
                            vtb[i][(u'START', key)] = probability
            else:
                if token[0] in emissions:
                    for key in emissions[token[0]]:
                        for t in vtb[i - 1]:
                            observe = emissions[token[0]][key] * transitions[(t[1], key)] * vtb[i - 1][t]
                            if observe > maxp:
                                maxp = observe
                                temp_key2 = (t[1], key)
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
                        maxp = -1
                else:
                    for key in emissions['UNK']:
                        for t in vtb[i - 1]:
                                    observe = emissions['UNK'][key] * transitions[(t[1], key)] * vtb[i - 1][t]
                                    # observe = 1 * transitions[key2] * vtb[i - 1][t]
                                    if observe > maxp:
                                        maxp = observe
                                        temp_key2 = (t[1], key)
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
                        maxp = -1
            i += 1
            if i == len(sent):
                last = vtb[i - 1]
                for tag in last:
                    probability = last[tag] * transitions[(tag[1], u'END')]
                    if i not in vtb:
                        vtb[i] = {}
                        vtb[i][(tag[1], u'END')] = probability
                    else:
                        vtb[i][(tag[1], u'END')] = probability
        vtbs.append(vtb)
        vtb = collections.OrderedDict()
    return vtbs


def backpoint(test_sents):
    vs = viterbi(emission, transition, test_sents)
    max_prob = 0
    tag = ''
    test_tag = []
    test_tags = []
    print "Choosing tags"
    for v in vs:
        j = next(reversed(v))
        for tag_prob in v[j]:
            if v[j][tag_prob] > max_prob:
                max_prob = v[j][tag_prob]
                tag = tag_prob[0]
        list.insert(test_tag, 0, tag)
        j = j - 1
        while j > 0:
            for probs in v[j]:
                if probs[1] == tag:
                    list.insert(test_tag, 0, probs[0])
            tag = test_tag[0]
            j -= 1
        test_tags.append(test_tag)
        test_tag = []
        max_prob = 0
    return test_tags


def calculate_accuracy(test_sents):
    test_tags = backpoint(test_sents)
    origin_tags = []
    total_tag = 0
    right_tag = 0
    for sent in test_sents:
        tags = [t for (_, t) in sent]
        origin_tags.append(tags)
        total_tag += len(tags)
    i = 0
    while i < len(test_tags):
        j = 0
        while j < len(test_tags[i]):
            if test_tags[i][j] == origin_tags[i][j]:
                right_tag += 1
            j += 1
        i += 1
    print "Total words: ", total_tag
    print "Right guessed: ", right_tag
    accuracy = right_tag / (1.0 * total_tag)
    print "Accuracy: ", accuracy


calculate_accuracy(testing_sents)
