import re
import sys
import os


def parser(config):
    # 从config里面找到几个必要的全局参数
    quiz_dir = re.search('试题输出文件夹：(.*)\n', config).group(1).strip()
    quiz_dir = os.path.expanduser(quiz_dir)
    date = re.search('是否显示日期：(.*)\n', config).group(1).strip()
    pages = re.search('页数：(.*)\n', config).group(1).strip()
    mix = re.search('题型混合：(.*)\n', config).group(1).strip()
    qty = re.search('每页习题数量：(.*)\n', config).group(1).strip()
    if not quiz_dir:
        quiz_dir = os.path.expanduser('~/Desktop')
    if date in ['是', 'True']:
        date = True
    else:
        date = False
    if mix in ['是', 'True']:
        mix = True
    else:
        mix = False
    try:
        pages = int(pages)
    except ValueError:
        pages = 1
    else:
        pass
    try:
        qty = int(qty)
    except ValueError:
        qty = 100
    else:
        pass

    paras = {'global': {
        'quiz_dir': quiz_dir,
        'date': date,
        'qty': qty,
        'pages': pages,
        'mix': mix
    }}
    rule_block = re.search('^#{10,} *\n(.+)^#{10,} *$', config, flags=re.DOTALL | re.MULTILINE).group(1)
    rules = re.split(r'#{10,}\n *', rule_block)
    paras['rules'] = []
    for rule in rules:
        if rule_parser(rule):
            paras['rules'].append(rule_parser(rule))

    return paras


def rule_parser(rule):
    blocks = re.split('-{10,} *', rule)
    rules = blocks_parser(blocks)

    return rules


def blocks_parser(blocks):
    rule_parsed = []
    # 获取比重和数值a范围，如果存在就添加到参数列表里
    weight = re.search('比重：(.*)', blocks[0]).group(1)
    a = re.search('数值a范围：(.*)', blocks[0]).group(1)
    display = re.search('显示：(.*)', blocks[0]).group(1)
    if weight:
        try:
            weight = float(weight)
        except ValueError:
            print('权重参数或者数值a设置出错!')
    if display in ['是', 'True', 'y', 'Yes']:
        display = True
    else:
        display = False

    if all([weight, a]):
        rule_parsed.append(weight)
        rule_parsed.append(a)
        rule_parsed.append(display)
    for block in blocks[1:]:
        ops = re.search('运算符：(.*)', block).group(1)
        number = re.search('数值.*范围：(.*)', block).group(1)
        ceiling = re.search('运算结果上限：(.*)', block).group(1)
        floor = re.search('运算结果下限：(.*)', block).group(1)
        carry = re.search('进位限制：(.*)', block).group(1)
        borrow = re.search('退位限制：(.*)', block).group(1)
        brackets = re.search('是否加括号：(.*)', block).group(1)
        display = re.search('显示：(.*)', blocks[0]).group(1)

        limits = {
            'ceiling': ceiling,
            'floor': floor,
            'carry': carry,
            'borrow': borrow,
            'brackets': brackets,
            'display': display
        }
        for key in limits.keys():
            if limits[key] in ['是', 'True', 'y', 'Yes']:
                limits[key] = True
            elif limits[key].isdigit():
                limits[key] = int(limits[key])
            else:
                limits[key] = False
        if not limits['ceiling']:
            limits['ceiling'] = sys.maxsize
        if not limits['floor']:
            limits['floor'] = 0
        if all([weight, a, ops, number]):
            rule_parsed.append(ops)
            rule_parsed.append(number)
            rule_parsed.append(limits)
    return rule_parsed


def empty_rule_checker(rule):
    pass
