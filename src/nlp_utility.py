#coding=utf-8
import numpy as np
import nltk

def nltk_tokenize(string):
    tokens = nltk.word_tokenize(string)
    return tokens

def nltk_tokenize_2(string):
    all_tokens = []
    s_list = string.strip().split('.')
    for s in s_list:
        tokens = nltk.word_tokenize(s)
        all_tokens.extend(tokens)
    return all_tokens

def all2lower(obj):
    if isinstance(obj, str):
        return obj.lower()
    elif isinstance(obj, list):
        res = []
        for val in obj:
            res.append(val.lower())
        return res
    else:
        print type(obj)
        raise ValueError

#将抽取到以段落为元素的list转成以sentence为元素的list
def content2sentences(content):
    sentences = []
    for section in content:
        stcs = section.strip().split('.')
        for stc in stcs:
            sentences.append(stc + '.')
    return sentences

#统计文本词频
def term_frequent(section_list):
    term_dict = {}
    for section in section_list:
        tokens = nltk_tokenize_2(section)
        for token in tokens:
            term_dict[token] = term_dict.get(token, 0) + 1
    return term_dict

def load_word2vec(filepath):
    fr = open(filepath)
    meta = fr.readline().strip().split(' ')
    vocab_size = int(meta[0])
    vec_size = int(meta[1])
    model = {}
    for line in fr.readlines():
        if line.rstrip() == '':
            continue
        array = line.rstrip().split(' ')
        assert len(array) == vec_size + 1
        key = array[0]
        vec = np.asarray(array[1:], dtype=np.float32)
        model[key] = vec
    fr.close()
    return model

if __name__=='__main__':
    model = load_word2vec('../model/wordvec0921.txt')
    print model['hello']
