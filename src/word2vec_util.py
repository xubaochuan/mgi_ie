#coding=utf-8
import numpy as np

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
