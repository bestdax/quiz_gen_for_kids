from pdf import PDF
from quizzes import Quiz

pdf = PDF()
types_of_quiz = ['10以内加减法',
                 '20以内加减法',
                 '100以内加减法',
                 '表内乘法接10以内加减法']
# 选择题型，页数，是否显示日期
index = [2, ]
pages = 1
date = True

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
