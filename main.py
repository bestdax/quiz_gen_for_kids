import os
from parser import parser
from pdf import PDF
from quizzes import Quiz
import glob

default_config = '''设置文件版本V0.2
这个文件中保存的是生成试题的设置，您可以根据自己的需要生成需要的习题。
说明：
- 所有开关可以设置的选项为`True`、`False`、`是`、`否`，或者留空。
- 题型混合选项在多个题型时生效，默认选项为否。
- 每个题型前后都要用####包起来。
- 同一题型各个运算的数值之间请用-----分隔开。
- 运算符+-*/分别代表加减乘除。
- 如果需要在多个运算符中随机选，可以列出多个运算符，比如+-。
- 数值范围如果写10的话，最大出现的值为9。
- 如果不想随机，需要固定为一个数值的话，写成`=10`。
- 运算结果限制可以限制运算的结果不要超出某个范围，比如加法结果不超过10或者不小于5等等，如果不写则不设限。
- 进位限制只对加法有效，如果设置成`是`或者`True`会强制生成进位的加法，为空，`否`或者`False`不设限。
- 退位限制只对减法有效，如果设置成`是`或者`True`会强制生成进位的减法，为空，`否`或者`False`不设限。
- 是否加括号可以设置算式是否加括号。
- 如果有多个算式规则的话，比重会生效，会生成相应比例数目的算式，范围为0~1，比如0.75。
- 页数可以设置生成PDF文件的的页数，如果不填则默认为1。
- 是否显示日期，可以设置是否显示日期。
- 每页习题数量，默认值为100。

试题输出文件夹：~/Desktop
题型混合：否
页数：1
是否显示日期：是
每页习题数量：100

###############################################################################
算式规则：
比重：1
数值a范围：7
显示：是
-------------------------------------------------------------------------------
运算符：*
数值b范围：7
运算结果上限：
运算结果下限：
进位限制：
退位限制：
是否加括号：
显示：是
-------------------------------------------------------------------------------
运算符：+-
数值c范围：100
运算结果上限：
运算结果下限：
进位限制：
退位限制：
是否加括号：
显示：否
###############################################################################
算式规则：
比重：
数值a范围：
-------------------------------------------------------------------------------
运算符：
数值b范围：
运算结果上限：
运算结果下限：
进位限制：
退位限制：
是否加括号：
-------------------------------------------------------------------------------
运算符：
数值c范围：
运算结果上限：
运算结果下限：
进位限制：
退位限制：
是否加括号：
###############################################################################
    '''
# 如果有设置文件就读取并执行没有的话就新建一个
if not os.path.exists('config'):
    with open('config', 'w') as c:
        config = default_config
        c.write(config)
else:
    for config_file in glob.glob('config*'):
        with open(config_file, 'r+') as c:
            config = c.read()
            if 'V0.2' not in config:
                config = default_config
                c.seek(0)
                c.truncate()
                c.write(config)

        paras = parser(config)
        pdf = PDF()
        user = config_file[7:]
        for i in range(paras['global']['pages']):
            pdf.add_page()
            pdf.set_title('四则运算练习')
            pdf.set_date(paras['global']['date'])
            q = Quiz()
            quizzes = q.bulk_quiz_gen(paras)
            pdf.set_quizzes(quizzes=quizzes)
        quiz_dir = paras['global']['quiz_dir']
        pdf_filename = os.path.join(quiz_dir, f'{user}.pdf' if user else 'quizzes.pdf')
        pdf.output(f'{pdf_filename}', 'F')
