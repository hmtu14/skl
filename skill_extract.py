import csv
import time
import re
import os
import threading
from nltk.corpus import stopwords


skl_data = []
list_remove = ["&amp;"]
pause_flag = False

stopWords = set(stopwords.words('english'))
skill_dict = []

with open("SKL_data.csv", "r", encoding='utf8') as inputf:
    reader = csv.reader(inputf)
    for line in reader:
        skl_data.append(line)

with open("SKL_data.csv", "r") as inputf:
    reader = inputf.readlines()
    for line in reader:
        if len(line.split("-")) > 1:
            skill_dict.append(line)

# with open("train.csv", "r", encoding='utf8') as inputf:
#     reader = csv.reader(inputf)
#     for line in reader:
#         if (line[1].replace('"','') == "SKL"):
#             SKL_data.append(line)

# with open("SKL_data.csv", "w", encoding='utf8') as outputf:
#     writer = csv.writer(outputf)
#     for line in SKL_data:
#         writer.writerow(line)


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
            prev_para = para[:i].strip()
            next_para = para[i+1:].strip()

            #If - or o is bullet:
            if next_para[0] == "o" or next_para == "-" or next_para == "+":
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
            for skill in skill_dict:
                if (prev_para.split(" ")[len(prev_para.split(" "))-1].strip().lower() in skill) and (next_para.split(" ")[0].strip().lower() in skill):
                    print(prev_para.split(" ")[len(prev_para.split(" "))-1].strip().lower())
                    print("$$$$$$$$")
                    print(next_para.split(" ")[0].strip().lower())
                    para = para[:i] + " " + para[i+1:]
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


pauseT = pauseThread()
pauseT.start()
for i in range(67,68):
    para = skl_data[i][0]
    para = remove_newline(para)
    para = remove_bullet(para)
    para = split_newline(para)
    for block in para.split("^"):
        if block.strip() == "":
            continue
        print(block)
        print("========================================================")
    print(i)
    time.sleep(0)
    while (pause_flag):
        time.sleep(0.1)
    # os.system("clear")
    

