import random
import re

class Quiz:
    def __init__(self):
        self.ops = '+-*/'

    def quiz_gen(self, paras=None):
        # 如果没有参数传入，打印提示信息
        if not paras:
            print('请在config文件中根据提示输入参数')

        else:
            quiz = ''
            ops, rngs = paras
            if type(rngs) != list:
                rngs = [rngs]
            for i, op in enumerate(ops):
                if i == 0:
                    a = random.randint(1, rngs[i] - 1)
                b = random.randint(1, rngs[i] - 1)
                # 如果是减法的话，被减数小于减数的话，对调
                if op == '-':
                    if eval(str(a)) < b:
                        a, b = b, a
                quiz = f'{a:2} {op} {b:2}'
                a = quiz
            quiz = quiz.replace('*', '×')
            quiz = quiz.replace('/', '÷') + ' ='
            return quiz

    def bulk_quiz_gen(self, paras=None, qty=100):
        if not paras:
            print('请在config文件中根据提示输入参数')
        else:
            quizzes = []
            quiz_no = 1
            for para in paras:
                weight = float(para.split(' ')[-1])
                for i in range(int(qty * weight)):
                    paras_of_quiz = para_parser(para)
                    quiz = f'{quiz_no:3}) ' + self.quiz_gen(paras_of_quiz)
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
