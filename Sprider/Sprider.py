#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import urllib.request

def Get_All(url) :
    page = urllib.request.urlopen(url)
    page_file = page.read()
    return page_file

if __name__ == '__main__':
    path_file = open("image.txt", "r")
    All_Path_File = str(path_file.read())
    reg = r'image/(20173\d{5}\.jpg)"'
    imgre = re.compile(reg,flags=re.IGNORECASE);
    imglist = re.findall(imgre, All_Path_File)
    print(len(All_Path_File))
    _2016list = []
    _2017list = []
    for num in imglist:
        if num[3] == "6" and num[4] == "3":
            _2016list.append(num)
        elif num[3] == "7" and num[4] == "3":
            _2017list.append(num)
    cnt = 0
    print(len(_2017list))
    failed_list = []
    for student in range(0,len(_2017list)):
        time.sleep(1)
        try:
            f = open('C:\\Image\\2017\\' + _2017list[student], "wb")
            f.write(urllib.request.urlopen("http://222.24.192.216:8085/image/" + _2017list[student],timeout=5).read())
            f.close()
            cnt = cnt + 1
            print(str(cnt) + ": Success on student " + _2017list[student])
        except:
            print("Failed on " + _2017list[student])
            failed_list.append(_2017list[student])
    print(failed_list)



