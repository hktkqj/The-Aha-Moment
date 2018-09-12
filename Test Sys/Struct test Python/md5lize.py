import hashlib
import string

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()

def Encrypt(word,key) :
    info=''
    s = string.printable[0:62]
    for i in range(0, len(word)):
        info += s[(s.find(word[i]) + s.find(key[i % len(key)])) % 62]
    return info

def Decrypt(word='',key='') :
    flag = ''
    s = string.printable[0:62]
    for i in range(0, len(word)):
        flag += s[(s.find(word[i]) + 62 - s.find(key[i % len(key)])) % 62]
    return flag

if __name__ == '__main__':
    str="123456"
    print(md5lize(str))
    print(Encrypt(str,'112233asd'))