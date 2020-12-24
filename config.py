import yaml
import os


def config():
    if os.path.exists('cfg.yml'):
        with open('cfg.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
        return config
    else:
        with open('cfg.yml', 'w') as f:
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
            return [cfg]


def write_cfg(cfg):
    with open('cfg.yml', 'w') as f:
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
