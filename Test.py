import HMM
import nltk
import time
import collections
from nltk.corpus import brown

tick = time.time()
print tick
# Pre-processing training and testing sets
sents = brown.tagged_sents(tagset='universal')  # Get training set
# train_length = len(sents) / 2  # Define size of training set
train_length = 1000
training_sents = []
# test_length = len(sents) - train_length + 1
test_length = len(sents) - 2
testing_sents = []
# Add start and end tag
start = (u'<s>', u'START')
end = (u'</s>', u'END')
for sent in sents[0: train_length]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    training_sents.append(sent)
print "train", time.time() - tick
for sent in sents[test_length: len(sents)]:
    testing_sents.append(sent)
# print testing_sents
print "test", time.time() - tick
pairs = HMM.get_pair(training_sents)
# exit(0)
# Get emissions and transitions
em = HMM.emission_with_unk(training_sents)
print "em time ", time.time()
tr = HMM.transition_probability(training_sents)
print "time", time.time() - tick
# print em['was']
# print tr


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
                if token[0] in em:
                    for key in em[token[0]]:
                        probability = em[token[0]][key] * tr[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START',key)] = probability
                        else:
                            vtb[i][(u'START',key)] = probability
                else:
                    for key in em['UNK']:
                        if (u'START', key) in tr:
                            probability = em['UNK'][key] * tr[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START',key)] = probability
                        else:
                            vtb[i][(u'START',key)] = probability
                # print vtb
                # exit(0)
            else:
                if token[0] in em:
                    for key in em[token[0]]:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i-1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = em[token[0]][key] * tr[key2] * vtb[i-1][t]
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
                    for key in em['UNK']:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i - 1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = em['UNK'][key] * tr[key2] * vtb[i - 1][t]
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
                    probability = last[tag] * tr[(tag[1], u'END')]
                    if i not in vtb:
                        vtb[i] = {}
                        vtb[i][(tag[1], u'END')] = probability
                    else:
                        vtb[i][(tag[1], u'END')] = probability
            from_list = []
        print vtb
        vtbs.append(vtb)
        vtb = collections.OrderedDict()
    return vtbs


# test = viterbi(em, tr, testing_sents)

def backpoint(test_sents):
    vs = viterbi(em, tr, test_sents)
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


def accuracy(test_sents):
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
    # exit(0)
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


accuracy(testing_sents)
print time.time() - tick