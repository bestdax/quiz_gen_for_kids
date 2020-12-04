import yaml
import os


def config():
    if os.path.exists('config.yml'):
        with open('cfg.yml', 'r') as f:
            configs = [cfg for cfg in yaml.load_all(f, Loader=yaml.Loader)]
        return configs
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
                                                    'floor': None},
                                         'number': {'display': True, 'range': 100},
                                         'operators': '+-'}, ],
                              'weight': 1}],
                   'user': 'default'}
            yaml.dump(cfg, f)
            return [cfg]
