#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this network consist of top 5 weight edge
# secondary associations also retain only the first five values
# conceptual words are not repeated

# codes 02


import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import logging
import nltk
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter


from collections import Counter
from nltk.corpus import stopwords
from nltk import collocations



document = open('./corpus_training_step123.txt', encoding='utf8').read()

tokens = nltk.word_tokenize(document)

#tokens_lower = [w.lower() for w in tokens]

lexicalpos = nltk.pos_tag(tokens)
#print(lexicalpos)
#type(lexicalpos)

noun = [word for (word, tag) in lexicalpos if tag.startswith('N')]          # 获取名词
#print(noun)
# ['screen', 'works', 'rotating', 'vibration', 'vibrator', 'material', 'screen', 'coal', 'petroleum', 'industries', 'screening', 'machine', 'grading', 'removing', 'materials']
#type(noun)
# <class 'list'>

#def func(one_list):
#    return list(set(one_list))
#    
#noun_one = func(noun)      # list去重    
#print(noun_one)
# ['rotating', 'vibrator', 'screen', 'removing', 'industries', 'grading', 'coal', 'petroleum', 'screening', 'machine', 'works', 'vibration', 'material', 'materials']
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!取名词，变量为noun
count1 = Counter(tokens)

count5 = []
for i in count1:
    if (count1[i]>=1):
        count5.append(i)



model=KeyedVectors.load('./word2vec_travelingwave_step123.model')

G = nx.Graph()



#sim = model.similarity('vibration','excitation')
#G.add_edge('vibration', 'excitation', weight=sim)

count5.remove('transient')
count5.remove('voltage')
count5.remove('optic')
count5.remove('measurement')

wordlist = ['transient', 'voltage', 'optic', 'measurement']

s01 = model.similarity('transient', 'voltage')
G.add_edge('transient', 'voltage', weight=s01)
s02 = model.similarity('transient', 'optic')
G.add_edge('transient', 'optic', weight=s02)
s03 = model.similarity('transient', 'measurement')
G.add_edge('transient', 'measurement', weight=s03)


s04 = model.similarity('voltage', 'optic')
G.add_edge('voltage', 'optic', weight=s04)
s05 = model.similarity('voltage', 'measurement')
G.add_edge('voltage', 'measurement', weight=s05)

s06 = model.similarity('optic', 'measurement')
G.add_edge('optic', 'measurement', weight=s06)


# %%% transient %%%

n = 0
wordlist_top = []
while n<=9:
    n=n+1
    sim_top5 = 0
    word_top5 = ''
    for word1 in count5:
        sim = model.similarity('transient', word1)
        if sim >= sim_top5:
            sim_top5 = sim
            word_top5 = word1
    G.add_edge('transient', word_top5, weight=sim_top5)
    count5.remove(word_top5)
    wordlist_top.append(word_top5)

wordlist = wordlist + wordlist_top


wordlist_sec = []
for wordtop5 in wordlist_top:
    n = 0
    while n<=4:
        n=n+1
        sim_top5_sec = 0
        wordtop5_sec = ''
        for word5 in count5:
            sim5 = model.similarity(wordtop5, word5)
            if sim5 > sim_top5_sec:
                sim_top5_sec = sim5
                wordtop5_sec = word5
        G.add_edge(wordtop5, wordtop5_sec, weight=sim_top5_sec)
        count5.remove(wordtop5_sec)
        wordlist_sec.append(wordtop5_sec)

wordlist = wordlist + wordlist_sec



n = 0
wordlist_mid = []
while n<=9:
    n=n+1
    sim_mid = 0
    word_mid = ''
    for word3 in count5:
        sim = model.similarity('transient', word3)
        if 0.7<=sim<0.9:
            if sim > sim_mid:
                sim_mid = sim
                word_mid = word3
    G.add_edge('transient', word_mid, weight=sim_mid)
    count5.remove(word_mid)
    wordlist_mid.append(word_mid)

wordlist = wordlist +wordlist_mid



n = 0
wordlist_far = []
while n<=4:
    n=n+1
    sim_far = 0
    word_far = ''
    for word6 in count5:
        sim = model.similarity('transient', word6)
        if sim<0.7:
            if sim > sim_far:
                sim_far = sim
                word_far = word6
    G.add_edge('transient', word_far, weight=sim_far)
    count5.remove(word_far)
    wordlist_far.append(word_far)

wordlist = wordlist + wordlist_far



# %%% voltage %%%

n = 0
wordlist_top_voltage = []
while n<=9:
    n=n+1
    sim_top5 = 0
    word_top5 = ''
    for word1 in count5:
        sim = model.similarity('voltage', word1)
        if sim >= sim_top5:
            sim_top5 = sim
            word_top5 = word1
    G.add_edge('voltage', word_top5, weight=sim_top5)
    count5.remove(word_top5)
    wordlist_top_voltage.append(word_top5)

wordlist = wordlist + wordlist_top_voltage



wordlist_sec_voltage = []
for wordtop5 in wordlist_top_voltage:
    n = 0
    while n<=4:
        n=n+1
        sim_top5_sec = 0
        wordtop5_sec = ''
        for word5 in count5:
            sim5 = model.similarity(wordtop5, word5)
            if sim5 > sim_top5_sec:
                sim_top5_sec = sim5
                wordtop5_sec = word5
        G.add_edge(wordtop5, wordtop5_sec, weight=sim_top5_sec)
        count5.remove(wordtop5_sec)
        wordlist_sec_voltage.append(wordtop5_sec)

wordlist = wordlist + wordlist_sec_voltage



n = 0
wordlist_mid_voltage = []
while n<=9:
    n=n+1
    sim_mid = 0
    word_mid = ''
    for word3 in count5:
        sim = model.similarity('voltage', word3)
        if 0.7<=sim<0.9:
            if sim > sim_mid:
                sim_mid = sim
                word_mid = word3
    G.add_edge('voltage', word_mid, weight=sim_mid)
    count5.remove(word_mid)
    wordlist_mid_voltage.append(word_mid)

wordlist = wordlist + wordlist_mid_voltage



n = 0
wordlist_far_voltage = []
while n<=4:
    n=n+1
    sim_far = 0
    word_far = ''
    for word6 in count5:
        sim = model.similarity('voltage', word6)
        if sim<0.7:
            if sim > sim_far:
                sim_far = sim
                word_far = word6
    G.add_edge('voltage', word_far, weight=sim_far)
    count5.remove(word_far)
    wordlist_far_voltage.append(word_far)

wordlist = wordlist + wordlist_far_voltage



# %%% optic %%%

n = 0
wordlist_top_optic = []
while n<=9:
    n=n+1
    sim_top5 = 0
    word_top5 = ''
    for word1 in count5:
        sim = model.similarity('optic', word1)
        if sim >= sim_top5:
            sim_top5 = sim
            word_top5 = word1
    G.add_edge('optic', word_top5, weight=sim_top5)
    count5.remove(word_top5)
    wordlist_top_optic.append(word_top5)

wordlist = wordlist + wordlist_top_optic



wordlist_sec_optic = []
for wordtop5 in wordlist_top_optic:
    n = 0
    while n<=4:
        n=n+1
        sim_top5_sec = 0
        wordtop5_sec = ''
        for word5 in count5:
            sim5 = model.similarity(wordtop5, word5)
            if sim5 > sim_top5_sec:
                sim_top5_sec = sim5
                wordtop5_sec = word5
        G.add_edge(wordtop5, wordtop5_sec, weight=sim_top5_sec)
        count5.remove(wordtop5_sec)
        wordlist_sec_optic.append(wordtop5_sec)

wordlist = wordlist + wordlist_sec_optic



n = 0
wordlist_mid_optic = []
while n<=9:
    n=n+1
    sim_mid = 0
    word_mid = ''
    for word3 in count5:
        sim = model.similarity('optic', word3)
        if 0.7<=sim<0.9:
            if sim > sim_mid:
                sim_mid = sim
                word_mid = word3
    G.add_edge('optic', word_mid, weight=sim_mid)
    count5.remove(word_mid)
    wordlist_mid_optic.append(word_mid)

wordlist = wordlist + wordlist_mid_optic



n = 0
wordlist_far_optic = []
while n<=4:
    n=n+1
    sim_far = 0
    word_far = ''
    for word6 in count5:
        sim = model.similarity('optic', word6)
        if sim<0.7:
            if sim > sim_far:
                sim_far = sim
                word_far = word6
    G.add_edge('optic', word_far, weight=sim_far)
    count5.remove(word_far)
    wordlist_far_optic.append(word_far)

wordlist = wordlist + wordlist_far_optic



# %%% measurement %%%

n = 0
wordlist_top_measurement = []
while n<=9:
    n=n+1
    sim_top5 = 0
    word_top5 = ''
    for word1 in count5:
        sim = model.similarity('measurement', word1)
        if sim >= sim_top5:
            sim_top5 = sim
            word_top5 = word1
    G.add_edge('measurement', word_top5, weight=sim_top5)
    count5.remove(word_top5)
    wordlist_top_measurement.append(word_top5)

wordlist = wordlist + wordlist_top_measurement



wordlist_sec_measurement = []
for wordtop5 in wordlist_top_measurement:
    n = 0
    while n<=4:
        n=n+1
        sim_top5_sec = 0
        wordtop5_sec = ''
        for word5 in count5:
            sim5 = model.similarity(wordtop5, word5)
            if sim5 > sim_top5_sec:
                sim_top5_sec = sim5
                wordtop5_sec = word5
        G.add_edge(wordtop5, wordtop5_sec, weight=sim_top5_sec)
        count5.remove(wordtop5_sec)
        wordlist_sec_measurement.append(wordtop5_sec)

wordlist = wordlist + wordlist_sec_measurement



n = 0
wordlist_mid_measurement = []
while n<=9:
    n=n+1
    sim_mid = 0
    word_mid = ''
    for word3 in count5:
        sim = model.similarity('measurement', word3)
        if 0.7<=sim<0.9:
            if sim > sim_mid:
                sim_mid = sim
                word_mid = word3
    G.add_edge('measurement', word_mid, weight=sim_mid)
    count5.remove(word_mid)
    wordlist_mid_measurement.append(word_mid)

wordlist = wordlist + wordlist_mid_measurement



n = 0
wordlist_far_measurement = []
while n<=4:
    n=n+1
    sim_far = 0
    word_far = ''
    for word6 in count5:
        sim = model.similarity('measurement', word6)
        if sim<0.7:
            if sim > sim_far:
                sim_far = sim
                word_far = word6
    G.add_edge('measurement', word_far, weight=sim_far)
    count5.remove(word_far)
    wordlist_far_measurement.append(word_far)

wordlist = wordlist + wordlist_far_measurement








# %%%%%% collocations %%%%%%

file_collocations = open('./collocations_wordlist_step123.txt', 'a', encoding='utf8')
for word_save in wordlist:
    file_collocations.write(word_save + ' ')
file_collocations.close()



subject_word_bag = open('./corpus_training_step123.txt', encoding='utf8').read()
stops = [word for word in stopwords.words('english')] + ['re:', 'fwd:', '-']
subject_words = [word for word in subject_word_bag.split() if word.lower() not in stops]
bigram_measures = collocations.BigramAssocMeasures()
bigram_finder = collocations.BigramCollocationFinder.from_words(subject_words)

# def apply_freq_filter(self, min_freq)   --- Removes candidate ngrams which have frequency less than min_freq.
bigram_finder.apply_freq_filter(5)

file_collocations = open('./collocations_step123.txt', 'a', encoding='utf8')

for word1 in wordlist:
    for word2 in wordlist:
        tup1 = (word1, word2)
        for bigram in bigram_finder.score_ngrams(bigram_measures.raw_freq):
            if tup1 == bigram[0]:
                coll_probability = str(bigram[1])
                file_collocations.write(tup1[0] + '_' + tup1[1] + ',' + coll_probability + '\n')
file_collocations.close()






#for word2 in count5:
#    sim = model.similarity('excitation', word2)
#    if sim > 0.2:
#        G.add_edge('excitation', word2, weight=sim)


#n = 0                                         # 获取list中元素的两两比较(不包含自身的比较)
#for word1 in count5:
#    n = n+1
#    for word2 in count5[n:]:
#        sim = model.similarity(word1,word2)
#        if sim > 0.7:
#            G.add_edge(word1, word2, weight=sim)
#        G.add_edge(word1, word2, weight=sim)
        
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] >= 0.9]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if 0.7 <= d['weight'] < 0.9]
efar = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < 0.7]

#pos = nx.spring_layout(G)  # positions for all nodes
#pos = nx.random_layout(G)
pos = nx.spring_layout(G)
#pos = nx.circular_layout(G)


# circular_layout(G[, dim, scale, center])  Position nodes on a circle.
# fruchterman_reingold_layout(G[, dim, k, ...])Position nodes using Fruchterman-Reingold force-directed algorithm.
# random_layout(G[, dim, scale, center])    Position nodes uniformly at random.
# shell_layout(G[, nlist, dim, scale, center])  Position nodes in concentric circles.
# spring_layout(G[, dim, k, pos, fixed, ...])   Position nodes using Fruchterman-Reingoldforce-directed algorithm.
# spectral_layout(G[, dim, weight, scale,center])  Position nodes using theeigenvectors of the graph Laplacian.

# nodes
nx.draw_networkx_nodes(G, pos, node_size=60, node_color='b', alpha=0.6)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, alpha=0.5,)
nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.5, style='dashed')
nx.draw_networkx_edges(G, pos, edgelist=efar, width=1, alpha=0.5, edge_color='r', style='dashdot')

# edge_color= ''   including: y=yellow

# labels
nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')

plt.axis('off')
plt.savefig('./network_travelingwave_step123.png')
#plt.show()
nx.write_gexf(G, './network_travelingwave_step123.gexf')