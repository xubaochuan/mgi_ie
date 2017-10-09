ambiguity_elements = ['In', 'As']
def load_chemical_elements(filepath = '../model/chemical_element.txt'):
    chemical_element_set = set()
    fr = open(filepath)
    for line in fr.readlines():
        element = line.strip()
        chemical_element_set.add(element.lower())
    return chemical_element_set