import importlib,sys
importlib.reload(sys)
import time
from datetime import datetime, date
import requests
import shutil
import os

from pathlib import Path

import pandas as pd

import zipfile

# 换算成kb,# 获取文件大小
def GetfileSizeKB(path):
    try:
        size = os.path.getsize(path)/1024
        return (size)
    except:
        print("获取文件大小错误")



# 本函数把要处理的ip读出来，放到list文件中
def getIPList(idDictTxt):
    # 读出需要处理的词云文件  topicTxt
    ipList=[]
    with open(idDictTxt, 'r') as fR:  # 读取文件
        lines=fR.readlines()  # 读出全部行
        for line in lines:
            if line != "\n":
                words=line.rstrip()
                temp=words.split('.0/', 1)
                ipString = temp[0][2:]
                # print(ipString)
                ipList.append(ipString)  #
    fR.close()
    return ipList
# zipFile 解压文件， zipPath 解压目录
def zipManage(zipFile,cvsPath):

    f=zipfile.ZipFile(zipFile, 'r')  # 压缩文件位置
    for file in f.namelist():
        f.extract(file, cvsPath)  # 解压位置
    f.close()

    # 删除原始zip文件，如果硬盘空间够的话，不建议执行，这条语句会降低效率
    # os.remove(zipFile)



def makeIPflowFromCVS_BK (cvsFile,ipList,outPath,beginTime):
    df=pd.read_csv(cvsFile)
    csvNumber = len(df)
    selectIPList = []
    i = 0
    df['ip'] = df['ip'][:-4]
    for index, row in df.iterrows():
        # 获得当前cvs文件中的ip地址
        currentIP = str(row['ip'])[:-4]
        # 对这条记录循环，判断是否在ip字典中
        if (index % 10000) == 0:
            print("合计：" + str(csvNumber) +  "条记录，当前处理的记录的ip地址为：" + str(currentIP) + ",index:"
                  + str(index) + "开始时间：" + str(beginTime) + "，已经找到" + str(i) + "条！")
        for ipDict in ipList:
            # print(ipDict + "," + currentIP)
            if ipDict == currentIP:
                # print("已经找到ip文件为：" + ipDict)
                selectIP={}
                selectIP['ipIndex'] = currentIP

                selectIP['ip'] = row['ip']
                selectIP['date']=row['date']
                selectIP['time']=row['time']
                selectIP['zone']=row['zone']
                selectIP['cik']=row['cik']
                selectIP['accession']=row['accession']
                selectIP['extention']=row['extention']
                selectIP['code']=row['code']
                selectIP['size']=row['size']
                selectIP['idx']=row['idx']
                selectIP['norefer']=row['norefer']
                selectIP['noagent']=row['noagent']
                selectIP['find']=row['find']
                selectIP['crawler']=row['crawler']
                selectIP['browser']=row['browser']

                selectIPList.append(selectIP)
                i=i + 1
    print(str(len(ipList)))

def makeIPflowFromCVS2 (cvsFile,ipList,outPath):
    df=pd.read_csv(cvsFile, low_memory=False)

    print("本文件记录条数：" + str(len(df)))
    # 生成关键ip
    df['nip']=df['ip'].str[:-4]

    testNumber = 1
    for ipDict in ipList:
        # 查找ipDict
        institutions=df[(df['nip'] == ipDict)]
        # 把找到的写入文件
        for index, row in institutions.iterrows():
            testNumber = testNumber + 1
            if (testNumber % 1000) == 0:
                print(ipDict + "：在[" + cvsFile + "]文件中已找到第" + str(testNumber) + "条，正在写入......")
            # 打开指定文件，文件名以查找的IP命名，分别以追加的形式写入文件
            outFile=outPath + "\\" + ipDict + ".csv"

            # 追加的形式打开
            with open(outFile, 'a') as f1:
                temp = ipDict + "," + str(row['ip']) + "," + str(row['date']) \
                       + "," + str(row['time']) + "," + str(row['zone']) + "," \
                       + str(row['cik']) + "," + str(row['accession']) + "," \
                       + str(row['extention']) + "," + str(row['code']) + "," \
                       +  str(row['size']) + "," + str(row['idx']) + "," \
                       + str(row['norefer']) + "," + str(row['find']) + "," \
                       + str(row['crawler']) + "," + str(row['browser'])
                f1.write(temp + "\n")


def makeIPflowFromCVS (cvsFile,ipList,outPath,beginTime,fileTotalNumber,fileCurrentNumer,allBeginTime):
    df=pd.read_csv(cvsFile)
    csvNumber = len(df)
    selectIPList = []
    i = 1
    for ipDict in ipList:
        # 寻找指定ip
        for index, row in df.iterrows():
            # 获得当前cvs文件中的ip地址
            currentIP = str(row['addip'])
            # 对这条记录循环，判断是否在ip字典中
            if (index % 10000) == 0:
                # 开始时间
                localtime=time.localtime(time.time())
                currentTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

                desc = "查找数据！本次处理共有"+ str(fileTotalNumber) + "个文件，当前是第" \
                       + str(fileCurrentNumer) + "个！" +"文件为：" + cvsFile \
                       + ",合计23个ip，正在查找第" + str(i) + "个IP:" + str(ipDict) +"，共有" + str(csvNumber) + "条记录,当前处理的是文件第" + str(index) + "条记录,本文件开始时间是：" \
                       + str(beginTime) +"，当前时间是：" + str(currentTime) + ",总开始时间：" + str(allBeginTime)
                print(desc)
            # print(ipDict + "," + currentIP)
            if ipDict == currentIP:
                # 打开指定文件，文件名以查找的IP命名，分别以追加的形式写入文件
                outFile=outPath + "\\" + ipDict + ".csv"
                # 追加的形式打开
                with open(outFile, 'a') as f1:
                    temp = currentIP + "," + str(row['ip']) + "," + str(row['date']) \
                           + "," + str(row['time']) + "," + str(row['zone']) + "," \
                           + str(row['cik']) + "," + str(row['accession']) + "," \
                           + str(row['extention']) + "," + str(row['code']) + "," \
                           +  str(row['size']) + "," + str(row['idx']) + "," \
                           + str(row['norefer']) + "," + str(row['find']) + "," \
                           + str(row['crawler']) + "," + str(row['browser'])
                    f1.write(temp + "\n")
        i = i + 1


def check_ip(argv):
    url1='http://freeapi.ipip.net/'  # 中国网站
    url2='http://ip-api.com/json/'  # 外国网站


    # args = sys.argv[1]
    url1=url1 + argv
    url2=url2 + argv + "?lang=zh-CN"
    response=requests.get(url1)
    response2=requests.get(url2)

    print(response.text)
    print(response2.text)

    f=eval(response2.text)
    print(argv + "====================")
    print("所属国家" + f['country'])

    print("国家代码 " + f['countryCode'])
    print("地区 " + f['region'])
    print("地区 " + f['regionName'])
    print("城市 " + f['city'])
    print("(经度，维度) " + str(f['lon']) + " " + str(f['lat']))
    print("时区 " + f['timezone'])
    print("isp " + f['isp'])
    print("组织 " + f['org'])


# 获得指定目录下的全部txt文件名称集合，该函数可以汇总txt或者pdf文件
def getAllFileName(file_dir,fileType):

    pdf_list=[]  # 定义pdf文件列表
    # 在file_dir目录下循环，找出全部文件  walk函数包括子目录
    for files in os.walk(file_dir):
        # 通过变量调试，分析出files[2]就是文件列表,针对这个循环，判断并取出pdf文件
        for file in files[2]:
            # 判断是否是pdf文件
            if (os.path.splitext(file)[1] == fileType) :
                # 将pdf文件加入列表
                pdf_list.append(os.path.join(file))

    return pdf_list

# 切割csv文件
def splitCSV(cvsFile,cutNumber):
    split_size=cutNumber  # 子文件行数最大值10万行
    res_file_path=Path(cvsFile)

    # cacheSize设置缓存
    tmp=pd.read_csv(res_file_path,low_memory=False)
    columns=tmp.columns.to_list()
    idx=0
    while (len(tmp) > 0):
        start=1 + (idx * split_size)
        tmp=pd.read_csv(res_file_path,
                        header=None,
                        names=columns,
                        skiprows=start,
                        nrows=split_size)
        if len(tmp) <= 0:
            break
        file_name=res_file_path.name.split(".")[0] + "_{}_{}".format(start, start + len(tmp)) + ".csv"
        file_path=res_file_path.parent / file_name
        tmp.to_csv(file_path, index=False)
        idx+=1
        print(file_name + "\t保存成功")
    os.remove(cvsFile)


# 主程序,
def mainCVS2(cvsFilesPath,logFile,ipDictPath,outPath,cacheSize,absYear):
    # 开始时间
    localtime=time.localtime(time.time())
    allBeginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    # 初始化ip字典
    ipList=getIPList(ipDictPath)

    # 读取全部指定zipFiles目录下的文件到一个ziplist中
    csvFileList=getAllFileName(cvsFilesPath, ".csv")

    fileTotalNumber=len(csvFileList)
    myi=1

    print("2-2、SECcsv程序启动，正在读入带处理文件，请稍后.....")

    # 循环处理文件
    for csvFile in csvFileList:
        # 开始时间
        localtime=time.localtime(time.time())
        thisBeginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

        mycsvFile=cvsFilesPath + csvFile

        # 只循环一遍大文件，在每条依次循环23遍
        makeIPflowFromCVS2(mycsvFile, ipList, outPath, thisBeginTime, fileTotalNumber, myi, allBeginTime,cacheSize)

        localtime=time.localtime(time.time())
        thisEndTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

        desc="2-2、SECcsv程序处理[" + str(absYear) + "]数据：开始时间：" + str(allBeginTime) + ",合计：" + str(fileTotalNumber) + "个文件，已处理完第" + str(myi) \
             + "个,thisBegin：" + str(thisBeginTime) + ",thisEnd：" + str(thisEndTime)
        print(desc)

        with open(logFile, 'a') as f1:
            f1.write(absYear + ":" + csvFile + "，合计:"+ str(fileTotalNumber) +"个文件,当前为："
                     + str(fileTotalNumber) + "-" + str(myi) + "，begin："+ thisBeginTime + ",end:" + thisEndTime + "\n")
        f1.close()

        myi=myi + 1
    print("总体处理完成，具体时间如下：")
    print(allBeginTime)

    localtime=time.localtime(time.time())
    end_localtime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    print(end_localtime)

# 查询ip所属区域
def checkIPFromSEC(ipDictPath):

    ipList=getIPList(ipDictPath)

    for myip in ipList:
        ipTemp = myip + ".0"
        check_ip(ipTemp)

# 切割文件 cutNumber设置切割记录数量, cacheSize设置缓存
def splitAllCSV(zipFilesPath,cvsFilesPath,ipDictPath,cutNumber, cacheSize,yearName):

    ipList=getIPList(ipDictPath)

    # 读取全部指定zipFiles目录下的文件到一个ziplist中
    zipFileList=getAllFileName(zipFilesPath, ".zip")

    # 循环处理文件
    fileTotalNumber=len(zipFileList)

    # 总开始时间
    tempTime=time.localtime(time.time())
    allBeginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", tempTime))

    # 循环切割大文件
    i=1
    zipNumber=len(zipFileList)
    for zipFile in zipFileList:
        # 开始时间
        localtime=time.localtime(time.time())
        beginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))


        # 解压缩，把zipFile转化到cvsFiles，zipFileList中文件不带路径，需要加上
        zipManage(zipFilesPath + zipFile, cvsFilesPath)
        # 读取解压缩的文件
        csvFile=zipFile[:-4] + ".csv"

        cvsFullFile=cvsFilesPath + csvFile
        # 预处理文件，切割文件
        splitCSV(cvsFullFile, cutNumber, cacheSize)

        # 开始时间
        localtime=time.localtime(time.time())
        endTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

        # 计算本次处理花费多少秒
        seconds=(endTime - beginTime).seconds

        desc="2-1 数据预处理，解压和切割文件中！" + yearName + "：本次需要处理" + str(zipNumber) + "个文件，""当前切割第" + str(i) + "个文件，文件名称：" \
             + zipFilesPath + zipFile + "，其中本次开始时间：" + beginTime + "，本次结束时间：" + str(endTime) + ",总开始时间：" + allBeginTime
        print(desc)

        i=i + 1

    desc = "2-1、数据预处理完成！" + yearName + "目录下，合计：" + str(zipNumber) + "个文件，已全部切割完成，保存在csvFiles目录下！"
    print(desc)
    localtime=time.localtime(time.time())
    end_localtime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    print("begin:" + allBeginTime)
    print("end:" + end_localtime)


if __name__ == '__main__':

    # 程序说明：
    # 1、要求保持相对目录结构不变
    # 2、两个参数需要修改，absPath,absYear
    # ==============================================
    # 绝对路径
    absPath="E:\\duduPython\\jqCSV\\"
    # 需要处理数据的年的列表
    absYearList = ['2003','2004','2005','2006','2007','2008','2009',
               '2010','2011','2012','2013','2014','2015','2016','2017']

    # 设置csv文件大小,参数为KB，用来决定是否移到bigFiles
    csvFileSizeSetup = 3600000
    # 配置切割文件的大小，3000万条为一个文件
    cutNumber = 30000000
    # # 读入文件的缓存大小,low_memory=False
    # cacheSize = 500000
    # ===============================================

    # 写日志文件
    logFile=absPath + "data\\log.txt"

    # 未处理的大文件名单
    bigSizeFilesPath = absPath + "bigFiles\\"
    # 名单
    bigSizeFilesPFile = bigSizeFilesPath + "\\big_csv_List.txt"

    # ip字典文件路径
    ipDictPath=absPath + "data\\ipDict.txt"
    # 最后生成文件的路径
    outPath=absPath + "\\outPath\\"

    # 记录本次程序运行处理的年的集合
    scvDirectoryList = []

    # 总开始时间
    time_start_program = time.time()  # 记录开始时间

    file_count = 1 # 本次处理的全部文件计数器

    # 初始化IP字典
    ipList=getIPList(ipDictPath)

    # 让所有年循环起来处理
    for absYear in absYearList:
        # 设置解压后的cvs的目录
        # zipFilesPath=absPath + "zipFiles\\" + absYear + "\\"
        csvFilesPath=absPath + "csvFiles\\" + absYear + "\\"

        # 如果不存在指定年的目录，则结束本次循环
        isExists=os.path.exists(csvFilesPath)
        if not isExists:
            print("指定年["+ str(absYear) +"]的目录不存在！")
            continue
        else:
            scvDirectoryList.append(csvFilesPath)

    print("本次处理的文件目录：" )
    print(scvDirectoryList)

    # 处理当前存在年的目录数据
    for scvDirect in scvDirectoryList:


        # 读取全部指定zipFiles目录下的文件到一个ziplist中
        csvFileList=getAllFileName(scvDirect, ".csv")

        # 统计文件数量
        fileTotalNumber=len(csvFileList)
        # 当前目录下，文件计数器
        myi = 1
        print("SECcsv程序启动，当前处理[" + str(scvDirect) + "]数据，请稍后.....")

        # 条数超过3000万条记录的csv文件，进行移出到big文件夹
        print("===================超级大文件，移出处理=========")
        for csvFile in csvFileList:
            # 设置文件全目录
            mycsvFile=scvDirect + csvFile

            file_size = GetfileSizeKB(mycsvFile)
            # 文件大小大于默认处理文件的大小，则切割
            if file_size > csvFileSizeSetup:

                # 判断保存大文件目录是否存在，不存在就新建
                isExists=os.path.exists(bigSizeFilesPath)
                if not isExists:
                    os.makedirs(bigSizeFilesPath)

                # 移动文件
                src=os.path.join(scvDirect, csvFile)
                dst=os.path.join(bigSizeFilesPath, csvFile)
                # 移动文件#src为要移动的文件的路径，dst为目的路径
                shutil.move(src, dst)

                write_time=time.time()  # 记录结束时间
                write_time_bigCSV=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(write_time))

                desc = bigSizeFilesPath + csvFile + ",size:" + str(int(file_size/1024)) +"M,移入时间：" + write_time_bigCSV
                print(desc)
                with open(bigSizeFilesPFile, 'a') as f1:
                    f1.write(desc + "\n")
                f1.close()


        print("=================" + scvDirect + ":本目录下文件预处理完成，进入查找阶段.....")

        # 重新读取全部指定zipFiles目录下的文件到一个ziplist中
        csvFileList=getAllFileName(scvDirect, ".csv")
        # 循环查找ip处理文件
        for csvFile in csvFileList:
            # 开始时间
            time_begin_scvFile=time.time()  # 记录一个文件的开始时间

            # 设置文件全目录
            mycsvFile=scvDirect + csvFile

            print("")
            print("================正在处理"+ str(mycsvFile) + "，请稍后......=====================")

            # 只循环一遍大文件，在每条依次循环23遍
            makeIPflowFromCVS2(mycsvFile,ipList,outPath)

            time_end_scvFile=time.time()  # 记录结束时间

            # 计算耗时
            time_sum_program=int(time_end_scvFile - time_begin_scvFile)
            # 程序启动到现在的总耗时
            from_begin_to_now_total_time = int((time_end_scvFile - time_start_program)/60)

            beginTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_begin_scvFile))
            endTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_end_scvFile))
            beginTime_program=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_start_program))

            desc= csvFile + "：程序启动时间："+ str(beginTime_program)  + ",已处理文件： " + str(file_count) \
                 + "个!合计耗时" + str(from_begin_to_now_total_time) + "分钟！当前处理目录：" \
                 + scvDirect + ",本目录共有" + str(fileTotalNumber) + "个文件，" \
                 + "当前目录已完成" + str(myi) + "个，本次耗时：" + str(time_sum_program) \
                 + "秒，thisBegin：" + str(beginTime) + ",thisEnd：" + str(endTime)
            print(desc)

            with open(logFile, 'a') as f1:
                f1.write(csvFile + ",写入时间：" + str(endTime) + ",耗时：" + str(time_sum_program) + "秒\n")
            f1.close()

            # 删除处理后的scv文件
            os.remove(mycsvFile)

            myi=myi + 1
            file_count = file_count + 1
        print("")
    time_end_program = time.time()  # 记录结束时间
    time_sum_program=int((time_end_program - time_start_program)/60)  # 计算的时间差为程序的执行时间，单位为秒/s

    begin_program=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_start_program))
    end_program=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_end_program))

    desc = "本次数据全部处理完成！总耗时：" + str(time_sum_program) \
           + "分钟，合计处理文件" + str(file_count) + ",begin:" + begin_program + "---" + end_program
    print(desc)
