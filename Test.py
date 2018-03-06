import HMM
import nltk
from nltk.corpus import brown


# Pre-processing training and testing sets
sents = brown.tagged_sents(tagset='universal')  # Get training set
# train_length = len(sents) / 2  # Define size of training set
train_length = 100
training_sents = []
test_length = len(sents) - train_length + 1
test_sents = []
# Add start and end tag
start = (u'<s>', u'START')
end = (u'</s>', u'END')
for sent in sents[0: train_length]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    training_sents.append(sent)

for sent in sents[test_length: len(sents)]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    test_sents.append(sent)


# Get emission and transition
emissions = HMM.emission_with_UNK(training_sents)
transitions = HMM.transition_probability(training_sents)
print len(emissions)
print len(transitions)
