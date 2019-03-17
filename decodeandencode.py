import factoradic
import bisect
import numpy as np

TEMPLATE = ':abcdefghijklmnopqrstuvwxyz'


# 4位最大阶乘数:3210 = 3*3! + 2*2! + 1*1! + 0*0! = 23
# 与4A4=24全排列一一对应

def seq2list(number):
    # 转换为阶乘数,依次弹出满列表对应下标即可
    new_numbers = (factoradic.to_factoradic(number) + [0] * 27)[:27][::-1]
    temp = list(TEMPLATE)
    return [temp.pop(i) for i in new_numbers]


def list2seq(mylist):
    # 加入空列表取下标,形成的数字作为阶乘数,转换为10进制即可
    new_strings = mylist[::-1]
    temp = []
    return factoradic.from_factoradic([bisect.insort(temp, c) or temp.index(c) for c in new_strings])


if __name__ == "__main__":
    result = seq2list(np.math.factorial(27)-np.math.factorial(24))
    print(result)
    result = list2seq(list(':abcdefghijklmnopqrstuvwxzy'))
    print(result)
