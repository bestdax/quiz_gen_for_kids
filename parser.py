import re


class Parser:
    def __init__(self, config):
        self.config = config
        # 从config里面找到几个必要的全局参数
        self.date = re.search('是否显示日期：(.*)\n', self.config).group(1).strip()
        self.pages = re.search('页数：(.*)\n', self.config).group(1).strip()
        self.mix = re.search('题型混合：(.*)\n', self.config).group(1).strip()
        self.qty = re.search('每页习题数量：(.*)\n', self.config).group(1).strip()
        if self.date in ['是', 'True']:
            self.date = True
        else:
            self.date = False

        if self.mix in ['是', 'True']:
            self.mix = True
        else:
            self.mix = False
        try:
            self.pages = int(self.pages)
        except:
            self.pages = 1
        else:
            pass

        try:
            self.qty = int(self.qty)
        except:
            self.qty = 100
        else:
            pass

        # 从config中读取算式规则
        self.paras = []
        p = re.compile(r'#+\n(.+?)###+?\n?', flags=re.DOTALL)
        expressions = p.findall(self.config)
        for index, exp in enumerate(expressions):
            ops = re.search('运算符：(.*)', exp).group(1).strip()
            result_border = re.search('运算结果限制：(.*)', exp).group(1).strip()
            carry = re.search('进位限制：(.*)', exp).group(1).strip()
            borrow = re.search('退位限制：(.*)', exp).group(1).strip()
            brackets = re.search('是否加括号：(.*)', exp).group(1).strip()
            values = re.findall('数值.+?范围：(.*)', exp)
            weight = re.search('比重：(.*)', exp).group(1).strip()
            paras = {'ops': ops,
                     'result_border': result_border,
                     'carry': carry,
                     'borrow': borrow,
                     'brackets': brackets,
                     'values': values,
                     'weight': weight
                     }
            for key, value in paras.items():
                if key == 'ops':
                    if not value:
                        paras['ops'] = None
                    else:
                        for c in ops:
                            if c not in '+-*/':
                                paras['ops'] = None
                                break

                if key == 'result_border':
                    if not value:
                        paras['result_border'] = False
                    else:
                        if value in ['是', 'True']:
                            paras['result_border'] = True
                        else:
                            paras['result_border'] = False
                if key == 'carry':
                    if value in ['是', 'True']:
                        paras['carry'] = True
                    else:
                        paras['carry'] = False
                if key == 'borrow':
                    if value in ['是', 'True']:
                        paras['borrow'] = True
                    else:
                        paras['borrow'] = False
                if key == 'brackets':
                    if value in ['是', 'True']:
                        paras['brackets'] = True
                    else:
                        paras['brackets'] = False
                if key == 'values':
                    if all(v == '' for v in value):
                        paras['values'] = None
                if key == 'weight':
                    if not value and (not self.paras):
                        paras['weight'] = 1
                    else:
                        try:
                            weight = int(weight)
                        except:
                            paras['weight'] = None
                        else:
                            if weight > 1 or weight <= 0:
                                paras['weight'] = None
            # 如果键值全部有意义就把设置添加进列表
            if all([value != None for value in paras.values()]):
                self.paras.append(paras)
            else:
            # 如果只有部分键值设置过了，提示缺哪些设置
                if any(paras.values()):
                    for k, v in paras.items():
                        if v == None:
                            print(f'第{index + 1}个算式规则中{k}的值设置不正确，请参看config文件中的说明。')
        if self.paras:
            if len(self.paras) == 1:
                paras[0]['weight'] = 1
            if len(self.paras) > 1:
                weights = []
                for para in self.paras:
                    weights.append(para['weight'])
                if sum(weights) > 1:
                    for weight in weights:
    def parser(self):
        pass
