#%pip install hazm

from __future__ import unicode_literals
from hazm import *
import codecs
import json
import collections

print('#part 1')
#f = open('foo.json')
f = open('IR_data_news_12k.json')
data = json.load(f)
f.close()

contents = []
for i in data:
    tmp = data[i]['content']
    contents.append(tmp[0:len(tmp)-16])
#print('#1')
#for i in contents:
#    print(i)
#print()

normalizer = Normalizer()
for i in range(len(contents)):
    contents[i] = normalizer.normalize(contents[i])
#print('#2')
#for i in contents:
#    print(i)

tokens = []
for i in range(len(contents)):
    tokens.append(word_tokenize(contents[i]))
#print('#3')
#for i in tokens:
#    print(i)
#    print()

lemmatizer = Lemmatizer()
for i in range(len(tokens)):
    for j in range(len(tokens[i])):
        tokens[i][j] = lemmatizer.lemmatize(tokens[i][j])
#print('#4')
#for i in tokens:
#    print(i)
#    print()

"""
stemmer = Stemmer()
for i in range(len(tokens)):
    for j in range(len(tokens[i])):
        tokens[i][j] = stemmer.stem(tokens[i][j])
print('#5')
for i in tokens:
    print(i)
    print()
"""

f = codecs.open('stopwords.dat', encoding='utf-8')
stopWords = []
for l in f.readlines():
    stopWords.append(l.strip('\n'))
f.close()
#print('A#')
#print(stopWords)
#print()

for i in range(len(stopWords)):
    stopWords[i] = normalizer.normalize(stopWords[i])
#print('B#')
#print(stopWords)
#print()

for i in range(len(stopWords)):
    stopWords[i] = lemmatizer.lemmatize(stopWords[i])
#print('C#')
#print(stopWords)
#print()

tmpTokens = []
for i in range(len(tokens)):
    tmpTokensDoc = []
    for j in range(len(tokens[i])):
        if(tokens[i][j] not in stopWords): tmpTokensDoc.append(tokens[i][j])
    tmpTokens.append(tmpTokensDoc)
tokens = tmpTokens.copy()
#print('#5')
#for i in tokens:
#    for j in i:
#        print(j)
#    print('\n+++++\n')
#print()

print('#part 2')
#uniqueTokens = set()
#for i in tokens:
#    for j in i:
#        uniqueTokens.add(j)
#sortedTokens = []
#sortedTokens = sorted(list(uniqueTokens))
#print('#6')
#for i in sortedTokens:
#    print(i)
#print()

positionalIndex = {}
for j in range(len(tokens)):
    for k in range(len(tokens[j])):
        token = tokens[j][k]
        if(token in positionalIndex):
            oldDocFrequency = positionalIndex[token][0]
            oldFrequencyInDoc = positionalIndex[token][1].copy()
            oldPositionsInDoc = positionalIndex[token][2].copy()
            if(j in oldFrequencyInDoc):
                oldFrequencyInDoc[j] += 1
                oldPositionsInDoc[j].append(k)
                positionalIndex[token] = (oldDocFrequency, oldFrequencyInDoc.copy(), oldPositionsInDoc.copy())
            else:
                a = oldFrequencyInDoc.copy()
                b = oldPositionsInDoc.copy()
                a[j] = 1
                b[j] = [k]
                positionalIndex[token] = (oldDocFrequency+1, a.copy(), b.copy())
        else:
                a = dict()
                b = dict()
                a[j] = 1
                b[j] = [k]
                positionalIndex[token] = (1, a.copy(), b.copy())
positionalIndex = collections.OrderedDict(sorted(positionalIndex.items())).copy()
#print('#7')
#print(positionalIndex['گیتی'])

#print('#part 3')
import sys
print('Enter your query: ', end = '')
query = input()
print()

termsInQuery = []
query = normalizer.normalize(query)
termsInQuery = word_tokenize(query).copy()

for i in range(len(termsInQuery)):
    termsInQuery[i] = lemmatizer.lemmatize(termsInQuery[i])

tmp = []
for i in termsInQuery:
    if(i not in stopWords or i == '!' or i == '"' or i == '»' or i == '«'): tmp.append(i)
termsInQuery = tmp.copy()

#print('#8')
#for i in termsInQuery:
#    print(i)
#print()

for i in termsInQuery:
    if i not in positionalIndex and i != '!' and i != '"' and i != '»' and i != '«':
        print('No Match Found!')
        sys.exit()

mustInclude = []
mustNotInclude = []
phrases = []
negative = 0
phrase = 0
tmpPhrase = []
for i in termsInQuery:
    if i == '!':
        negative = 1
        continue
    elif i == '«':
        phrase = 1
        continue
    elif i == '»':
        phrases.append(tmpPhrase)
        tmpPhrase = []
        phrase = 0
        continue
    elif negative == 1:
        mustNotInclude.append(i)
        negative = 0
        continue
    elif phrase == 1:
        tmpPhrase.append(i)
        continue
    mustInclude.append(i)

#print('#9')
#for i in mustInclude:
#    print(i)
#print('+++++')
#for i in mustNotInclude:
#    print(i)
#print('+++++')
#for i in phrases:
#    print(i)
#print()

tmp = []
phraseAppearances = []
if len(phrases) > 0:
    for i in phrases:
        pSumAppearances = dict()
        if len(i) > 0: pSumAppearances = positionalIndex[i[0]][1].copy()
        for j in range(len(i)-1):
            a = pSumAppearances.copy()
            b = positionalIndex[i[j+1]][1].copy()
            pSumAppearances = {z: a.get(z, 0) + b.get(z, 0) for z in set(a) & set(b)}
        pSumAppearances = collections.OrderedDict(sorted(pSumAppearances.items())).copy()
        tmp.append(pSumAppearances)
        phraseAppearances.append(dict())
    for i in range(len(tmp)):
        for j in tmp[i]:
            dummy = []
            for k in phrases[i]:
                dummy.append(positionalIndex[k][2][j])
            for k in dummy[0]:
                continueFlag = 0
                for l in range(len(dummy)-1):
                    if (k+l+1) not in dummy[l+1]:
                        continueFlag = 1
                        break
                if continueFlag == 1: continue
                if j in phraseAppearances[i]: phraseAppearances[i][j] += 1
                else: phraseAppearances[i][j] = 1

#print('#10')
#for i in phraseAppearances:
#    print(i)
#    print(len(i))
#    print()
#print()

sumAppearances = dict()
if len(mustInclude) > 0: sumAppearances = positionalIndex[mustInclude[0]][1].copy()
for i in range(len(mustInclude)-1):
    a = sumAppearances.copy()
    b = positionalIndex[mustInclude[i+1]][1].copy()
    sumAppearances = {z: a.get(z, 0) + b.get(z, 0) for z in set(a) | set(b)}
sumAppearances = collections.OrderedDict(sorted(sumAppearances.items())).copy()

allAppearances = dict()
if len(phrases) > 0: allAppearances = phraseAppearances[0].copy()
for i in range(len(phrases)-1):
    a = allAppearances.copy()
    b = phraseAppearances[i+1].copy()
    allAppearances = {z: a.get(z, 0) + b.get(z, 0) for z in set(a) | set(b)}
allAppearances = {z: allAppearances.get(z, 0) + sumAppearances.get(z, 0) for z in set(allAppearances) | set(sumAppearances)}
allAppearances = collections.OrderedDict(sorted(allAppearances.items())).copy()

varietyAppearances = dict()
for i in allAppearances:
    nAppearances = 0
    for j in mustInclude:
        if i in positionalIndex[j][1]: nAppearances += 1
    for j in range(len(phrases)):
        if i in phraseAppearances[j]: nAppearances += 1
    varietyAppearances[i] = nAppearances
varietyAppearances = collections.OrderedDict(sorted(varietyAppearances.items())).copy()

result = []
tmp = []
for i in range(len(mustInclude)+len(phrases)):
    result.append(list())
    tmp.append(list())
for i in allAppearances:
    result[len(mustInclude)+len(phrases)-varietyAppearances[i]].append(i)
for i in range(len(result)):
    dummy = dict()
    for j in result[i]:
        dummy[j] = allAppearances[j]
    tmp[i] = list(dict(sorted(dummy.items(), key=lambda item: item[1])).keys()).copy()
    tmp[i].reverse()
result = tmp.copy()

if len(mustNotInclude) != 0:
    tmp = []
    for i in range(len(mustInclude)+len(phrases)):
        tmp.append(list())
    for i in mustNotInclude:
        for j in range(len(result)):
            for k in result[j]:
                if k not in positionalIndex[i][1]: tmp[j].append(k)
    result = tmp.copy()

#print('#11')
#for i in result:
#    print(i)
#    print(len(i))
#    print()
#print()

res = []
for i in result:
    for j in i:
        res.append(j)
if len(res) == 0: print('No Match Found!')
else:
    i = 0
    while i < min(5, len(res)):
        print(f'Retrieved Doc #{i+1} with DocID #{res[i]}:')
        a = data[str(res[i])]['title']
        b = data[str(res[i])]['url']
        print(f'Title: {a}')
        print(f'URL: {b}')
        print()
        i += 1

print('#phase 2')
import math

allTerms = list(positionalIndex.keys())

docVectors = []
for i in range(12202):
    tmp = []
    for t in allTerms:
        if(i not in positionalIndex[t][1]):
            tmp.append(0)
            continue
        f = positionalIndex[t][1][i]
        tf = 1 + math.log(f, 10)
        idf = math.log(12202/positionalIndex[t][0], 10)
        tfidf = tf * idf
        tmp.append(tfidf)
    docVectors.append(tmp)

print('Enter your query: ', end = '')
query = input()
print()
termsInQuery = []
query = normalizer.normalize(query)
termsInQuery = word_tokenize(query).copy()
for i in range(len(termsInQuery)):
    termsInQuery[i] = lemmatizer.lemmatize(termsInQuery[i])
tmp = []
for i in termsInQuery:
    if(i not in stopWords or i == '!' or i == '"' or i == '»' or i == '«'): tmp.append(i)
termsInQuery = tmp.copy()
for i in termsInQuery:
    if i not in positionalIndex and i != '!' and i != '"' and i != '»' and i != '«':
        print('No Match Found!')
        sys.exit()

#print('#1')
#for i in termsInQuery:
#    print(i)
#print()

queryVector = []
for t in allTerms:
    if(t not in termsInQuery):
        queryVector.append(0)
        continue
    cnt = 0
    for j in termsInQuery:
        if(t == j): cnt += 1
    f = cnt
    tf = 1 + math.log(f, 10)
    idf = math.log(12202/positionalIndex[t][0], 10)
    tfidf = tf * idf
    queryVector.append(tfidf)

#print('#2')
#for i in range(len(allTerms)):
#    print(f'{allTerms[i]} ==> {queryVector[i]}')

uniqueTermsInQuery = set()
for i in termsInQuery:
    uniqueTermsInQuery.add(i)
uniqueTermsInQuery = list(uniqueTermsInQuery)

def method1(a, b):
    dotProduct = 0
    for i in range(len(a)):
        dotProduct += a[i] * b[i]
    absA = 0
    absB = 0
    for i in range(len(a)):
        absA += a[i] * a[i]
        absB += b[i] * b[i]
    absA = math.sqrt(absA)
    absB = math.sqrt(absB)
    return dotProduct/(absA*absB)

def method2(a, b):
    c = 0.0
    for i in range(len(a)):
        if(a[i]!=0 and b[i]!=0): c+=1
    d = 0.0
    for i in range(len(a)):
        if(a[i]!=0 or b[i]!=0): d+=1
    if(d == 0): return 0
    return c/d

similarities1 = []
similarities2 = []
for i in range(len(docVectors)):
    similarities1.append(method1(queryVector, docVectors[i]))
    #similarities2.append(method2(queryVector, docVectors[i]))

K = 5
import heapq
res1 = heapq.nlargest(K, range(len(similarities1)), key=similarities1.__getitem__).copy()
#res2 = heapq.nlargest(K, range(len(similarities2)), key=similarities2.__getitem__).copy()

print('Method1:')
print('--------')
i = 0
while i < K:
    print(f'Retrieved Doc #{i+1} with DocID #{res1[i]}:')
    a = data[str(res1[i])]['title']
    b = data[str(res1[i])]['url']
    print(f'Title: {a}')
    print(f'URL: {b}')
    print()
    i += 1
"""
print('Method2:')
print('--------')
i = 0
while i < K:
    print(f'Retrieved Doc #{i+1} with DocID #{res2[i]}:')
    a = data[str(res2[i])]['title']
    b = data[str(res2[i])]['url']
    print(f'Title: {a}')
    print(f'URL: {b}')
    print()
    i += 1"""