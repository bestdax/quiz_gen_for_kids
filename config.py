import yaml
import os


def config():
    if os.path.exists('cfg.yml'):
        with open('cfg.yml', 'r') as f:
            config =  yaml.load(f, Loader=yaml.Loader)
        return config
    else:
        with open('cfg.yml', 'w') as f:
            cfg = {'global': {'mix': False,
                              'pages': 1,
                              'qty': 100,
                              'quiz_dir': '~/Desktop',
                              'show_date': True},
                   'rules': [{'first_number': {'display': True, 'range': 100},
                              'show_answer': False,
                              'steps': [{'limits': {'borrow': None,
                                                    'brackets': None,
                                                    'carry': None,
                                                    'ceiling': None,
                                                    'floor': None,
                                                    'remainder': None},
                                         'number': {'display': True, 'range': 100},
                                         'operators': '+-'}, ],
                              'weight': 1}],
                   'user': 'default'}
            yaml.dump(cfg, f)
            return [cfg]

def write_cfg(cfg):
    with open('cfg.yml', 'w') as f:
        yaml.dump(cfg, f)
