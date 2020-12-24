import os
import random
import re
import sys
from typing import List

from pdf import PDF


def gen_pdf_quiz(cfg):
    for user in cfg:
        pdf = PDF()
        for i in range(cfg[user]['global']['pages']):
            pdf.add_page()
            pdf.set_title('四则运算练习')
            pdf.set_date(cfg[user]['global']['show_date'])
            quizzes = bulk_quiz_gen(cfg[user])
            pdf.set_quizzes(quizzes=quizzes)
        quiz_dir = cfg[user]['global']['quiz_dir']
        quiz_dir = os.path.expanduser(quiz_dir)
        pdf_filename = os.path.join(quiz_dir, f'{user}.pdf' if user else 'quizzes.pdf')
        pdf.output(f'{pdf_filename}', 'F')


def bulk_quiz_gen(user):
    rules = user['rules']
    quizzes: List[str] = []
    mix = user['global']['mix']
    qty = user['global']['qty']
    number_of_digits = len(str(qty))
    quiz_count = 0
    for n, rule in enumerate(rules):
        weight = rule['weight']
        if n != len(rules) - 1:
            qty_of_type = int(qty * weight)
            quiz_count += qty_of_type
        else:
            qty_of_type = qty - quiz_count
        for i in range(qty_of_type):
            quiz = quiz_gen(rule)
            quizzes.append(quiz)
    if mix:
        random.shuffle(quizzes)
    for i in range(qty):
        quizzes[i] = f'{i + 1:{number_of_digits}}) {quizzes[i]}'
    return quizzes


def evaluate(quiz):
    try:
        return eval(quiz)
    except ZeroDivisionError:
        return float('nan')


def quiz_formator(a, op, b):
    return f'{a:2} {op} {b:2}'


def rand_gen(rng):
    return random.randint(1, rng - 1)


###############################################################################
# 根据数字范围的规则产生随机数
# 范围是一个整数的话就产生从0到这个数的随机数
# 范围为'=30'就输出30
# 范围为'20, 30'就输出20到30(包含首尾)的随机数。
###############################################################################
def rand(number_range):
    """
    根据数字范围的规则产生随机数
    范围是一个整数的话就产生从0到这个数的随机数
    范围为'=30'就输出30
    范围为'20, 30'就输出20到30(包含首尾)的随机数。
    :param number_range:
    :return: 按照规则生成的随机数
    """
    if type(number_range) == int:
        return random.randint(0, number_range - 1)
    elif type(number_range) == str:
        if number_range.startswith('='):
            try:
                number = int(number_range[1:])
            except ValueError:
                print('数字范围规则设置出错!')
            else:
                return number
        elif re.search(r'\d+, *\d+', number_range):
            a, b = re.findall(r'(\d+), *(\d+)', number_range)[0]
            try:
                a = int(a)
                b = int(b)
            except ValueError:
                print('数字范围规则设置出错!')
            else:
                if a > b:
                    a, b = b, a
                return random.randint(a, b)
    else:
        print('数字范围规则设置出错!')


def is_formula(formula):
    if re.search(r'\d+ *[+\-*/] *\d+ *', formula):
        return True
    else:
        return False


def quiz_gen(rule):
    quiz_components = []
    for n, step in enumerate(rule['steps']):
        limits = step['limits']
        while True:
            if n == 0:
                a = rand(rule['first_number']['range'])
            op = random.choice(step['operators'])
            b = rand(step['number']['range'])
            quiz = quiz_formator(a, op, b)
            if not limits['floor']:
                floor = 0
            else:
                floor = limits['floor']
            if evaluate(quiz) < floor:
                continue
            if not limits['ceiling']:
                ceiling = sys.maxsize
            else:
                ceiling = limits['ceiling']
            if evaluate(quiz) > ceiling:
                continue
            if limits['carry']:
                if evaluate(quiz) // 10 == (a // 10 + b // 10):
                    continue
            if limits['borrow']:
                if evaluate(quiz) // 10 + b // 10 == a // 10:
                    continue
            if op == '/' and (not limits['remainder']):
                if b == 0:
                    continue
                if evaluate(quiz) != (a // b):
                    continue
            break
        if limits['brackets']:
            quiz_components.append('(')
        if n == 0:
            if rule['first_number']['display']:
                quiz_components.append(str(a))
            else:
                quiz_components.append('(  )')
        quiz_components.append(op)
        if step['number']['display']:
            quiz_components.append(str(b))
        else:
            quiz_components.append('(  )')
        if limits['brackets']:
            quiz_components.append(')')
        a = evaluate(quiz)
    quiz_components.append('=')
    if rule['show_answer']:
        quiz_components.append(a)
    quiz = ''
    for item in quiz_components:
        if str(item) in '()':
            quiz += item
        elif str(item) in '+-*/=':
            quiz += f'{item}'
        else:
            quiz += f'{item:2}'

    quiz = quiz.replace('*', '×')
    quiz = quiz.replace('/', '÷')
    return quiz


if __name__ == '__main__':
    import yaml

    with open('config.yml', 'r') as c:
        config = yaml.load(c, Loader=yaml.Loader)
    rules = config['rules']
    print(quiz_gen(rules[0]))
