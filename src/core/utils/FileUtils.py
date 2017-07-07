# -*- coding: utf-8 -*-

import json
import os

"""
项目绝对地址
"""
project_dir = os.getcwd()[:os.getcwd().find("/bird/")+6]

"""
相对路径转绝对路径
"""
def getPath(path):
    return project_dir+path

"""
读取文件
@file_name 文件名
@mode 写入模式（r:只读，w:覆盖写入，r+:继续写入）
"""
def openFile(file_name, mode = "rw+"):
    return open(getPath(file_name), mode)

"""
按行读取
"""
def readList(file_name):
    for line in openFile(file_name, mode="r").readlines():
        yield line.strip()

"""
按文件读取
"""
def readString(file_name):
    return openFile(file_name, mode="r").read()

"""
读取JSON
"""
def readJSON(file_name):
    return json.loads(readString(file_name))

"""
写入文本
@file_name 文件名
@text 内容
"""
def writeString(file_name, text):
    file = openFile(file_name, mode="w")
    file.write(text)
    file.flush()
    file.close()
"""
写入行
@file_name 文件名
@line 行内容
@isNew 是否覆盖
"""
def writeLine(file_name, line, isNew=False):
    if (isNew == False):
        file = openFile(file_name, mode="r+")
        file.read()
        file.write(line+"\n")
        file.flush()
        file.close()
    else:
        file = openFile(file_name, mode="w")
        file.write(line + "\n")
        file.flush()
        file.close()

"""
写入多行
@file_name 文件名
@line 行内容
@isNew 是否覆盖
"""
def writeLines(file_name, lines, isNew=False):
    if(isNew == False):
        file = openFile(file_name, mode="r+")
        file.read()
        for line in lines:
            file.write(line+"\n")
        file.flush()
        file.close()
    else:
        file = openFile(file_name, mode="w")
        for line in lines:
            file.write(line + "\n")
        file.flush()
        file.close()

"""
删除文件
"""
def remove(file_name):
    os.remove(file_name)

