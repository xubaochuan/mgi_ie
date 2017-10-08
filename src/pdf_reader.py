#coding=utf-8
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
import re
import unicodedata

def remove_ligature(string):
    conv_ligature_string = unicodedata.normalize("NFKD", string.decode('utf-8'))
    words = conv_ligature_string.split(' ')
    new_words = []
    for word in words:
        if '-' in word:
            new_words.append(word.replace('-', ''))
        else:
            new_words.append(word)
    return ' '.join(new_words).encode('utf-8')

def remove_references(text_list):
    pattern = re.compile(r'^\[\d+\]')
    temp_line = 0
    for i in range(len(text_list),0,-1):
        match = pattern.match(text_list[i-1])
        if match and '.' in text_list[i-1]:
            if temp_line == 1:
                del text_list[i]
                temp_line = 0
            del text_list[i-1]
        else:
            if temp_line == 1:
                break
            else:
                temp_line = 1
    return text_list

def concate(text_list):
    section_list = []
    last_section = ''
    for line in text_list:
        section = line.strip()
        if section == '':
            continue
        if section[0].islower():
            if last_section != '':
                section = last_section + ' ' + section
        if section[-1] != '.':
            last_section = section
        else:
            section_list.append(section)
    return section_list

def extract_content(filepath):
    fp = open(filepath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrmgr, device)
    i = 0
    invalid_strings = ['Corresponding author', 'E-mail address', 'corresponding author', 'e-mail address', 'Correspondence to', 'http://dx.doi.org/', 'All rights reserved']
    content_list = []
    outline_list = []
    for page in PDFPage.create_pages(document):
        i += 1
        interpreter.process_page(page)
        layout = device.get_result()
        j = 0
        
        filter_layout = []
        for x in layout:
            if isinstance(x, LTTextBoxHorizontal):
                text = x.get_text().encode('utf-8')
                if text.strip().isdigit():
                    continue
                else:
                    filter_layout.append(x)

        num = len(filter_layout)
        for x in filter_layout:
            if isinstance(x, LTTextBoxHorizontal):
                j += 1
                if i == 1 and j < 5:
                    continue
#                if i == 1 and j == num:
#                    continue
                if i > 1 and j == 1:
                    continue
                text = x.get_text().encode('utf-8')
                invalid_flag = 0
                for string in invalid_strings:
                    if string in text:
                        invalid_flag = 1
                        break
                if invalid_flag == 1:
                    continue
                
                if text.count('. ') == 1 and text.count('\n') == 1:
                    number_str = text.strip().split('. ')[0]
                    number_list = number_str.strip().split('.')
                    sub_title_flag = 1
                    for n in number_list:
                        if not n.isdigit():
                            sub_title_flag = 0
                            break
                    if sub_title_flag == 1:
                        outline_list.append(text.replace('\n', ''))
                        content_list.append(text.replace('\n', ''))
                        continue
                text_list = text.strip().split('\n')
                if len(text)/len(text_list) > 50:
                    content_list.append(text.replace('\n', ''))
    content_list = remove_references(content_list)
    text_list = []
    for text in content_list:
        text_list.append(remove_ligature(text))
    text_list = concate(text_list)
    return outline_list, text_list

def main():
    filepath = 'data/material.pdf'
    text = extract_content(filepath)
    for section in text:
        print section

if __name__=='__main__':
    main()
