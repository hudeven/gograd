#-*-coding:utf-8-*-

import os, re
from urllib import urlretrieve

def obtainImage(url, out_folder):
    filename = url.split("/")[-1]
    outpath = os.path.join(out_folder, filename)
    if url.lower().startswith("http"):
        urlretrieve(url, outpath)
        return outpath
    else:
        print "Http Head Required"
        return None

#Longest common subsequence
def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result

#Longest common substring
def long_substr(data):
    if not data : return None
    substr = ''
    for i in range(len(data[0])):
        for j in range(len(data[0])-i+1):
            if j > len(substr) and is_substr(data[0][i:i+j], data):
                substr = data[0][i:i+j]
    return substr

def is_substr(find, data):
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True

def findKeywords(sentence, keywords, flag, antiLink = False):
    if antiLink and re.match(r'\$.*\$.*', sentence, flag):
        #print "Sorry, antiLink:", sentence
        return []
    results = []
    sentence = re.sub(r'\s[\s]+', ' ', sentence)
    for each in keywords:
        eachReg = re.sub(r' ', '.', each)
        eachReg = re.sub(r'[^a-zA-Z0-9]', '.', eachReg)
        eachReg = r'.*' + eachReg + r'.*'
        if re.match(eachReg, sentence, flag):
            if len(sentence.strip().split(' '))<=3:   # if at most 3 words in a line!!
                results.append(re.sub(r'\$', ' ', sentence).strip()) #because hyperlink is in format of $<..>$
            else: results.append(each)
            #print sentence, " matches ", eachReg, " from ", each
    return results
