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
test_length = len(sents) - 1
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
print em['was']
# print tr


def viterbi(emissions, transitions, test_sents):
    vtb = collections.OrderedDict()
    vtbs = []
    from_list = []
    maxp = 0
    temp_key2 = ''
    for sent in test_sents:
        i = 0
        print "sent:", sent
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
                print vtb
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
            vtbs.append(vtb)
            from_list = []
        print vtb
        vtb = collections.OrderedDict()
    return vtbs


# test = viterbi(em, tr, testing_sents)

def tag_sent():
    vs = viterbi(em, tr, testing_sents)
    tagged_sents = []
    # temp_max = 0
    # temp_max_tag = ''
    # for v in vs:
    #     for w in reversed(v):
    #         for p_tag in v[w]:
    #             if v[w][p_tag] > temp_max:
    #                 temp_max = v[w][p_tag]
    #                 temp_max_tag = p_tag
    #
    #                 exit(0)

tag_sent()
print time.time() - tick