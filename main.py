import os

from pdf import PDF
from quizzes import Quiz

pdf = PDF()
types_of_quiz = ['10以内加减法',
                 '20以内加减法',
                 '100以内加减法',
                 '表内乘法接10以内加减法',
                 '表内乘法']

# 如果有设置文件就读取并执行没有的话就新建一个
if os.path.exists('config'):
    with open('config', 'r') as c:
        config = c.read()
        exec(config)
else:
    config = '''
# 这个文件中保存的是生成试题的设置
# 以下是题型对应的编号
# 0     10以内加减法
# 1     20以内加减法
# 2     100以内加减法
# 3     表内乘法接10以内加减法
# 4     表内乘法
# 在以下设置中修改以生成想要的试题
index = [2, ]
pages = 1
date = True
    '''
    with open('config', 'w') as c:
        c.write(config)
        exec(config)

for i in range(pages):
    pdf.add_page()
    pdf.set_title('四则运算练习')
    pdf.set_date(date)
    q = Quiz()
    types = []
    for i in index:
        types.append(types_of_quiz[i])
    quizzes = q.bulk_quiz_gen(types)
    pdf.set_quizzes(quizzes=quizzes)
pdf.output('quizzes.pdf', 'F')
