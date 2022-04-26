#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Qiyu
"""



from nltk.corpus import wordnet as wn

keywords = ['transmission', 'line', 'fault', 'location', 'traveling', 'wave', 'sensor', 'transient', 'voltage', 'optic', 'measurement']

keylist = ['transmission', 'line', 'fault', 'location', 'traveling', 'wave', 'sensor', 'transient', 'voltage', 'optic', 'measurement']

for word_re in keywords:
	de = wn.synsets(word_re, pos=wn.NOUN)
	if de == []:
		keywords.remove(word_re)
		keylist.remove(word_re)

file = open('./netc_wordlist_travelingwave.txt', 'a', encoding='utf8')
#print(keywords)
#print(keylist)
file.write('keywords:' + '\n')
for k in keywords:
	file.write(k + ', ')
file.write('\n' + '\n')
file.write('keylist:' + '\n')
for k in keylist:
	file.write(k + ', ')
file.write('\n' + '\n')


for word in keywords:
	keylist.remove(word)
	if keylist == []:
		break
	elif keylist != []:
		for word_2 in keylist:
#			print(word + ' ' + word_2)
			x = wn.synsets(word, pos=wn.NOUN)
			y = wn.synsets(word_2, pos=wn.NOUN)
			
			tuple_list = []
			for i in x:
				for j in y:
					tuple1 = ()
					path_len = i.shortest_path_distance(j)
					if path_len != None:
						tuple1 = (path_len, i, j)
						tuple_list.append(tuple1)
			
			path_list = []
			for r in range(len(tuple_list)):
				path_list.append(tuple_list[r][0])
			
			min_len = min(path_list)
			for r in range(len(tuple_list)):
				if tuple_list[r][0] == min_len:
					file.write('\n')
					file.write(word + '-' + word_2 + '  ' + '<path length min>' + '   ' + str(tuple_list[r][0]) + '\n')
					file.write(str(tuple_list[r][1]) + '\n')
					file.write(str(tuple_list[r][2]) + '\n')
					LSC = tuple_list[r][1].lowest_common_hypernyms(tuple_list[r][2])
					file.write(str(LSC[0]) + '\n')
#					print(word + '-' + word_2 + '  ' + '<path length min>' + '   ' + str(tuple_list[r][0]))
#					print(tuple_list[r][1])
#					print(tuple_list[r][2])
#					LSC = tuple_list[r][1].lowest_common_hypernyms(tuple_list[r][2])
#					print(LSC[0])
		
file.close()


#set1 = wn.synset('coffee.n.01')
#set2 = wn.synset('tea.n.01')
#path_len = set1.shortest_path_distance(set2)




#set1.lowest_common_hypernyms(set2)
#set1.hypernyms()
#set2.hypernyms()

#import warnings
#warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
#from gensim.models.keyedvectors import KeyedVectors
#from gensim.models import word2vec
#import logging
#from nltk.corpus import wordnet as wn
#import random
#import nltk
#from collections import Counter
#
#
#
#def func1(one_list):
#    return list(set(one_list))
#
## word_list = [str(lemma.name()) for lemma in wn.synset('line.n.01').lemmas()]
#
#syn_list = wn.synsets('power')
#
#word_lemma = []
#for syn in syn_list:
#    wlist = [str(lemma.name()) for lemma in syn.lemmas()]
#    word_lemma = word_lemma + wlist
#
#
#hyper_list = []
#for syn in syn_list:
#    hyper = syn.hypernyms()
#    for hyper_set in hyper:
#        hypernym = [str(lemma.name()) for lemma in hyper_set.lemmas()]
#        hyper_list = hyper_list + hypernym
#
#hypo_list = []
#for syn in syn_list:
#    hypo = syn.hyponyms()
#    for hypo_set in hypo:
#        hyponym = [str(lemma.name()) for lemma in hypo_set.lemmas()]
#        hypo_list = hypo_list + hyponym
#
#
#word_list00 = word_lemma + hyper_list + hypo_list
#word_list = func1(word_list00)
#
#
#
#document = open('./corpus_training.txt', encoding='utf8').read()
#tokens = nltk.word_tokenize(document)
#lexicalpos = nltk.pos_tag(tokens)
#noun = [word for (word, tag) in lexicalpos if tag.startswith('N')]          # 获取名词
#
#count1 = Counter(noun)
#count5 = []
#for i in count1:
#    if (count1[i]>=1):
#        count5.append(i)
#
## %%% transmission %%%
#count5.remove('power')
#
#
#
#model=KeyedVectors.load('./word2vec_bike.model')
#
#interval = [0.0, 0.25, 0.7, 1.0]
#for r in range(3):
#    word_list02 = []
#    for word02 in count5:
#        sim = model.similarity('power', word02)
#        if interval[r] <= sim < interval[r+1]:
#            word_list02.append(word02)
#
#    wordnet_list = []
#    for wordevalu in word_list02:
#        y = wn.synsets(wordevalu)
#        if y != []:
#          wordnet_list.append(wordevalu)
#
#    file_relatedvalue = open('./05_power_relatedvalue.txt', 'a', encoding='utf8')
#
#
#    if len(wordnet_list) > 0:
#        number = len(wordnet_list)
#        value_sum = 0
#        for word_all in wordnet_list:
#            syn_list = wn.synsets(word_all)
#            word_lemma = []
#            for syn in syn_list:
#                wlist = [str(lemma.name()) for lemma in syn.lemmas()]
#                word_lemma = word_lemma + wlist
#            wordsec_list = func1(word_lemma)
#            related_value = 0
#            for i in word_list:
#                for j in wordsec_list:
#                    if i == j:
#                        related_value = related_value + 1
#            value_sum = value_sum + related_value
#            file_relatedvalue.write('power' + ',' + word_all + ',' + str(related_value) + '\n')
#    file_relatedvalue.write('The above internal is ' + str(interval[r]) + '-' + str(interval[r+1]) + '\n')
#    file_relatedvalue.write('The number & value_sum in this internal is ' + str(number) + ',' + str(value_sum) + '\n')
#    file_relatedvalue.write('\n')
#
#
#    file_relatedvalue.close()




