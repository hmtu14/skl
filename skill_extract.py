import csv
import time
import re
import os
import threading
from nltk.corpus import stopwords
import spacy
import itertools


list_remove = ["&amp;"]
pause_flag = False

stopWords = set(stopwords.words('english'))
skill_dict = [] #skill with more than 2 word
all_skill_dict = []
nlp = spacy.load('en_core_web_md')
skl_data = []


with open("skl.csv","r", encoding="utf8") as inputf:
    reader = csv.reader(inputf)
    for line in reader:
        skl_data.append(line)

with open("Skills.txt", "r") as inputf:
    reader = inputf.readlines()
    for line in reader:
        if len(line.split("-")) > 1:
            try:
                for item in line.split("-"):
                    float(item)
            except:
                skill_dict.append(line)
        all_skill_dict.append(line.replace("-"," ").strip())

class pauseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global pause_flag
        while True:
            input()
            pause_flag = True
            print("Paused")
            input()
            pause_flag = False
            print("Resumed")



def is_bullet(s):    
    bullet_pattern = r'\\x[0-9a-f]{2}|\\u[0-9a-f]{4}'    
    if len(s.strip()) == 1:        
        s = s.encode('unicode_escape').decode('utf-8')        
        m = re.fullmatch(bullet_pattern, s)        
        return m != None    
    return False

def remove_newline(para):
    for i in range(len(para)):
        if (i >= len(para)):
            return para
        char = para[i]
        if char == "\n":
            try:
                prev_para = para[:i].strip()
                next_para = para[i+1:].strip()
                #If - or o is bullet:
                if next_para[0] == "o" or next_para == "-" or next_para == "+":
                    if next_para[1:].strip()[0].isupper():
                        para = para[:i] + "^" + para[i+1:]
                    continue
                #If ,
                if (prev_para[len(prev_para)-1] == ","):
                    para = para[:i] + " " + para[i+1:]
                    continue
                #No upper
                if (next_para[0].islower()):
                    para = para[:i] + " " + para[i+1:]
                    continue
                #stopwords
                if (prev_para.split(" ")[len(prev_para.split(" "))-1] in stopWords):
                    para = para[:i] + " " + para[i+1:]
                    continue
                #&
                if (prev_para[len(prev_para)-1] == "&"):
                    para = para[:i] + " " + para[i+1:]
                    continue
                #Skill splitted:
                tmp1 = prev_para.split(" ")
                tmp2 = next_para.split(" ")
                for skill in skill_dict:
                    if (tmp1[len(tmp1)-1].strip().lower() in skill) and (tmp2[0].strip().lower() in skill):
                        para = para[:i] + " " + para[i+1:]
                        continue
            except:
                continue
            #Tach dong:
            para = para[:i] + "^" + para[i+1:]

    return para

def remove_bullet(para):
    for char in para:
        if is_bullet(char):
            para = para.replace(char, "^")
    return para

def split_newline(para):
    for i in range(len(para)):
        if (i >= len(para)):
            return para
        char = para[i]
        if char == ".":
            prev_para = para[:i].strip()
            next_para_raw = para[i+1:]
            next_para = para[i+1:].strip()
            # .net
            try:
                if (next_para_raw[0:3].lower() == "net"):
                    continue
            except:
                pass
            #num.num
            try:
                if (prev_para[len(prev_para) -1].isdigit() and next_para[0].isdigit ):
                    continue
            except:
                pass
            #No uppercase
            try:
                if (next_para[0].islower()):
                    continue
            except:
                pass

            para = para[:i] + "^" + para[i+1:]
    return para

def split_and_comma(block):
    for i in block.split(","):
        for it in i.split("and"):
            yield it

def skill_ext(block):
    #Pre-process
    block = block.strip()
    block = block.replace(",", " , ") # split ,
    block = re.sub(' +',' ',block) #remove duplicate space
    #If :
    if (":" in block):
        idx = block.find(":")
        content = block[idx+1:]
        return True, list(split_and_comma(content))
    #If list skill splited by ,:
    if ("," in block):
        #Find ADP
        ADP = ""
        doc = nlp(block)
        for token in doc:
            if (token.pos_ == "ADP"):
                ADP = token.text
                break
        #If no ADP
        if (ADP == ""):
            return True, list(split_and_comma(block))
        #If there's ADP:
        #Find the nearest ADP to ,:
        ADP = ""
        for token in doc:
            if (token.pos_ == "ADP"):
                ADP = token.text
            if (token.pos_ == "PUNCT"):
                break
        idx = block.find(ADP)      #Need to fix: sometime find not correct
        block = block[idx+1+len(ADP):]
        return True, list(split_and_comma(block))
    else:
        return False, block

def skill_extracter(para):
    res = {}
    res["Content"] = para
    res["Skill"] = []
    res["Other"] = []
    para = remove_newline(para)
    para = remove_bullet(para)
    para = split_newline(para)
    for block in para.split("^"):
        if block.strip() == "":
            continue
        bl, result = skill_ext(block)
        if bl:
            res["Skill"].extend(result)
        else:
            res["Other"].append(result)
    return res


def test_parse_tree(block):
    doc = nlp(block)
    for token in doc:
        print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])


Thread = pauseThread()
Thread.start()
for i in range(250,len(skl_data)):
    para = skl_data[i][0]
    para = remove_newline(para)
    para = remove_bullet(para)
    para = split_newline(para)
    for block in para.split("^"):
        if block.strip() == "":
            continue
        print(block)
        print("----------")
        test_parse_tree(block.strip())
        print("========================================================")
    print(i)
    time.sleep(5)
    while (pause_flag):
        time.sleep(0.1)
    os.system("cls")