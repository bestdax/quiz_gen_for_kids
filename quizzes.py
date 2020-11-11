import random


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
            range_a = rule[1]
            # 分步进行判断
            for i in range(steps):
                ops = rule[2 + 3 * i]
                range_b = rule[3 + 3 * i]
                limits = rule[4 + 3 * i]
                while True:
                    # 只有第一步的时候a可以变化
                    if i == 0:
                        if self.is_static(range_a):
                            a = int(range_a[1:])
                        else:
                            a = self.rand_gen(int(range_a))
                    op = random.choice(ops)
                    if self.is_static(range_b):
                        b = int(range_b[1:])
                    else:
                        b = self.rand_gen(int(range_b))
                    quiz = self.quiz_formator(a, op, b)
                    if eval(quiz) < limits['floor']:
                        continue
                    if eval(quiz) > limits['ceiling']:
                        continue
                    if limits['carry']:
                        if eval(quiz) // 10 == (a // 10 + b // 10):
                            continue
                    if limits['borrow']:
                        if eval(quiz) // 10 + b // 10 == a // 10:
                            continue
                    break

                quiz = self.quiz_formator(a, op, b)
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

    def quiz_formator(self, a, op, b):
        return f'{a:2} {op} {b:2}'

    def rand_gen(self, rng):
        return random.randint(1, rng - 1)

    # 判断是一个范围还是固定的数
    def is_static(self, a):
        if a.startswith('=') and a[1:].isdigit():
            return True
        else:
            return False


if __name__ == '__main__':
    q = Quiz()
