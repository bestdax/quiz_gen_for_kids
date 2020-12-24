from collections import defaultdict


def translate(string):
    trans_dict = defaultdict()
    reversed_trans_dict = defaultdict()
    with open('rsc/translate.txt') as f:
        lines = f.readlines()
        for line in lines:
            en, cn = line.strip().split()
            trans_dict[en] = cn
            reversed_trans_dict[cn] = en
    s = str(string)
    if s in trans_dict:
        return trans_dict[s]
    elif s in reversed_trans_dict:
        result = reversed_trans_dict[s]
        value_dict = {'None': None, 'False': False, 'True': True}
        if result in value_dict:
            result = value_dict[result]
        return result
    else:
        return string

