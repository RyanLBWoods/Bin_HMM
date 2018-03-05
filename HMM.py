import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import brown
from nltk import FreqDist
from nltk import ConditionalFreqDist

sents = brown.tagged_sents(tagset = 'universal')
train_length = 2
start = (u'<s>', u'START')
end = (u'</s>', u'END')
for sent in sents[0:train_length]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    # print len(sent)
# print sents[0]
# words = [w for (w, _) in sents[0]]
# tags = [t for (_, t) in sents[0]]
# print words

# print tags
# pair = [(w, t) for w in words for t in tags]
# i = ConditionalFreqDist(pair)
# print i
# print "conditions are", i.conditions()
# print i / (1.0 * len(sents[0]))
# print list(nltk.bigrams(tags))
# print list(nltk.bigrams(words))
"""
Calculate emission
1. Get frequency for each word
2. Get frequency of each word being tagged as XX
3. Calculate emission
"""
# Count words frequency
def word_freq():
    word_frequencies = {}
    for sent in sents[0:train_length]:
        words = [w for (w, _) in sent]
        tags = [t for (_, t) in sent]
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] + 1
            else:
                word_frequencies[word] = 1
    return word_frequencies

def tag_freq():
    tag_frequencies = {}
    for sent in sents[0:train_length]:
        for token in sent:
            if token[0] not in tag_frequencies:
                tag_frequencies[token[0]] = {}
                tag_frequencies[token[0]][token[1]] = 1
            else:
                if token[1] in tag_frequencies[token[0]]:
                    tag_frequencies[token[0]][token[1]] += 1
                else:
                    tag_frequencies[token[0]][token[1]] = 1
    return tag_frequencies

def emission_probability():
    ep = {}
    tf = tag_freq()
    wf = word_freq()
    for sent in sents[0:train_length]:
        for token in sent:
            if token[0] not in ep:
                ep[token[0]] = {}
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
            else:
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
    return ep

def tag_pair():
    tag_pairs = []
    for sent in sents[0: train_length]:
        tags = [t for (_, t) in sent]
        tp = list(nltk.bigrams(tags))
        tag_pairs.append(tp)
    print tag_pairs
    return tag_pairs

tag_pair()
# def word_tagged():
#     wt = {}
#     for sent in sents[0:train_length]:
#         words = [w for (w, _) in sent]
#         tags = [t for (_, t) in sent]
#         for word in words:
#             word_tag = word[word.rfind("/") + 1:len(word)]
#             # word_not_tag = word[0:word.rfind("/")]
#             # print word_tag
#             # print word_not_tag
#             # if word_tag in
#
# # word_tagged()
#
#
#
# # print e_p

def transition_probability():
    tp = {}
    for sent in sents[0:train_length]:
        list.insert(sent, 0, start)
        list.append(sent, end)
        words = [w for (w, _) in sent]
        tags = [t for (_, t) in sent]
        bi_tags = list(nltk.bigrams(tags))
        print sent
        for tag in tags:
            print tag, FreqDist(tag)
        # print FreqDist(u'START')
        # print sent
        # print u'START', FreqDist(u'START')
        # for tag in tags:
            # count = FreqDist(tag)
            # print tag, count
        # print words
        # print bi_tags[0]
        # for bi_tag in bi_tags:
        #     print bi_tag

        # print sent

# def emission_probability():
#     ep = {}
#     for sent in sents[0:train_length]:
#         list.insert(sent, 0, start)
#         list.append(sent, end)
#         words = [w for (w, _) in sent]
#         tags = [t for (_, t) in sent]
#         for word in words:
#             emission = FreqDist()

# transition_probability()