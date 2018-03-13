
# coding: utf-8

# In[1]:


import csv
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import nltk


# In[2]:


#Load spacy model
nlp = spacy.load("en_core_web_md")


# In[3]:


#Read_file
corpus = []
with open("SKL_data.csv","r", encoding="utf8") as inputf:
    reader = csv.reader(inputf)
    for line in reader:
        corpus.append(line[0])


# In[4]:


#CountVectorizer
vectorizer = CountVectorizer(lowercase=False, ngram_range=(1,2))
X = vectorizer.fit_transform(corpus)


# In[5]:


def split_and_comma(block):
    for i in block.split(","):
        for it in i.split("and"):
            yield it


# In[6]:


def parse_NOUN(root, doc):
    res = []
    #Get noun at root:
    #Need update
    for chunk in doc.noun_chunks:
        if root.text == chunk.root.text:
            res.append(chunk)
            break
    #Loop child
    for child in root.children:
        #Can kiem tra them appos voi truong hop () se bi nham thanh appos
        if (child.dep_ == "conj" or child.dep_ == "appos") and (child.pos_ == "NOUN" or child.pos_ == "PROPN"):
            res.extend(parse_NOUN(child,doc))
    return res


# In[8]:


string = "Fluent in French, English and Vietnamese"
doc = nlp(string)

if (string.count(":") > 1):
    print("ERROR")

field = []
level = []
skill = []

for token in doc:
    #If :
    if (":" in token.text):
        #If truoc : la noun:
        #Co the kiem tra them noun nay co phai la root k. Neu la root thi ok, k phai root thi can kiem tra them
        #Example: Programing Languages and Frameworks:
        if (token.head.pos_ == "NOUN" or token.head.pos_ == "PROPN"):
            #Lay noun_chunk:
            noun_chunk = ""
            c_level = ""
            for chunk in doc.noun_chunks:
                if token.head.text == chunk.root.text:
                    noun_chunk = chunk
            #Xac dinh ADJ/field:
            for child in token.head.children:
                if child.dep_ == "amod":
                    c_level += child.text + " "
            field.append(noun_chunk)
            level.append(c_level)
            #Lay list sau do:
            #tim node tiep theo (thuong la appos)
            flag = False
            for child in token.head.children:
                if (child.dep_ == "appos" or child.dep_ == "npadvmod" ) and (child.pos_ == "NOUN" or child.pos_ == "PROPN"):
                    print(child.text)
                    skill.append(parse_NOUN(child,doc))
                    flag = True
            if (not flag):
                skill.append([])
        else:
            #TODO
            print("TODO")
            pass
    if (token.pos_ == "ADP"):
        #Neu la gioi tu
        #Neu head la noun:
        if (token.head.pos_ == "NOUN" or token.head.pos_ == "PROPN"):
            #Lay noun_chunk:
            noun_chunk = ""
            c_level = ""
            for chunk in doc.noun_chunks:
                if token.head.text == chunk.root.text:
                    noun_chunk = chunk
            #Xac dinh ADJ/field:
            for child in token.head.children:
                if child.dep_ == "amod":
                    c_level += child.text + " "
            field.append(noun_chunk)
            level.append(c_level)
            #Get skill:
            #Get skill_start_node:
            for child in token.children:
                if child.dep_ == "pobj":
                    skill_node = child
                    break
            if (skill_node.pos_ == "NOUN" or skill_node.pos_ == "PROPN"):
                skill.append(parse_NOUN(skill_node,doc))
        #Neu head la adj:
        if (token.head.pos_ == "ADJ"):
            c_level = token.head.text
            field.append("")
            level.append(c_level)
            #Get skill:
            #Get skill_start_node:
            for child in token.children:
                if child.dep_ == "pobj":
                    skill_node = child
                    break
            if (skill_node.pos_ == "NOUN" or skill_node.pos_ == "PROPN"):
                skill.append(parse_NOUN(skill_node,doc))


# In[9]:


print(field)
print(level)
print(skill)


# In[ ]:


for chunk in doc.noun_chunks:
    print(chunk)

