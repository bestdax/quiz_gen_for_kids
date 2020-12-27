import yaml
import os
from utils import resource_path
from appdirs import AppDirs


def config():
    dirs = AppDirs('Quiz', 'Dax')
    if not os.path.exists(dirs.user_data_dir):
        os.mkdir(dirs.user_data_dir)
    config_path = os.path.join(dirs.user_data_dir, 'config.py')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.Loader)
        return cfg
    else:
        with open(config_path, 'w') as f:
            cfg = {'default':
                       {'global': {'mix': False,
                                   'pages': 1,
                                   'qty': 100,
                                   'quiz_dir': '~/Desktop',
                                   'show_date': True},
                        'rules': [{'first_number': {'display': True, 'range': 100},
                                   'show_answer': False,
                                   'steps': [{'limits': {'borrow': False,
                                                         'brackets': True,
                                                         'carry': False,
                                                         'ceiling': 100,
                                                         'floor': None,
                                                         'remainder': False},
                                              'number': {'display': True, 'range': 100},
                                              'operators': '+-'}
                                             ],
                                   'weight': 1}]
                        }}
            yaml.dump(cfg, f)
            return cfg


def write_cfg(cfg):
    dirs = AppDirs('Quiz', 'Dax')
    if not os.path.exists(dirs.user_data_dir):
        os.mkdir(dirs.user_data_dir)
    config_path = os.path.join(dirs.user_data_dir, 'config.py')
    with open(config_path, 'w') as f:
        yaml.dump(cfg, f)


def add_step(rule):
    new_step = {'limits':
                    {'borrow': False,
                     'brackets': False,
                     'carry': False,
                     'ceiling': None,
                     'floor': None,
                     'remainder': False},
                'number': {'display': True, 'range': 100},
                'operators': '+-'}
    rule['steps'].append(new_step)
    return new_step


def rm_step(rule):
    if len(rule['steps']) > 1:
        rule['steps'].pop(-1)
        return True
    else:
        return False
