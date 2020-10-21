import random
import datetime

operations = '+-*/'


def quiz_gen(quantity=100, quiz_type='minus_plus'):
    quizzes = ''
    if quiz_type == 'minus_plus':
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
    if quiz_type == 'minus_plus_multiply':
        ops = operations[:3]
        for i in range(quantity):
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            op = random.choice(ops[:2])
            while True:
                c = random.randint(1, 9)
                if op == '-':
                    if a * b >= c:
                        break
                else:
                    break
            quiz = f'{i + 1:3}) {a} × {b} {op} {c} = \n'
            quizzes += quiz
        return quizzes


def today_string():
    today = datetime.date.today()
    today = today.strftime('%Y年%m月%d日')
    return today


if __name__ == '__main__':
    print(quiz_gen(quiz_type='minus_plus_multiply'))
