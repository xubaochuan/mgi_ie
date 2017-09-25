#coding=utf-8
def concate():
    filepath = 'data/paper.txt'
    section_list = []
    fr = open(filepath)
    last_section = ''
    for line in fr.readlines():
        section = line.strip()
        if section[0].islower():
            if last_section != '':
                section = last_section + ' ' + section
        if section[-1] != '.':
            last_section = section
        else:
            section_list.append(section)
    fr.close()
    fw = open('data/concate_paper.txt', 'w')
    fw.write('\n'.join(section_list))
    fw.close()
if __name__=='__main__':
    concate()
