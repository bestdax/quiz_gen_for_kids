import os

from pdf import PDF
from quizzes import Quiz

pdf = PDF()
default_config = '''#设置文件版本V0.1
# 这个文件中保存的是生成试题的设置
# 您可以根据自己的需要生成需要的习题
# 设置的方法如下：
# 在paras后面的填上习题的代码
# 示例：
# ['*(+-) 10 100 0.8'， '(+-) 100 0.2']
# 第一段表示乘法后面接加法或者减法，后面的10对应乘法的数字边界最大为9
# 100是后面加减法的边界
# 0.8代表试题数量的权重，如果一共100题的话，这个题型有80题
# 运算符+-*/分别代表加减乘除
paras = ['(+-) 100 0.75',
         '* 7 0.25']
pages = 1
date = True
qty = 100
    '''

# 如果有设置文件就读取并执行没有的话就新建一个
if os.path.exists('config'):
    with open('config', 'r+') as c:
        config = c.read()
        if 'V0.1' in config:
            exec(config)
        else:
            config = default_config
            c.seek(0)
            c.truncate()
            c.write(config)
else:
    with open('config', 'w') as c:
        c.write(default_config)
        exec(default_config)


for i in range(pages):
    pdf.add_page()
    pdf.set_title('四则运算练习')
    pdf.set_date(date)
    q = Quiz()
    quizzes = q.bulk_quiz_gen(paras, qty=qty)
    pdf.set_quizzes(quizzes=quizzes)
pdf.output('quizzes.pdf', 'F')