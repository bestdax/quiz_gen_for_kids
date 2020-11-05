import os
from parser import Parser
from pdf import PDF
from quizzes import Quiz

pdf = PDF()

# 如果有设置文件就读取并执行没有的话就新建一个
if os.path.exists('config'):
    with open('config', 'r') as c:
        config = c.read()

else:
    config = '''这个文件中保存的是生成试题的设置，您可以根据自己的需要生成需要的习题。
说明：
- 所有开关可以设置的选项为`True`、`False`、`是`、`否`，或者留空。
- 题型混合选项在多个题型时生效，默认选项为否。
- 每个题型前后都要用####包起来。
- 运算符+-*/分别代表加减乘除。
- 如果需要在多个运算符中随机选，可以列出多个运算符，比如+-。
- 数值范围如果写10的话，最大出现的值为9。
- 如果不想随机，需要固定为一个数值的话，写成`=10`。
- 运算结果限制可以限制运算的结果不要超出某个范围，比如加法结果不超过10，如果不写则不设限。
- 进位限制只对加法有效，如果设置成`是`或者`True`会强制生成进位的加法，为空，`否`或者`False`不设限。
- 退位限制只对减法有效，如果设置成`是`或者`True`会强制生成进位的减法，为空，`否`或者`False`不设限。
- 是否加括号可以设置算式是否加括号。
- 如果有多个算式规则的话，比重会生效，会生成相应比例数目的算式，范围为0~1，比如0.75。
- 页数可以设置生成PDF文件的的页数，如果不填则默认为1。
- 是否显示日期，可以设置是否显示日期。
- 每页习题数量，默认值为100。

题型混合：否
页数：1
是否显示日期：是
每页习题数量：100

###############################################################################
算式规则：
运算符：*
数值a范围：7
数值b范围：7
运算结果限制：
进位限制：
退位限制：
是否加括号：
运算符：+-
数值c范围：100
运算结果限制：
进位限制：
退位限制：
是否加括号：
比重：1
###############################################################################
算式规则：
运算符：
数值a范围：
数值b范围：
运算结果限制：
进位限制：
退位限制：
是否加括号：
运算符：
数值c范围：
运算结果限制：
进位限制：
退位限制：
是否加括号：
比重：1
###############################################################################
    '''

with open('config', 'w') as c:
    c.write(config)

p = Parser(config)
print(p.mix, p.pages, p.date, p.qty, p.paras)

# for i in range(pages):
#     pdf.add_page()
#     pdf.set_title('四则运算练习')
#     pdf.set_date(date)
#     q = Quiz()
#     quizzes = q.bulk_quiz_gen(paras, qty=qty)
#     pdf.set_quizzes(quizzes=quizzes)
# pdf.output('quizzes.pdf', 'F')
