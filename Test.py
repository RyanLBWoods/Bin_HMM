import HMM
import nltk
import time
import json
import string
import collections
from nltk.corpus import brown

# Read trained model from file
emf = open('Emission.json', 'r')
emission = json.load(emf)
trf = open('Transition.json', 'r')
tr = json.load(trf)
transition = {}
for key in tr:
    t_key = key[3: len(key) - 2].split(',')
    transition[(t_key[0][:-1], t_key[1][3:])] = tr[key]

# Set testing sets
sents = brown.tagged_sents(tagset='universal')  # Get corpus
training_sents = []
test_length = 0.1 * len(sents)
print test_length
exit(0)
testing_sents = []
for sent in sents[test_length: len(sents)]:
    testing_sents.append(sent)
# Collect pairs of tags
pairs = []
for token in transition:
    pairs.append(token)


def viterbi(emissions, transitions, test_sents):
    vtb = collections.OrderedDict()
    vtbs = []
    from_list = []
    maxp = 0
    temp_key2 = ''
    for sent in test_sents:
        i = 0
        # print "sent:", sent
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
                        if (u'START', key) in transitions:
                            probability = emissions['UNK'][key] * transitions[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START', key)] = probability
                        else:
                            vtb[i][(u'START', key)] = probability
                # print vtb
                # exit(0)
            else:
                if token[0] in emissions:
                    for key in emissions[token[0]]:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i - 1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = emissions[token[0]][key] * transitions[key2] * vtb[i - 1][t]
                                    if observe > maxp:
                                        maxp = observe
                                        temp_key2 = key2
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
                        # print vtb
                        # exit(0)
                else:
                    for key in emissions['UNK']:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i - 1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = emissions['UNK'][key] * transitions[key2] * vtb[i - 1][t]
                                    if observe >= maxp:
                                        maxp = observe
                                        temp_key2 = key2
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
            i += 1
            maxp = 0
            if i == len(sent):
                # exit(0)
                last = vtb[i - 1]
                for tag in last:
                    probability = last[tag] * transitions[(tag[1], u'END')]
                    if i not in vtb:
                        vtb[i] = {}
                        vtb[i][(tag[1], u'END')] = probability
                    else:
                        vtb[i][(tag[1], u'END')] = probability
            from_list = []
        # print vtb
        vtbs.append(vtb)
        vtb = collections.OrderedDict()
    return vtbs


# test = viterbi(em, tr, testing_sents)

def backpoint(test_sents):
    vs = viterbi(emission, transition, test_sents)
    max_prob = 0
    tag = ''
    test_tag = []
    test_tags = []
    for v in vs:
        # print v
        j = next(reversed(v))
        # print j
        # while j > 0:
        for tag_prob in v[j]:
            # print tag_prob
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
        # max_prob = 0
        # print test_tag
        test_tags.append(test_tag)
        test_tag = []
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
    # print test_tags
    i = 0
    print len(test_tags)
    print "222:   ", len(origin_tags)
    print len(test_tags[0]), test_tags[0]
    print len(origin_tags[0]), origin_tags[0]
    while i < len(test_tags):
        j = 0
        while j < len(test_tags[i]):
            if test_tags[i][j] == origin_tags[i][j]:
                right_tag += 1
            j += 1
        i += 1
    print right_tag
    print total_tag
    accuracy = right_tag / (1.0 * total_tag)
    print accuracy


calculate_accuracy(testing_sents)
