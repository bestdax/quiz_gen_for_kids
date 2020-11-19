import os
from pdf import PDF
from quizzes import bulk_quiz_gen
import yaml

with open('config.yml', 'r') as f:
    configs = [config for config in yaml.load_all(f, Loader=yaml.Loader)]

for config in configs:
    pdf = PDF()
    user = config['user']
    for i in range(config['global']['pages']):
        pdf.add_page()
        pdf.set_title('四则运算练习')
        pdf.set_date(config['global']['show_date'])
        quizzes = bulk_quiz_gen(config)
        pdf.set_quizzes(quizzes=quizzes)
    quiz_dir = config['global']['quiz_dir']
    quiz_dir = os.path.expanduser(quiz_dir)
    pdf_filename = os.path.join(quiz_dir, f'{user}.pdf' if user else 'quizzes.pdf')
    pdf.output(f'{pdf_filename}', 'F')
