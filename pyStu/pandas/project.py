import os
from pathlib import Path
import pandas as pd
import numpy as np

path = './data'
fileNames = os.listdir(path)
file1_name = fileNames[0]
file1_path = path+'/'+file1_name

# 读取file1
file1 = pd.read_excel(file1_path,skiprows=5,skipfooter=3)

tarr = file1.values

def getCol(list):
    target_col = []
    for i in range(len(list)):
        tmp = list[i]
        if tmp != '合计':
            target_col.append(i)
    return target_col

def getNameAndIndex(list):
    stationsName = []
    stationsIndex = []

    for i in range(2, len(list)):
        stationsIndex.append(i)
        stationsName.append(list[i])

    return [stationsName,stationsIndex]

tar_col = getCol(tarr[0])
[names,indexs] = getNameAndIndex(tarr[0])

# 读取数据源
def getNewInAndOut(f):
    file = pd.read_excel(f,skiprows=5,skipfooter=3,usecols=tar_col)
    arr = file.values
    d_in = {}
    d_out = {}

    # 初始化进出站数据
    for i in indexs:
        d_in[i] = []
        d_out[i] = []

    # 按行迭代
    for i in range(43,len(arr)):
        row = arr[i]
        inputList = None
        stationType = row[1]

        if stationType == '进站':
            inputList = d_in
        elif stationType == '出站':
            inputList = d_out
        else:
            continue

        # 存储第j列的进出站数据
        for j in range(2,len(row)):
            content = row[j]
            inputList[j].append(content)

    # 整理进出站数据，转为matrix
    in_list = []
    out_list = []
    for key in d_in:
        in_list.append(d_in[key])
        out_list.append(d_out[key])

    return [in_list,out_list]

# 读文件
def readFile(path):
    file = pd.read_csv(path)
    arr = file.values.tolist()
    return arr

# 写文件，有文件读文件
def writeInAndOut(f, fileIn='',fileOut=''):
    [in_list, out_list] = getNewInAndOut(f)
    in_oldArr = []
    out_oldArr = []

    if fileIn:
        in_oldArr = readFile(path+'/'+fileIn)
    if fileOut:
        out_oldArr = readFile(path+'/'+fileOut)

    if len(in_oldArr)>0 and len(out_oldArr)>0 :
        for i in range(len(in_oldArr)):
            in_oldArr[i] += in_list[i]
            out_oldArr[i] += out_list[i]
        mode = 'r+'
    else:
        in_oldArr = in_list
        out_oldArr = out_list
        mode = 'w'

    print(mode)
    df_in = pd.DataFrame(in_oldArr)
    df_out = pd.DataFrame(out_oldArr)

    df_in.to_csv('./data/in.csv',mode=mode,header=True,index=None)
    df_out.to_csv('./data/out.csv',mode=mode,header=True,index=None)


writeInAndOut(file1_path,'in.csv','out.csv')




