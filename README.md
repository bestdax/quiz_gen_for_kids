# 口算题自动生成

生成给孩子用的练习题，具体的设置请在`config.yml`文件中修改。config文件会在第一次运行后自动生成。
以下为`config.yml`文件中的设置项的一些说明：
- `+-*/`对应加减乘除
- 每个用户的配置起始为`---`，结束于`...`。
```yaml
---
user: elsa # 用户名，生成的PDF文件会用这个来命名
global: # 全局变量
  mix: false # 不同题型是否混合
  pages: 1 # 生成PDF文件的页数
  show_date: true # 是否显示日期
  qty: 50 # 每页试题的数量
  quiz_dir: ~/Desktop # 输入PDF文件的目录
rules: # 口算题生成规则
  -
    weight: 1 # 如果有多个规则，每个规则生成试题所占的百分比，1为100%
    show_answer: false # 是否显示答案
    first_number: # 试题中第一个数字
      range: 100 # 数字的范围，有三种写法。 100 或者 10, 20 或者 =10
      display: true # 数字显示开关
    steps: # 计算步骤
      -
        operators: +- # 运算符，如果有多个的话就随机选择一个
        number: # 参与运算的第二个数字
          range: 100
          display: true
        limits: # 运算的一些条件设置
          ceiling: 15 # 运算结果的最大值
          floor: # 运算结果的最小值
          carry: # 是否强制进位
          borrow: # 减法时是否强制退位
          brackets: true # 是否加括号
      - # 运算的第二步设置开始
        operators: "*"  # 运算符是*号的时候要用引号包起来
        number:
          range: 10
          display: true
        limits:
          ceiling:
          floor:
          carry:
          borrow:
          brackets:
...
```
