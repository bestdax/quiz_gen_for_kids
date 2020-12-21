from collections import defaultdict
def translate():
    trans_dict = defaultdict()
    with open('translate.txt') as f:
        lines = f.readlines()
        for line in lines:
            en, cn = line.strip().split()
            trans_dict[en] = cn
    return trans_dict
