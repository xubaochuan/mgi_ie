#coding=utf-8
import csv
import os
import sys
import nltk
import random
import math
import numpy as np
from emd import emd
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import word2vec_util
import time
reload(sys)
sys.setdefaultencoding('utf-8') 
global model

def load_word2vec_model(filepath = '../model/wordvec0921.txt'):
    global model
#    model = gensim.models.KeyedVectors.load_word2vec_format(filepath, binary=False)
    model = word2vec_util.load_word2vec(filepath)
    return model

def tokenize(content):
    raw_tokens = nltk.word_tokenize(content)
    tokens = []
    stop_words = load_stop_words()
    for i in raw_tokens:
        word = i.lower()
        if word in stop_words or word not in model:
            continue
        else:
            tokens.append(word)
    return ' '.join(tokens)

def load_stop_words(filepath = '../model/smart_stop_words'):
    stop_words = set()
    fr = open(filepath)
    for line in fr.readlines():
        if line.strip() == '':
            continue
        word = line.strip()
        stop_words.add(word)
    return stop_words

def cal_idf(content_list):
    count_dict = {}
    idf_dict = {}
    total = 0.0
    for one in content_list:
        word_list = one.strip().split(' ')
        temp_set = set()
        total += 1
        for word in word_list:
            if word not in temp_set:
                temp_set.add(word)
            else:
                continue
            if word not in count_dict:
                count_dict[word] = 0.0
            count_dict[word] += 1
    for k,v in count_dict.items():
        idf = math.log(total/v)
        idf_dict[k] = idf
    return idf_dict

def get_sentence_vec(sentence_list, idf_enable = False):
    if idf_enable == True:
        idf_dict = cal_idf(sentence_list)
    global model
    word_weight_list = []
    word_vec_list = []
    for one in sentence_list:
        word_count_dict = {}
        sentence_word_weight_list = []
        sentence_word_vec_list = []
        total_word = 0.0
        word_list = one.strip().split(' ')
        for word in word_list:
#            if word in stop_words:
#                continue
            if word in model:
                vec = model[word]
            else:
                continue
            if word not in word_count_dict:
                word_count_dict[word] = {}
                word_count_dict[word]['count'] = 0.0
            word_count_dict[word]['count'] += 1
            word_count_dict[word]['vec'] = vec
            total_word += 1
        for k,v in word_count_dict.items():
            if idf_enable == True:
                idf = idf_dict[k]
                weight = word_count_dict[k]['count']/total_word*float(idf)
            else:
                weight = word_count_dict[k]['count']/total_word
            sentence_word_weight_list.append(weight)
            sentence_word_vec_list.append(word_count_dict[k]['vec'])
        weight_sum = 0.0
        for i in sentence_word_weight_list:
            weight_sum += i
        normalize_word_weight_list = []
        for i in sentence_word_weight_list:
            normalize_word_weight_list.append(i/float(weight_sum))
        word_weight_list.append(normalize_word_weight_list)
        word_vec_list.append(sentence_word_vec_list)
    return word_weight_list, word_vec_list

def cosine_distance(f1, f2):
    result = cosine_similarity([f1], [f2])
    r = float(result[0][0])
    return r

def euclidean_distance(f1, f2):
    dist = np.sqrt(np.sum(np.square(f1 - f2)))
    return float(dist)

def rwmd(querys, candidates):
    global model
    model = load_word2vec_model()
    query_weight_list ,query_vec_list = get_sentence_vec(querys)
    candidate_weight_list, candidate_vec_list = get_sentence_vec(candidates)
    q_len = len(querys)
    s_len = len(candidates)
    result = []
    for i in range(q_len):
        distance_dict = {}
        for j in range(s_len):
            min_distance_list = []
            for m, q_wordvec in enumerate(query_vec_list[i]):
                min_distance = 10000
                for s_wordvec in candidate_vec_list[j]:
                    distance = euclidean_distance(q_wordvec, s_wordvec)
                    if distance < min_distance:
                        min_distance = distance
                min_distance_list.append(min_distance)
            if len(min_distance_list) != len(query_weight_list[i]):
                raise ValueError("length did not match")
            distance_sum = 0.0
            for index, distance in enumerate(min_distance_list):
                weight = query_weight_list[i][index]
                distance_sum += weight * distance
            distance_dict[j] = distance_sum
        sort_distance_dict = sorted(distance_dict.iteritems(),key=lambda d:d[1], reverse = False)
        index = 0 
        for k,v in sort_distance_dict:
            if v > 1:
                continue
            if index < 10:
                result_tuple = (querys[i], candidates[k], v)
                result.append(result_tuple)
                index += 1
            else:
                break
    return result
