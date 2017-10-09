#coding=utf-8
import os
import pdf_reader
import mat_info
import json
import time
import nlp_utility
import material_utility
import wmd
import openie.open_ie_api as openie
import dssm.dssm as dssm
import tensorflow as tf
import db
from dssm.dataFormer import DSSMDataFormer

pdf_dir = '/Users/xubaochuan/www/MgiNet/storage/app/pdf'

chemical_elements = material_utility.load_chemical_elements()
matInfo = mat_info.MatInfo()
wmdClass = wmd.WMD()

dssmDataFormer = DSSMDataFormer()
dssmModel = dssm.Model()
sess = tf.Session()
saver = tf.train.Saver()
dssmModel.load_model(saver, sess, './model/dssm.ckpt')

def validValue(vals, knows):
    vals = dssmDataFormer.get_onehot_vec(vals)
    knows = dssmDataFormer.get_onehot_vec(knows)
    pred = sess.run([dssmModel.pred_y], feed_dict={dssmModel.query: vals, dssmModel.doc: knows})
    return pred[0].tolist()

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

def extract(task_id, filepath):
    result = {}
    outline, content = pdf_reader.extract_content(filepath)
    content = nlp_utility.all2lower(content)
    sentences = nlp_utility.content2sentences(content)
    tf_dict = nlp_utility.term_frequent(content)
    topic_material = get_material_name(tf_dict)
    result['topic_material'] = topic_material

    for att in matInfo.retrieval_conf:
        att_key = att.replace(' ', '_')
        rwmd_result = wmdClass.rwmd(matInfo.retrieval_conf[att], sentences)
        related_sentence = {}
        for val in rwmd_result:
            related_sentence[val[1]] = max(val[2], related_sentence.get(val[1], 0))
        related_sentence = sorted(related_sentence.iteritems(), key=lambda d:d[1], reverse=True)
        val_list = []
        knows_list = []
        for stc, score in related_sentence:
            openie_res = openie.call_api_single(stc)
            openie_res.sort(key=lambda x:len(x[2]))
            knowledges = db.getRelatedKnowledge(att)
            for val in openie_res:
                for knows in knowledges:
                    val_list.append(val[2])
                    knows_list.append(knows)
        pred = validValue(val_list, knows_list)
        for i, p in enumerate(pred):
            if p == 1:
                result[att_key] = val_list[i]
    result_json = json.dumps(result)
    code = db.updateTask(task_id, result_json)
    if code == 200:
        print task_id, code
    else:
        print "error"


def run():
    while True:
        code, task = db.getTask()
        if code == 200:
            task_id = task['id']
            filepath = os.path.join(pdf_dir, task['pdf_path'])
            print task_id, filepath
            extract(task_id, filepath)
        else:
            time.sleep(1)

if __name__=='__main__':
    run()