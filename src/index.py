#coding=utf-8
import pdf_reader
import mat_info
import nlp_utility
import material_utility
import wmd
import openie.open_ie_api as openie

chemical_elements = material_utility.load_chemical_elements()
matInfo = mat_info.MatInfo()
wmdClass = wmd.WMD()

#获取主题材料名称
def get_material_name(tf_dict):
    material_list = []
    for k,v in tf_dict.items():
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
        if tf_dict[material] > most:
            most = tf_dict[material]
            topic_material = material
    return topic_material

def extract(filepath):
    outline, content = pdf_reader.extract_content(filepath)
    content = nlp_utility.all2lower(content)
    senteces = nlp_utility.content2sentences(content)
    tf_dict = nlp_utility.term_frequent(content)
    topic_material = get_material_name(tf_dict)

    for att in matInfo.retrieval_conf:
        rwmd_result = wmdClass.rwmd(matInfo.retrieval_conf[att], senteces)
        related_sentence = {}
        for val in rwmd_result:
            related_sentence[val[1]] = max(val[2], related_sentence.get(val[1], 0))
        related_sentence = sorted(related_sentence.iteritems(), key=lambda d:d[1], reverse=True)
        for stc, score in related_sentence:
            openie_res = openie.call_api_single(stc)
            print openie_res
            exit()

def run():
    while True:
        filepath = "../data/material.pdf"
        extract(filepath)

if __name__=='__main__':
    run()