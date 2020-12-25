import os
import sys
from collections import defaultdict


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS2', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def translate(string):
    trans_dict = defaultdict()
    reversed_trans_dict = defaultdict()
    translate_file = resource_path('rsc/translate.txt')
    with open(translate_file) as f:
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
