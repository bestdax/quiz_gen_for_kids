import random
import re


class Quiz:
    def __init__(self):
        self.ops = '+-*/'

    def quiz_gen(self, rule=None):
        # 如果没有参数传入，打印提示信息
        if not rule:
            print('请在config文件中根据提示输入参数')

        else:
            quiz = ''
            steps = len(rule) // 3
            range_a = int(rule[1])
            a = random.randint(1, range_a - 1)
            for i in range(steps):
                ops = rule[2 + 3 * i]
                range_b = int(rule[3 + 3 * i])
                limits = rule[4 + 3 * i]
                b = random.randint(1, range_b - 1)
                op = random.choice(ops)
                # 如果是减法的话，被减数小于减数的话，对调
                if op == '-':
                    if eval(str(a)) < b:
                        a, b = b, a
                quiz = f'{a:2} {op} {b:2}'
                a = quiz
            quiz = quiz.replace('*', '×')
            quiz = quiz.replace('/', '÷') + ' ='
            return quiz

    def bulk_quiz_gen(self, paras):
        if not paras:
            print('请在config文件中根据提示输入参数')
        else:
            quizzes = []
            quiz_no = 1
            for rule in paras['rules']:
                weight = rule[0]
                qty = paras['global']['qty']
                for i in range(int(qty * weight)):
                    quiz = f'{quiz_no:3}) ' + self.quiz_gen(rule)
                    quizzes.append(quiz)
                    quiz_no += 1
            return quizzes


if __name__ == '__main__':
    q = Quiz()
    # t = type_paras('表内乘法接10以内加减法')
    # print(t)
    # for item in t:
    #     print(item)
    print(para_parser('(+-) 100 0.75'))
