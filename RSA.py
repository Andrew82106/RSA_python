import random
import math
from sys import exit


def fastExpMod(b, e, m):
    """
    实现一个快速幂
    :param b:
    :param e:
    :param m:
    :return:
    """
    result = 1
    e = int(e)
    while e != 0:
        if e % 2 != 0:
            e -= 1
            result = (result * b) % m
            continue
        e >>= 1
        b = (b * b) % m
    return result


def miller_rabin_test(n):
    """
    使用miller_rabin_test进行大数测验
    :param n:
    :return:
    """
    p = n - 1
    r = 0
    while p % 2 == 0:
        r += 1
        p /= 2
    try:
        b = random.randint(2, n - 2)
    except:
        raise Exception(f"random.randint(2, n - 2):random.randint(2, {n - 2})")
    if fastExpMod(b, int(p), n) == 1:
        return True
    for i in range(0, 7):
        if fastExpMod(b, (2 ** i) * p, n) == n - 1:
            return True
    return False


def create_prime_num(keylength):
    """
    创建素数
    :param keylength:
    :return:
    """
    while True:
        n = random.randint(4, keylength)
        if n % 2 != 0:
            found = True
            for i in range(0, 10):
                if miller_rabin_test(n):
                    pass
                else:
                    found = False
                    break
            if found:
                return n


def create_keys(keylength):
    """
    创建密钥
    :param keylength:
    :return:
    """
    p = create_prime_num(keylength / 2)
    q = create_prime_num(keylength / 2)
    n = p * q
    fn = (p - 1) * (q - 1)
    e = choose_a_E(fn)
    d = match_d(e, fn)
    return n, e, d


def choose_a_E(fn):
    """
    创建公钥e
    :param fn:
    :return:
    """
    while True:
        e = random.randint(0, fn)
        if math.gcd(e, fn) == 1:
            return e


def match_d(e, fn):
    """
    找到和e匹配的d
    :param e:
    :param fn:
    :return:
    """
    d = 0
    while True:
        if (e * d) % fn == 1:
            return d
        d += 1


def encrypt(M, e, n):
    """
    加密
    :param M:
    :param e:
    :param n:
    :return:
    """
    return fastExpMod(M, e, n)


def decrypt(C, d, m):
    """
    解密
    :param C:
    :param d:
    :param m:
    :return:
    """
    return fastExpMod(C, d, m)


def display():
    print("______________________________RSA模拟器_______")
    print("q:退出")
    print("1:演示RSA加密，待加密密文由用户输入")
    print("2:演示RSA加密，待加密密文由rsa.txt指定")
    print("请输入操作码")
    print("______________________________RSA模拟器_______")


en = ""


def encrypt_file():
    global en
    print(">>>>>>>>>>>>>>加密过程：")
    f = open('./rsa.txt', "r")
    mess = f.read()
    print(f"INFO：：待加密原文：{mess}")
    f.close()
    n, e, d = create_keys(1024)
    print("INFO：：密钥生成结果：（n:", n, " ,d:", d, ") ", f"公钥为：e:{e}")
    s = ''
    for ch in mess:
        c = chr(encrypt(ord(ch), e, n))
        s += c
    try:
        print(f"INFO：：Encrypt Done! 加密结果：{str(s)}")
    except:
        print("INFO：：由于字符集原因，加密结果无法显示")
    en = str(s)
    return n, e, d


def decrypt_file(n, d):
    print(">>>>>>>>>>>>>>解密过程：")
    mess = en
    s = ''
    try:
        print(f"INFO：：读取的密文为：{mess}")
    except:
        print("INFO：：由于字符集原因，密文无法显示")
    print("INFO：：密钥为：（n:", n, " ,d:", d, ") ")
    for ch in mess:
        c = chr(decrypt(ord(ch), d, n))
        s += c
    f = open("rsa-2.txt", "w", encoding='utf-8')
    f.write(str(s))
    print(f"INFO：：Decrypt Done! 解密结果：{str(s)}")


if __name__ == '__main__':
    display()
    while True:
        c = input(">>>")
        # c = '2'
        if c == 'q':
            exit(0)
        elif c == '2':
            n, e, d = encrypt_file()
            decrypt_file(n, d)
        elif c == '1':
            f = open('./rsa.txt', 'w', encoding='utf-8')
            f.write(input("输入待加密密文："))
            print("INFO：：密文存储至rsa.txt")
            f.close()
            n, e, d = encrypt_file()
            decrypt_file(n, d)
        else:
            print("ERROR：：指令码错误")
        display()
