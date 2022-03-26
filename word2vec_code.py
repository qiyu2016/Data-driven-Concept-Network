# -*- coding: utf-8-*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
# 解决warning问题
# UserWarning: detected Windows; aliasing chunkize to chunkize_serial
# warnings.warn("detected Windows; aliasing chunkize to chunkize_serial")
import gensim
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import logging
import nltk
import re
import string
from nltk.stem import WordNetLemmatizer



def clearSen(comment):
    comment = comment.replace('-', ' ')
    return comment



# 分词 & 去除其中的标点符号
def get_tokens(text):
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens 
#tokens = get_tokens(text1)


with open('./corpus_process_step123.txt', encoding='utf8') as f:
    document = f.read()
    document = clearSen(document)
    
    
    tokens = get_tokens(document)
    
    lemmatizer = WordNetLemmatizer()
    tokens_lemma = [lemmatizer.lemmatize(t, pos='n') for t in tokens]


    result = ' '.join(tokens_lemma)
    result = result.encode('utf-8')
    with open('./corpus_training_step123.txt', 'w', encoding='utf8') as f2:
        f2.write(result.decode('utf-8'))
f.close()
f2.close()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.LineSentence('./corpus_training_step123.txt')   # 加载语料
model = word2vec.Word2Vec(sentences, size=90, window=10, min_count=1)

model.save('./word2vec_travelingwave_step123.model')

