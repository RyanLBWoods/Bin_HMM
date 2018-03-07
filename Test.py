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
train_length = 5000
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
print len(em)
print tr


def viterbi(emissions, transitions, test_sents):
    vtb = collections.OrderedDict()
    vtbs = []
    from_list = []
    maxp = 0
    temp = ''
    pre_tag = ''
    last = {}
    for sent in test_sents:
        i = 0
        print len(sent)
        for token in sent:
            if i == 0:
                if token[0] in em:
                    for key in em[token[0]]:
                        probability = em[token[0]][key] * tr[(u'START', key)]
                        if token[0] not in vtb:
                            vtb[(token[0], u'START')] = {}
                            vtb[(token[0], u'START')][key] = probability
                        else:
                            vtb[(token[0], u'START')][key] = probability
                else:
                    for key in em['UNK']:
                        probability = em['UNK'][key] * tr[(u'START', key)]
                        if token[0] not in vtb:
                            vtb[(token[0], u'START')] = {}
                            vtb[(token[0], u'START')][key] = probability
                        else:
                            vtb[(token[0], u'START')][key] = probability
                temp = (token[0], u'START')
                pre_tag = u'START'
            else:
                if token[0] in em:
                    for key in em[token[0]]:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for key2 in from_list:
                            if temp in vtb:
                                if key2[0] in vtb[temp]:
                                    observe = em[token[0]][key] * tr[key2] * vtb[temp][key2[0]]
                                    if observe > maxp:
                                        maxp = observe
                                        pre_tag = key2[0]
                                else:
                                    continue
                        if token[0] not in vtb:
                            vtb[(token[0], pre_tag)] = {}
                            vtb[(token[0], pre_tag)][key] = maxp
                        else:
                            vtb[(token[0], pre_tag)][key] = maxp
                else:
                    for key in em['UNK']:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for key2 in from_list:
                            if temp in vtb:
                                if key2[0] in vtb[temp]:
                                    observe = em['UNK'][key] * tr[key2] * vtb[temp][key2[0]]
                                    if observe > maxp:
                                        maxp = observe
                                        pre_tag = key2[0]
                                else:
                                    continue
                        if token[0] not in vtb:
                            vtb[(token[0], pre_tag)] = {}
                            vtb[(token[0], pre_tag)][key] = maxp
                        else:
                            vtb[(token[0], pre_tag)][key] = maxp
            temp_token = token[0]
            temp = (temp_token, pre_tag)
            temp_tag = vtb[temp]
            i += 1
            maxp = 0
            if i == len(sent):
                last = vtb[temp]
                for tag in last:
                    probability = last[tag] * tr[(tag, u'END')]
                    if (u'END', tag) not in vtb:
                        vtb[(u'END', tag)] = {}
                        vtb[(u'END', tag)][tag] = probability
                    else:
                        vtb[(u'END', tag)][tag] = probability
        vtbs.append(vtb)
        vtb = collections.OrderedDict()
    print vtbs[0]
    print vtbs[1]


viterbi(em, tr, testing_sents)
print time.time() - tick