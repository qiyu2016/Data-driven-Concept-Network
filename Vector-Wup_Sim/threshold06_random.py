#!/usr/bin/python
# -*- coding: UTF-8 -*-



import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import logging
import nltk
from collections import Counter

import random
from nltk.corpus import wordnet as wn



document = open('./corpus_training_step123.txt', encoding='utf8').read()

tokens = nltk.word_tokenize(document)

lexicalpos = nltk.pos_tag(tokens)

noun = [word for (word, tag) in lexicalpos if tag.startswith('N')]          # 获取名词

count1 = Counter(noun)
count5 = []
for i in count1:
    if (count1[i]>=1):
        count5.append(i)

# %%% transmission %%%
count5.remove('sensor')

# 从count5 词汇列表中随机抽取2000个词汇
listrandom = random.sample(count5, 2000)

model=KeyedVectors.load('./word2vec_travelingwave_step123.model')



file_similarity = open('./sensor_random.txt', 'a', encoding='utf8')
# file_similarity.write('######' + 'transmission with words_(0.0-0.05)_similarity' + '############' + '\n')



for word3 in listrandom:
    sim = model.similarity('sensor', word3)
    x = wn.synsets('sensor', pos = wn.NOUN)
    y = wn.synsets(word3, pos = wn.NOUN)
    if y == []:
        sim_record = 'none'
    else:
        sim_list = []
        for i in x:
            for j in y:
                sim_wordnet = i.wup_similarity(j)
                sim_list.append(sim_wordnet)
        sim_record = max(sim_list)
        file_similarity.write(word3 + ',' + str(sim) + ',' + str(sim_record) + '\n')
file_similarity.close()
