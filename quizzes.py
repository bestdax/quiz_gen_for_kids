import random
import re


# 参数解析器
def para_parser(para):
    items = para.split(' ')
    ops = items[0]
    ops_parsed = ''
    in_bracket = False
    selective_ops = ''
    # 解析运算运算符
    for c in ops:
        # 如果遇到括号就打开括号开关
        if c in '(（':
            in_bracket = True
        # 如果不在括号内就直接添加到解析过的字符串中
        if not in_bracket:
            ops_parsed += c
        # 否则就添加到可选运算符中
        else:
            if c not in '()（）':
                selective_ops += c
        # 如果遇到右括号就关闭括号开关，从可选运算符中随机选一个并添加到运算符字符串中，同时清空可选运算符字符串
        if c in ')）':
            in_bracket = False
            ops_parsed += random.choice(selective_ops)
            selective_ops = ''

        # 从第二位开始存储的是运算的范围，数量根据运算符的个数来确定
        rngs = items[1: 1 + len(ops_parsed)]
        rngs = [int(item) for item in rngs]

        # 最后一位存储的是权重参数
        weight = items[-1]

    return ops_parsed, rngs


# TODO 要修改代码以提高扩展性

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
