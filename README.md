# 口算题自动生成

生成给孩子用的练习题，具体的设置请在config文件中修改。config文件会在第一次运行后自动生成。

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
