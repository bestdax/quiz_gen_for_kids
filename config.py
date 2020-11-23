import yaml
import os


def config():
    if os.path.exists('config.yml'):
        with open('config.yml', 'r') as f:
            configs = [config for config in yaml.load_all(f, Loader=yaml.Loader)]
        return configs
    else:
        with open('config.yml', 'w') as f:
            config = {'global': {'mix': False,
                                 'pages': 1,
                                 'qty': 100,
                                 'quiz_dir': '~/Desktop',
                                 'show_date': True},
                      'rules': [{'first_number': {'display': True, 'range': 100},
                                 'show_answer': False,
                                 'steps': [{'limits': {'borrow': None,
                                                       'brackets': True,
                                                       'carry': None,
                                                       'ceiling': None,
                                                       'floor': None},
                                            'number': {'display': True, 'range': 100},
                                            'operators': '+-'},],
                                 'weight': 1}],
                      'user': 'default'}
            yaml.dump(config, f)
            return [config]
