import nltk

"""
Calculate emission
1. Get frequency for each word
2. Get frequency of each word being tagged as XX
3. Calculate emission
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


def emission_probability(train_sents):
    ep = {}
    # tf = tagged_freq(train_sents)
    # wf = word_freq(train_sents)
    tag_frequencies = {}
    word_frequencies = {}

    for sent in train_sents:
        # Word frequency
        words = [w for (w, _) in sent]
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] + 1
            else:
                word_frequencies[word] = 1
        for token in sent:
            # Tagged frequency
            if token[0] not in tag_frequencies:
                tag_frequencies[token[0]] = {}
                tag_frequencies[token[0]][token[1]] = 1
            else:
                if token[1] in tag_frequencies[token[0]]:
                    tag_frequencies[token[0]][token[1]] += 1
                else:
                    tag_frequencies[token[0]][token[1]] = 1
            # Emission
            if token[0] not in ep:
                ep[token[0]] = {}
                ep[token[0]][token[1]] = tag_frequencies[token[0]][token[1]] / (1.0 * word_frequencies[token[0]])
            else:
                ep[token[0]][token[1]] = tag_frequencies[token[0]][token[1]] / (1.0 * word_frequencies[token[0]])
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
    for sent in train_sents:
        for token in sent:
            if token[0] in unk:
                unknown = (u'UNK', token[1])
                unk_sent.append(unknown)
            else:
                unk_sent.append(token)
        unk_sents.append(unk_sent)
    # unk_tf = tagged_freq(unk_sents)
    # unk_wf = word_freq(unk_sents)
    unk_wf = {}
    unk_tf = {}
    for unsent in unk_sents:
        # Word frequency
        words = [w for (w, _) in unsent]
        for word in words:
            if word in unk_wf:
                unk_wf[word] = unk_wf[word] + 1
            else:
                unk_wf[word] = 1
        for untk in unsent:
            # Tagged frequency
            if untk[0] not in unk_tf:
                unk_tf[untk[0]] = {}
                unk_tf[untk[0]][untk[1]] = 1
            else:
                if untk[1] in unk_tf[untk[0]]:
                    unk_tf[untk[0]][untk[1]] += 1
                else:
                    unk_tf[untk[0]][untk[1]] = 1
            # Calculate UNK emissions
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


def tag_pair(train_sents):
    tag_pairs = []
    for sent in train_sents:
        tags = [t for (_, t) in sent]
        pairs = list(nltk.bigrams(tags))
        tag_pairs.extend(pairs)
    return tag_pairs


def pair_freq(train_sents):
    tp = tag_pair(train_sents)
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

    tags_frequencies = {}
    tag_pairs = []

    for sent in train_sents:
        # Tags frequencies
        tags = [t for (_, t) in sent]
        for tag in tags:
            if tag in tags_frequencies:
                tags_frequencies[tag] += 1
            else:
                tags_frequencies[tag] = 1
        # Tag pairs
        # tags = [t for (_, t) in sent]
        pairs = list(nltk.bigrams(tags))
        tag_pairs.extend(pairs)
    trans_pro = {}
    k = 1
    # tag_pairs = tag_pair(train_sents)
    # tag_freq = tags_freq(train_sents)
    tag_num = len(tags_frequencies)
    pairs_freq = {}
    for token in tag_pairs:
        if token[0] not in pairs_freq:
            pairs_freq[token[0]] = {}
            pairs_freq[token[0]][token[1]] = 1
        else:
            if token[1] in pairs_freq[token[0]]:
                pairs_freq[token[0]][token[1]] += 1
            else:
                pairs_freq[token[0]][token[1]] = 1
    # pairs_freq = pair_freq(train_sents)
    # for p in tag_pairs:
        if token not in trans_pro:
            trans_pro[token] = (pairs_freq[token[0]][token[1]] + k) / (1.0 * (tags_frequencies[token[0]] + tag_num * k))
    return trans_pro


# Get how many kinds of pairs
def get_pair(train_sents):
    tp = tag_pair(train_sents)
    pairs = []
    for token in tp:
        if token not in pairs:
            pairs.append(token)
    return pairs
