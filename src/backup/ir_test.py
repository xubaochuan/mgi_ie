#coding=utf-8
import src.pdf_reader
from src.backup import wmd_utility as utility


def test():
    filepath = '../data/material.pdf'
    content = src.pdf_reader.extract_content(filepath)
    sentences = []
    for section in content:
        stcs = section.strip().split('.')
        for stc in stcs:
            sentences.append(stc + '.')
    query = ['prepared']
    result = utility.rwmd(query, sentences)
    print result

if __name__=='__main__':
    test()
