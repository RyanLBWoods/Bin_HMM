import nltk
import json
import time
from nltk.corpus import brown


# Process training set
def process_training_set():
    sents = brown.tagged_sents(tagset='universal')  # Get training set
    train_length = int(0.1 * len(sents))  # Define size of training set
    training_sents = []
    # Add start and end of sentence tags
    start = (u'<s>', u'START')
    end = (u'</s>', u'END')
    for sent in sents[0: len(sents) - train_length]:
        list.insert(sent, 0, start)
        list.append(sent, end)
        training_sents.append(sent)
    return training_sents


"""
Calculate emission
1. Get frequency for each word
2. Get frequency of each word being tagged as "tag"
3. Get frequency of each tag
3. Calculate emission probabilities (P(word | tag) = C(word, tag) / C(tag))
"""


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


def emission_probability(train_sents):
    ep = {}
    tf = tagged_freq(train_sents)
    tag_count = tags_freq(train_sents)
    for word in tf:
        ep[word] ={}
        for tag in tf[word]:
            ep[word][tag] = tf[word][tag] / (1.0 * tag_count[tag])
    return ep


def unk_emission(train_sents):
    wf = word_freq(train_sents)
    tf = tagged_freq(train_sents)
    unk = []
    unk_tags_freq = {u'UNK': {}}
    unk_em = {u'UNK': {}}
    tag_count = tags_freq(train_sents)
    # Collect word that appears only once
    # Mark as UNK
    print "Collecting UNK..."
    for key in wf:
        if wf[key] == 1:
            unk.append(key)
            # Collect tag frequencies for UNK
            for tag in tf[key]:
                if tag not in unk_tags_freq[u'UNK']:
                    unk_tags_freq[u'UNK'][tag] = 1
                else:
                    unk_tags_freq[u'UNK'][tag] += 1
    # Calculate emission probability of UNK
    print "Calculating emission probability of UNK..."
    for unk_tag in unk_tags_freq[u'UNK']:
        unk_em[u'UNK'][unk_tag] = unk_tags_freq[u'UNK'][unk_tag] / (1.0 * len(unk))
    return unk_em


# Add emission probability of UNK to emission dictionary
def emission_with_unk(train_sents):
    em = emission_probability(train_sents)
    unk_prob = unk_emission(train_sents)[u'UNK']
    em[u'UNK'] = unk_prob
    return em


"""
Calculate transition
1. Get tag frequencies
2. Get tag pairs
3. Calculate frequencies of pairs
4. Calculate transition probabilities (Apply Laplace smoothing)
P(to | from) = (C(from, to) + k )/ C(from) + V
"""


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
    print "Establishing transition probability matrix..."
    for tag1 in tag_freq:
        for tag2 in tag_freq:
            if tag1 in pairs_freq and tag2 in pairs_freq[tag1]:
                tag_maxtrix[tag1, tag2] = pairs_freq[tag1][tag2]
            else:
                tag_maxtrix[tag1, tag2] = 0
    # Fill in transitions
    print "Calculating transition probabilities..."
    for tag_pair in tag_maxtrix:
        pair_str = str(tag_pair)
        trans_pro[pair_str] = (tag_maxtrix[tag_pair] + k) / (1.0 * (tag_freq[tag_pair[0]] + tag_num * k))
    return trans_pro


# Save model to JSON file
def save_model(training_sents):
    # Calculate emission and transition probabilities
    print "Training..."
    em_model = emission_with_unk(training_sents)
    tr_model = transition_probability(training_sents)

    # Write emission and transition probabilities to file
    print "Saving model..."
    emission_file = open('Emission.json', 'w')
    # Convert to JSON
    em_obj = json.dumps(em_model)
    emission_file.write(em_obj)
    emission_file.close()

    transition_file = open('Transition.json', 'w')
    # Convert to JSON
    tr_obj = json.dumps(tr_model)
    transition_file.write(tr_obj)
    transition_file.close()
    print "Model saved."


start_tick = time.time()
print "Processing training set..."
training_sents = process_training_set()
save_model(training_sents)
print "Time used: ", time.time() - start_tick
