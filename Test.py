import HMM
import nltk
from nltk.corpus import brown

# Get test set
sents = brown.tagged_sents(tagset = 'universal')
test_length = len(sents) - HMM.train_length + 1
print test_length
test_sents = []

start = (u'<s>', u'START')
end = (u'</s>', u'END')

# Add start and end tag
for sent in sents[test_length: len(sents)]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    test_sents.append(sent)


# Get emission and transition
# emissions = HMM.emission_probability()
# transitions = HMM.transition_probability()
