#coding=utf-8
import nltk
import pdf_extraction
import wmd_utility as utility
import openie.open_ie_api as openie

ambiguity_elements = ['In', 'As']

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

def load_paper_content(filepath):
    content = pdf_extraction.extract_content(filepath)
    return content

def term_frequent(section_list):
    term_dict = {}
    for section in section_list:
        tokens = nltk_tokenize_2(section)
        for token in tokens:
            if token not in term_dict:
                term_dict[token] = 1
            else:
                term_dict[token] += 1
    return term_dict

def load_chemical_elements(filepath = '../model/chemical_element.txt'):
    chemical_element_set = set()
    fr = open(filepath)
    for line in fr.readlines():
        element = line.strip()
        chemical_element_set.add(element)
    return chemical_element_set

def get_material_name(term_dict):
    material_list = []
    chemical_elements = load_chemical_elements()
    for k,v in term_dict.items():
        split_list = []
        last_string = ''
        length = len(k)
        for i,char in enumerate(k):
            if char.isalpha():
                last_string = last_string + char
                if i == length-1:
                    split_list.append(last_string)
                    last_string = ''
            else:
                if last_string != '':
                    split_list.append(last_string)
                    last_string = ''
        if len(split_list) < 2:
            continue
#        if len(split_list) == 1 and split_list[0] in ambiguity_elements:
#            continue
        flag = 1
        for val in split_list:
            if val not in chemical_elements:
                flag = 0
                break
        if flag == 1:
            material_list.append(k)
    most = 0
    topic_material = ''
    for material in material_list:
        if term_dict[material] > most:
            most = term_dict[material]
            topic_material = material
    return topic_material

#get prepare method
def get_prepare_method():
    query = ['prepared']
    related = utility.rwmd(query, content)
    if related != []:
        openie_res = openie.call_api_single(related[0][1])
        r = ''
        for t in openie_res: 
            if 'prepared' in t[1] and len(t[2]) > len(r):
                r = t[2]
        return r
    else:
        return r

def extract(filepath):
    content = load_paper_content(filepath)
    term_dict = term_frequent(content)
    #get the topic material
    topic_material = get_material_name(term_dict)
    print topic_material
    #get prepare method

def main():
    filepath = '../data/material.pdf'
    extract(filepath)

if __name__=='__main__':
    main()
