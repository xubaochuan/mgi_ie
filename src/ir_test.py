#coding=utf-8
import wmd_utility as utility
import openie.main
import pdf_extraction

def test():
    filepath = '../data/material.pdf'
    content = pdf_extraction.extract_content(filepath)
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
