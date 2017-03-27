from datetime import *

#两个数据集交换
def exchange(a,b):
    a = a ^ b
    b = a ^ b
    a = a ^ b

#生成当前时间
def getDate(f='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(f)