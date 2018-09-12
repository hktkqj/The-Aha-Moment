#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib.request

def Get_All(url) :
    page = urllib.request.urlopen(url)
    page_file = page.read()
    return page_file

if __name__ == '__main__':
    result = Get_All("http://222.24.192.216:8085/image/")
    path_file = open("image.txt","w")
    path_file.write(str(result))
    path_file.close()






