import random
import datetime

operations = '+-*/'


def quiz_gen(quantity=100):
    quizzes = ''
    ops = operations[:2]
    for i in range(quantity):
        a = random.randint(10, quantity - 1)
        b = random.randint(10, quantity - 1)
        op = random.choice(ops)
        end = '\n'
        if op == '-':
            a, b = max(a, b), min(a, b)
        quiz = f'{i + 1:3}) ' + str(a) + ' ' + op + ' ' + str(b) + ' = (     )' + end
        quizzes += quiz
    return quizzes


def today_string():
    today = datetime.date.today()
    today = today.strftime('%Y年%m月%d日')
    return today
