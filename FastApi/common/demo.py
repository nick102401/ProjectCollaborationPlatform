

if __name__ == '__main__':
    month = "JanFebMarAprMayJunJulAugSepOctNovDec"  # 将所有月份简写存到month中

    n = input("请输入月份代表的数字:")

    pos = (int(n) - 1) * 3  # 输入的数字为n,将(n-1)*3,即为当前月份所在索引位置

    findmonth = month[pos:pos + 3]

    print("月份的简写为：" + findmonth + ".")