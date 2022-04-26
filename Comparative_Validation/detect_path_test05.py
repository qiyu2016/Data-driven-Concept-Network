#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Qiyu
"""

# 通过此方法获取的节点间的最短路径，其路径长度与采用 set1.shortest_path_distance(set2) 得到的路径长度完全相等



from nltk.corpus import wordnet as wn

document = open('./netc_wordlist_travelingwave.txt', encoding='utf8')

path0_list = []
path1_list = []
lsc_list = []

index_start = -1
index_path0 = -1
index_path1 = -1
index_lsc = -1
for index, line in enumerate(document):
	if 'transmission-line  <path length min>   2' in line:
		line_context = 'transmission-line  <path length min>   2'
		index_start = index
		index_path0 = index + 1
		index_path1 = index + 2
		index_lsc = index + 3
		

	if index == index_path0:
		path0 = line
		path0_word = path0[8:].strip().replace("')", "")
		path0_list.append(path0_word)
		index_path0 = index_path0 + 5
	elif index == index_path1:
		path1 = line
		path1_word = path1[8:].strip().replace("')", "")
		path1_list.append(path1_word)
		index_path1 = index_path1 + 5
	elif index == index_lsc:
		lsc_line = line
		lsc_word = lsc_line[8:].strip().replace("')", "")
		lsc_list.append(lsc_word)
		index_lsc = index_lsc + 5





# 基于WordNet寻找路径
file = open('./detect_path_test05.txt', 'a', encoding='utf8')


for iid in range(len(path0_list)):
	set1 = wn.synset(path0_list[iid])
	set2 = wn.synset(path1_list[iid])
	
	set_lsc = wn.synset(lsc_list[iid])   #两个同义词集的最深公共节点
	
	a = set1.hypernym_paths()
	b = set2.hypernym_paths()
	c_lsc = set_lsc.hypernym_paths()
	
# 查询包含最深公共节点set_lsc的两条最短路径	
#	m = []
#	n = []
#	p = []

#######################################################	
	pathlen_set = []
	path_set = []
	shortest_len = set1.shortest_path_distance(set2)
	for i in a:
		for j in b:
			pathi = []
			pathj = []
			for p in i:
				pathi.append(p)
			for p in j:
				pathj.append(p)
			
			re_list = []
			rtime = min(len(pathi), len(pathj))
			set_comdeep = pathi[rtime-1]
			if pathi[0:rtime] == pathj[0:rtime]:
				for r in range(rtime):
					re_list.append(pathi[r])
			else:
				for r in range(len(pathi)):
					if pathi[r] == pathj[r]:
						re_list.append(pathi[r])
					elif pathi[r] != pathj[r]:
						set_comdeep = pathi[r-1]
						break
					
			pathi.reverse()
			for k in re_list:
				pathi.remove(k)
				pathj.remove(k)
	
			pathi.append(set_comdeep)
			pathi.extend(pathj)
			print(pathi)
			pathlen_set.append(len(pathi))
			path_set.append(pathi)
	
	for i in range(len(pathlen_set)):
		if pathlen_set[i] == min(pathlen_set):
			path_index = i
			break
	
	path_shortest = path_set[path_index]
	

	
	#file.write('path No.' + str(iid+1) + '\n')
	#for r in range(len(a[icount])):
	#	file.write(str(a[icount][r]) + '\n')
	file.write(path0_list[iid] + '   ' + path1_list[iid] + '   ' + lsc_list[iid] + '   ')
	file.write(str(len(path_shortest)-1) + '\n')	


file.close()
