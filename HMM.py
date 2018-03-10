import nltk
import json
from nltk.corpus import brown

"""
Calculate emission
1. Get frequency for each word
2. Get frequency of each word being tagged as XX
3. Calculate emission
"""

sents = brown.tagged_sents(tagset='universal')  # Get training set
# train_length = len(sents) / 2  # Define size of training set
train_length = 1000
training_sents = []
start = (u'<s>', u'START')
end = (u'</s>', u'END')
for sent in sents[0: train_length]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    training_sents.append(sent)


def word_freq(train_sents):
    word_frequencies = {}
    for sent in train_sents:
        words = [w for (w, _) in sent]
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] + 1
            else:
                word_frequencies[word] = 1
    return word_frequencies


def tagged_freq(train_sents):
    tag_frequencies = {}
    for sent in train_sents:
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


def emission_probability(train_sents):
    i = 0
    ep = {}
    tf = tagged_freq(train_sents)
    wf = word_freq(train_sents)
    for sent in train_sents:
        for token in sent:
            if token[0] not in ep:
                ep[token[0]] = {}
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
            else:
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
    return ep


def unk_emission(train_sents):
    wf = word_freq(train_sents)
    unk = []
    unk_sent = []
    unk_sents = []
    unk_em = {}
    for key in wf:
        if wf[key] == 1:
            unk.append(key)
    print "done unk words"
    print len(train_sents)
    for sent in train_sents:
        for token in sent:
            if token[0] in unk:
                unknown = (u'UNK', token[1])
                unk_sent.append(unknown)
            else:
                unk_sent.append(token)
        unk_sents.append(unk_sent)
        unk_sent = []
    print "done change sent"
    unk_tf = tagged_freq(unk_sents)
    unk_wf = word_freq(unk_sents)
    for unsent in unk_sents:
        for untk in unsent:
            if untk[0] == 'UNK':
                if untk[0] not in unk_em:
                    unk_em[untk[0]] = {}
                    unk_em[untk[0]][untk[1]] = unk_tf[untk[0]][untk[1]] / (1.0 * unk_wf[untk[0]])
                else:
                    unk_em[untk[0]][untk[1]] = unk_tf[untk[0]][untk[1]] / (1.0 * unk_wf[untk[0]])
    return unk_em


def emission_with_unk(train_sents):
    em = emission_probability(train_sents)
    unk_prob = unk_emission(train_sents)['UNK']
    em['UNK'] = unk_prob
    return em


"""
Calculate transition
1. Get tag frequencies
2. Get tag pairs
3. Calculate frequencies of pairs
4. Calculate transition
"""


def tags_freq(train_sents):
    tags_frequencies = {}
    for sent in train_sents:
        tags = [t for (_, t) in sent]
        for tag in tags:
            if tag in tags_frequencies:
                tags_frequencies[tag] += 1
            else:
                tags_frequencies[tag] = 1
    return tags_frequencies


def tag_pairs(train_sents):
    tag_pairs = []
    for sent in train_sents:
        tags = [t for (_, t) in sent]
        pairs = list(nltk.bigrams(tags))
        tag_pairs.extend(pairs)
    return tag_pairs


def pair_freq(train_sents):
    tp = tag_pairs(train_sents)
    pf = {}
    for token in tp:
        if token[0] not in pf:
            pf[token[0]] = {}
            pf[token[0]][token[1]] = 1
        else:
            if token[1] in pf[token[0]]:
                pf[token[0]][token[1]] += 1
            else:
                pf[token[0]][token[1]] = 1
    return pf


# Calculate transition probability
# Apply Laplace smoothing (k = 1)
def transition_probability(train_sents):
    trans_pro = {}
    k = 1
    tag_freq = tags_freq(train_sents)
    tag_num = len(tag_freq)
    pairs_freq = pair_freq(train_sents)
    tag_maxtrix = {}
    # Build transition matrix
    print len(tag_freq)
    for tag1 in tag_freq:
        for tag2 in tag_freq:
            if (tag1, tag2) in pairs_freq:
                tag_maxtrix[tag1, tag2] = pairs_freq[tag1, tag2]
            else:
                tag_maxtrix[tag1, tag2] = 0
    # Fill in transitions
    for tag_pair in tag_maxtrix:
        pair_str = str(tag_pair)
        trans_pro[pair_str] = (tag_maxtrix[tag_pair] + k) / (1.0 * (tag_freq[tag_pair[0]] + tag_num * k))
    print trans_pro
    return trans_pro


def save_model():
    emission_file = open('Emission.json', 'w')
    em_model = emission_with_unk(training_sents)
    em_obj = json.dumps(em_model)
    emission_file.write(em_obj)
    emission_file.close()

    transition_file = open('Transition.json', 'w')
    tr_model = transition_probability(training_sents)
    tr_obj = json.dumps(tr_model)
    transition_file.write(tr_obj)
    transition_file.close()
    print "Model saved."


save_model()
