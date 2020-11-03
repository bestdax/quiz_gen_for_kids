import random


def type_paras(quiz_type=None):
    if quiz_type == '10以内加减法':
        return {'ops': random.choice('+-'), 'rng': 10}
    elif quiz_type == '20以内加减法':
        return {'ops': random.choice('+-'), 'rng': 20}
    elif quiz_type == '100以内加减法':
        return {'ops': random.choice('+-'), 'rng': 100}
    elif quiz_type == '表内乘法接10以内加减法':
        return {'ops': '*' + random.choice('+-'), 'rng': 10}
    elif quiz_type == '表内乘法':
        return {'ops': '*', 'rng': 6}
    else:
        return ''
# 要修改代码以提高扩展性

class Quiz:
    def __init__(self):
        self.ops = '+-*/'

    def quiz_gen(self, ops=None, rng=100):
        # 如果没有指定运算符从加减乘除中随机选择一个
        if not ops:
            ops = random.choice(self.ops)
        a = random.randint(1, rng - 1)
        b = random.randint(1, rng - 1)

        for op in ops:
            # 如果是减法的话，被减数小于减数的话，对调
            if op == '-':
                if eval(str(a)) < b:
                    a, b = b, a
            quiz = f'{a:2} {op} {b:2}'
            a = quiz
            b = random.randint(1, rng - 1)
        quiz = quiz.replace('*', '×')
        quiz = quiz.replace('/', '÷') + ' ='
        return quiz

    def bulk_quiz_gen(self, types=None, qty=100):
        if not types:
            print('请提供习题类型')
        quizzes = []
        for i in range(qty):
            type_index = i // (100 // len(types))
            paras = type_paras(types[type_index])
            quiz = f'{i + 1:3}) ' + self.quiz_gen(**paras)
            quizzes.append(quiz)
        return quizzes




if __name__ == '__main__':
    q = Quiz()
    t = type_paras('表内乘法接10以内加减法')
    print(t)
    # for item in t:
    #     print(item)
