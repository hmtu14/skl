from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import random
import nltk
import csv
import spacy



# List 
skill_grammar = nltk.data.load('list_skill_grammar.cfg')

sentences = list(generate(skill_grammar,depth=7))
print(len(sentences))
samples = random.sample(sentences, 20)
for sample in samples:
    print(' '.join(sample))


# sent = sentences[random.randint(0,len(sentences)-1)]
# print(" ".join(sent))
# for word in sent:
#     print(skill_grammar.productions(rhs=word))