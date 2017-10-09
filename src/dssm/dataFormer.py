#coding=utf-8
import numpy as np

class DSSMDataFormer(object):
    def __init__(self):
        self.vocab = self.load_vocab()

    def load_vocab(self):
        vocab_path = './dssm/vocab.txt'
        vocab = {}
        fr = open(vocab_path)
        index = 0
        for row in fr.readlines():
            word = row.strip()
            if word == '':
                continue
            vocab[word] = index
            index += 1
        fr.close()
        return vocab
        fw.close()

    def get_onehot_vec(self, input_data, sentence_length=20):
        data_set = []
        for row in input_data:
            temp = []
            row = row.strip().split()
            if len(row) == 0:
                print "sentence has no word"
                continue
            for word in row:
                if word in self.vocab:
                    temp.append(self.vocab[word])
            if len(temp) > sentence_length:
                temp = temp[:sentence_length]
            elif len(temp) < sentence_length:
                temp = temp + [0] * (sentence_length - len(temp))
            data_set.append(temp)
        return np.asarray(data_set, dtype=np.int32)