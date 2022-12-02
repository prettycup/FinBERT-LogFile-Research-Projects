import importlib,sys
importlib.reload(sys)
from datetime import datetime
import time
import winsound

import jieba
import pkuseg
import thulac

import pdfplumber as pb
from wordcloud import WordCloud

import os
import shutil

import string

import collections

from PyPDF2 import PdfFileReader


# 统计词频率
def getWordCount(txtPath, outPath, wordNumber):
    object_list = []
    with open(txtPath, "r", encoding='UTF-8') as f:
        pureWord=f.read()

        object_list = pureWord.split(" ")

    # 词频统计
    word_counts=collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top=word_counts.most_common(wordNumber)  # 获取前10最高频的词

    print(word_counts_top)  # 输出检查
    print(len(word_counts_top))
    # with open(outPath, 'a', encoding='UTF-8') as one_txt:
    #     one_txt.write(word_counts_top)
    #
    # print(word_counts_top)  # 输出检查


# 词云
def getWrodColud(txtPath,pngPath,wordNumber):
    with open(txtPath, "r", encoding='UTF-8') as f:
        pureWord=f.read()

    # mask=imageio.imread("chinamap.jpg")
    word=WordCloud(background_color="white", \
                   width=800, \
                   height=600,
                   max_words=wordNumber, # 显示前100个词
                   font_path='simhei.ttf',
                   ).generate(pureWord)

    word.to_file(pngPath)


# 返回是否是叠词，同时去掉字母，数字的词
def isRepeatWord(mystring):
    i = 0
    long = len(mystring)

    # =======================
    while i <= long :
        # 此处可以调节循环词的数量，如果只检查2个叠词，就写2就行，如果这个词都检查，就写long
        if (i + 2) <= long:
            firstWord = str(mystring[i:i + 1])
            secondWord = str(mystring[i + 1:i + 2])

            # 判断是否是数字，是数字的话，则返回1，删除
            if (str(firstWord).isdigit() or str(secondWord).isdigit()) == True:
                # print("是数字：" + mystring)
                return 1
            # 判断是否是字母，是字母的话，返回值1，删除
            if ord(firstWord) in range(65, 91) or ord(firstWord) in range(97, 123):
                # print("是字母：" + mystring)
                return 1
            if ord(secondWord) in range(65, 91) or ord(secondWord) in range(97, 123):
                # print("是字母：" + mystring)
                return 1
            # 判断是否是标点符号，是的话，则返回1，删除
            punc1=string.punctuation
            if (firstWord in punc1) or (secondWord in punc1) == True:
                # print("是标点符号：" + mystring)
                return 1

            # 去掉重复的的字的词
            if firstWord == secondWord:
                # if (i >= 1):
                #     print(mystring)
                return 1
            else:
                firstWord = ""
                secondWord = ""
        i = i + 1

    return 0
    # =====================
    # if long <= 2:  # 表示只处理2个的叠词
    #     # 所有的字都从词中取出，按照顺序依次对比，只要重复就去掉
    #     while i <= long :
    #         # 此处可以调节循环词的数量，如果只检查2个叠词，就写2就行，如果这个词都检查，就写long
    #         if (i + 2) <= 2:
    #             firstWord = mystring[i:i + 1]
    #             secondWord = mystring[i + 1:i + 2]
    #
    #             if firstWord == secondWord:
    #                 return 1
    #         else:
    #             return 0
    #         i = i + 1
    #
    # return 0




# 在字符串中去掉单个汉字
def getNoOneWord(mystring):
    i = 0
    j = 0
    k = 0
    strLength = len(mystring)
    newString=""
    oneWord = ""
    repeatWord = ""
    while i < strLength:

        x = mystring[i:i + 1]
        if x.isspace() == False:  # 挑出全部字符
            oneWord = oneWord + x
        else:
            if len(oneWord)> 1:  #长度大于1，就保留下来
                # 此处增加是否是包括叠字，如果是叠字需要删除
                if isRepeatWord(oneWord) == 0:
                    newString = newString + " " + oneWord
                    j = j + 1
                else:
                    # 把重复的叠词找出来
                    repeatWord = repeatWord + " " + oneWord
            oneWord=""

        i=i + 1
    return newString, j,repeatWord


# 在字符串中去掉数字，因为标点符号都是单个字符，并且前后都是字符，
# 所以符合这个函数的逻辑就被去掉了
def getNoNuberString(mystring,punctuation):
    i = 0
    long = len(mystring)

    newString = ""
    while i < long:
        x = mystring[i:i+1]
        if not((x.isdigit()== True) or (x in punctuation)):
            newString = newString + x
        i = i +1
    # print(newString)
    return newString


# 去掉重复的双拼字以及数字
def deleteRepeatWordAndDigit(txtFile):
    with open(txtFile, 'r', encoding='UTF-8') as f:
        txtLines=f.readlines()

    myLine=""
    for line in txtLines:
        line=line.replace("\n", "")
        line=line.strip()
        line=line.lstrip()




def makeOneTxt(punctuation):
    # 第一次导入使用 new
    # txtPath="E:\\嘟嘟资料\\科研项目\\new\\txt\\"
    # sourcePath="回函 new platform（latest0606)"

    # 第二次导入使用 old
    txtPath = "E:\\嘟嘟资料\\科研项目\\第三次提交去掉stopwords中关键词20220803\\txt\\"
    sourcePath = "回函 new platform（latest0606)"


    oneTxt = "E:\\嘟嘟资料\\科研项目\\oneTxtNoDigitNoWordNoRepeat.txt"
    logTxt = "E:\\嘟嘟资料\\科研项目\\oneTxtNoDigitNoWordNoRepeat_logTxt.txt"

    # 读出指定目录下的txt文件
    txtNameList = getAllTxtFileName(txtPath)

    # 第一次初始化为0
    i = 0

    # 第二次初始化为：
    # i = 1
    # 对指定的文件集合进行循环处理

    # 定义需要去掉的标点符号字典


    for txt in txtNameList:
        txtFile = ""
        # 生成要访问的txt文件
        txtFile = txtPath + txt
        # 文件大小为空的不处理
        if (os.path.getsize(txtFile) > 0):
            # 把txt文件全部读出来，写成一行
            with open(txtFile, 'r', encoding='UTF-8') as f:
                txtLines = f.readlines()

            myLine = ""
            for line in txtLines:
                line = line.replace("\n", "")
                line = line.strip()
                line = line.lstrip()


                myLine = myLine + " " + line

            # 此处增加去掉数字函数
            myLine = getNoNuberString(myLine, punctuation)

            # 此处去掉一个词,增加了去掉重复字组成的叠词
            myLine,mlength,repeatWord = getNoOneWord(myLine)
            # print(myLine)


            with open(oneTxt, 'a', encoding='UTF-8') as one_txt:
                one_txt.write( myLine + "\n")
            i = i + 1


            with open(logTxt, "a", encoding='UTF-8') as log_txt:
                log_txt.write("第" + str(i) + "行，文件名称：" + txt
                              + ", size:" + str('%.1f' % (os.path.getsize(txtFile)/1024))
                              + "K ,共有：" + str(mlength) + "个词,其中重复词：" + str(repeatWord) + " \n")
            if (i % 10 == 0):
                print("正在处理第" + str(i) + "个文件，名称为：" + str(txtFile))



# 检查函数，确认不能处理的文件个数
def selectUnableToProcessPDF():
    # 需要处理的pdf目录
    pdfPath="E:\\嘟嘟资料\\科研项目\\债券pdf整理\\数据\\回函 new platform（latest0606)"
    txtPath = "E:\\嘟嘟资料\\科研项目\\new\\txt"
    myErrorPDF = "E:\\嘟嘟资料\\科研项目\\new\\errorpdf.log"
    myErrorPath = "E:\\嘟嘟资料\\科研项目\\new\\pdf_error"
    myAllPDFList = getAllFileName(pdfPath,".pdf")

    mytxtPath = getAllTxtFileName(txtPath)

    i = 0  # 失败pdf计数
    j = 0  # 对比计数
    for pdf in myAllPDFList:
        isFinish=0
        j = j + 1
        print("正在对比中，" + str(j))
        for txt in mytxtPath:
            if (os.path.splitext(txt)[0] == os.path.splitext(pdf)[0]):
                isFinish = 1
                break
        if isFinish == 0:
            i = i + 1
            with open(myErrorPDF, 'a') as f1:
                f1.write("无法处理pdf文件：" + pdf + "\n")
            shutil.copy(pdfPath + "\\" + pdf , myErrorPath)
    # 最后写一下有多少个文件要处理
    with open(myErrorPDF, 'a') as f1:
        f1.write("===================================\n")
        f1.write("===================================\n")
        f1.write("总结：合计" + str(len(myAllPDFList)) + "个文件，其中分词成功的txt文件有"
                 + str(len(myAllPDFList)-i)
                 + "个！,无法处理的文件有：" + str(i) + "个！\n")
    winsound.Beep(262, 3000)



# 获得指定目录下的txt文件名称集合
def getAllTxtFileName(file_dir):

    txt_list=[]  # 定义pdf文件列表
    # 在file_dir目录下循环，找出全部文件  walk函数包括子目录
    for files in os.walk(file_dir):
        # 通过变量调试，分析出files[2]就是文件列表,针对这个循环，判断并取出pdf文件
        for file in files[2]:
            # 判断是否是pdf文件
            if (os.path.splitext(file)[1] == '.txt') :
                # 将pdf文件加入列表
                txt_list.append(os.path.join(file))

    return txt_list
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

# 指定的txt文件转化成分词后的txt文件
def makeWordTxt(inTxt,outTxt,participleType):
    fR=open(inTxt, 'r', encoding='UTF-8') # 读取文件
    sent=fR.read()

    if participleType == "jieba":
        sent_list=jieba.cut(sent) # 使用jieba进行分词
        fW=open(outTxt, 'w', encoding='UTF-8')  # 写入文件
        fW.write(sent_list)
        fR.close()
        fW.close()
        time.sleep(0.001)
    if participleType == "pkuseg":
        seg = pkuseg.pkuseg()  # 默认配置加载模型
        sent_list = seg.cut(sent)

        fW=open(outTxt, 'w', encoding='UTF-8')  # 写入文件
        fW.write(" ".join(sent_list))
        fR.close()
        fW.close()
        time.sleep(0.001)
    if participleType == "thulac":
        thu1=thulac.thulac(seg_only=True,filt=True)  # 只进行分词，不进行词性标注
        sent_list = thu1.cut(sent, text=True)  # 对input.txt文件内容进行分词，输出到output.txt

        fW=open(outTxt, 'w', encoding='UTF-8')  # 写入文件
        fW.write(sent_list)
        fR.close()
        fW.close()
        time.sleep(0.001)
    if participleType == "smq":
        sent_list = sent

        fW=open(outTxt, 'w', encoding='UTF-8')  # 写入文件
        fW.write(sent_list)
        fR.close()
        fW.close()
        time.sleep(0.001)
    # fW=open(outTxt, 'w', encoding='UTF-8') # 写入文件
    # fW.write(sent_list)
    # fR.close()
    # fW.close()
    # time.sleep(0.001)


def getWordList(myLine):
    return myLine.split(" ")


# 生成词云基础数据格式
def makeCloudWord(topicTxt,errorCloudTxt,cloudTxt):
    # 读出需要处理的词云文件  topicTxt
    topicList=[]
    with open(topicTxt, 'r') as fR:  # 读取文件
        lines=fR.readlines()  # 读出全部行
        for line in lines:
            words=line.rstrip()
            cnWord,enWord =words.split(':', 1)
            # print(cnWord.lower())
            senWord = float('%.1f' % (float(enWord)/ 1000))
            topicList.append(cnWord + "|" + str(senWord))  #
    fR.close()
    # print(topicList)

    # 读出需要处理的词云列表，有问题的词云，主要取得是它的颜色列表
    errorCloudList = []
    with open(errorCloudTxt, 'r') as fR:  # 读取文件
        lines=fR.readlines()  # 读出全部行
        for line in lines:
            words=line.rstrip()
            cnWord=words.split('|', 4)[2]
            errorCloudList.append(cnWord)  # 获得词云色彩
    fR.close()

    # 生成云图文件
    i = 0
    with open(cloudTxt, "w", encoding='UTF-8') as f1:
        for topic in topicList:
            print(topic + " " + str(i) + "色彩数量：" + str(len(errorCloudList)))
            word = topic + "|" + errorCloudList[i] + "|1|0"
            f1.write(word + "\n")
            i = i + 1


# 把中文词翻译成英文词
def replaceCNtoEng(inTxt,outTxt,wordListTxt):
    # 先把对比的词出读出到列表中
    myList= []
    with open(wordListTxt, 'r') as fR:  # 读取文件
        lines=fR.readlines()  # 读出全部行
        for line in lines:
            words=line.rstrip()

            myList.append(words)  #
    fR.close()
    # print(myList)



    i = 0
    txtFileStringCn = ''
    txtFileStringEng=''

    txtTempString = ''
    lengW = len(myList)  # 定义字符长度
    while i < len(myList):
        cnWord, engWord=myList[i].split(':', 1)
        # print(str(i) + " " + cnWord + ":" + engWord)

        txtTempString = txtTempString + "," + cnWord


        j = 0
        while j < (lengW - i):
            txtFileStringCn = cnWord + "," + txtFileStringCn
            txtFileStringEng= engWord + "," + txtFileStringEng
            j = j + 1
        i = i + 1
        # print(txtFileStringCn)
        # print(txtFileStringEng)
    print(txtTempString)

    with open("e:\\pdf\\txtFileStringCn.txt", "w", encoding='UTF-8') as f:
        f.write(txtFileStringCn)

    with open("e:\\pdf\\txtFileStringEng.txt", "w", encoding='UTF-8') as f:
        f.write(txtFileStringEng)

    # word=WordCloud(background_color="white", \
    #                width=800, \
    #                height=600,
    #                max_words=50,  # 显示前50个词
    #                font_path='simhei.ttf',
    #                ).generate(txtFileString)
    #
    # word.to_file(pngPath)

    # 循环处理翻译成英文-=====================================
    # myi = 0
    # txtFileString = ''
    # eWord = ""
    # cWord = ""
    # with open(inTxt, 'r', encoding='UTF-8') as fR:  # 读取文件
    #     txtFileString=fR.read()
    #     while myi < len(myList):
    #
    #         cnWord,engWord = myList[myi].split(',',1)
    #         print(str(myi) + " " + cnWord + ":" + engWord)
    #         eWord = eWord + engWord + ","
    #         cWord = cWord + cnWord + ","
    #         txtFileString=txtFileString.replace(cnWord, " " + engWord + " ")
    #         myi = myi + 1
    # fR.close()
    # print(eWord)
    # print(cWord)


    # 处理后的文件写入outTxt文件中
    # with open(outTxt, "w",encoding='UTF-8') as f:
    #     f.write(txtFileString)

# 单个pdf文件，先删除公司名称，然后转化成txt文件
def deleteCompanyTxtByAll(tempTxt,companyList,oneTxt):
    # 读取文件到一个大的字符串中

    with open(tempTxt, 'r', encoding='UTF-8') as fR:  # 读取文件
        txtFileString=fR.read()
    fR.close()

    # 由于直接读取整个文件，换行符："\n"，也被保存下来了，需要替换掉，
    txtFileString=txtFileString.replace("\n", "")

    myNew=""
    myI=0
    myWord=txtFileString.split(" ")

    while myI < len(companyList):
        name=companyList[myI]

        # 先查询是否有关键词
        myCount = myWord.count(name)
        j = 1

        # 循环删除几次
        while j <=myCount:
            myWord.remove(name)  # 删除一次
            j = j + 1

        myI=myI + 1

    with open(oneTxt, "w", encoding='UTF-*') as f:
        f.write(" ".join(myWord))

# 单个pdf文件，先删除公司名称，然后转化成txt文件
def deleteCompanyTxt(tempTxt,outTxt,companyList):
    # 读取文件到一个大的字符串中

    with open(tempTxt, 'r', encoding='UTF-8') as fR:  # 读取文件
        txtFileString=fR.read()
    fR.close()



    # 由于直接读取整个文件，换行符："\n"，也被保存下来了，需要替换掉，
    # txtFileString = txtFileString.replace("\n","")

    myNew = ""
    myI = 0
    while myI < len(companyList):
        name = companyList[myI]
        number = txtFileString.count(name)
        # 替换词
        txtFileString = txtFileString.replace(name, myNew)
        print(name)
        myI = myI + 1

    # 处理删除单词后，分割变成了两个空格
    txtFileString=txtFileString.replace("  ", " ")
    txtFileString=txtFileString.replace("   ", " ")
    txtFileString=txtFileString.replace("    ", " ")

    # 处理后的文件写入tempTxt文件中
    with open(outTxt, "w", encoding='UTF-8') as f:
        f.write(txtFileString)


# 单个pdf文件转化成txt文件
def pdfToTxt(pdfFile,txtFile):
    a = 0
    # 读取PDF文档

    try:
        with pb.open(pdfFile) as pdf:
            a=len(pdf.pages)
            file_handle=open(txtFile, mode='w', encoding='utf-8')
            i=0
            for i in range(0, a):
                first_page=pdf.pages[i]
                # 导出当前页文本
                text=first_page.extract_text()
                # print(text)

                file_handle.write(text)

                if (i % 10 == 0):
                    print("共有" + str(a) + "页，当前页：", first_page.page_number)
                    print("-----------------------------------------")
    except Exception as e:
        pb.set_debug()
        print(e)
        return -1
    # except Exception as e:
    #     print(e)
    #     return -1
    # pdf.close()
    time.sleep(0.001)
    return a


# 从公司文件中生成公司列表
def getCompanyList(txtFile):

    myCompanyList = []
    oneWordList = []

    try:
        # txtFile变量定义的是stopwords.txt文件的名称及路径
        with open(txtFile, 'r', encoding='UTF-8') as f:
            lines = f.readlines()  # 读出全部行
            print(len(lines))  # 此处打印了一下行数，为：588069行
            for line in lines:
                name = line.rstrip()  # 去掉回车 "\n"
                myCompanyList.append(name)  # 把每行都加入到列表中

                # 此处代码用来测试
                # 此处代码，把一个字符为一行的加入到oneWrodList列表中
                if len(name) == 1:
                    oneWordList.append(name)
            print(len(oneWordList))  # 一个字为一行的进行了统计，打印的结果是：3545个

    except Exception as e:
        print(e)
        return -1

    # print("列表有:" + str(len(oneWordList)) + "个：明细如下")
    #     # print(oneWordList)
    # print(str(len(myCompanyList)))
    # print(myCompanyList)
    return myCompanyList

# 去掉叠词和数字的函数，专供cutAndSelectTxt调用
def selectWord(outFile,oneTxt,logTxt,txtFile,punctuation):
    # 文件大小为空的不处理


    if (os.path.getsize(outFile) > 0):
        # 把txt文件全部读出来，写成一行
        with open(outFile, 'r', encoding='UTF-8') as f:
            txtLines=f.readlines()

        myLine=""
        for line in txtLines:
            line=line.replace("\n", "")
            line=line.strip()
            line=line.lstrip()

            myLine=myLine + " " + line

        # 此处增加去掉数字，字母，符号
        myLine=getNoNuberString(myLine, punctuation)

        # 此处去掉一个词,增加了去掉重复字组成的叠词
        myLine, mlength, repeatWord=getNoOneWord(myLine)
        # print(myLine)

        with open(oneTxt, 'a', encoding='UTF-8') as one_txt:
            one_txt.write(myLine + "\n")

        with open(logTxt, "a", encoding='UTF-8') as log_txt:
            mystr = "文件名称：" + str(txtFile) + ",共有：" + str(mlength) + "个词,其中叠词：" + str(repeatWord) + " \n"
            log_txt.write(mystr)
        print(mystr)

# 去掉非词
def getTrueWordFromTxt(outTxt,trueWordTxt):

    # companyList=getCompanyList(noWordTxt)
    # companyList = ['公司','万元', '集团','发行人']

    companyList=['有限','分别','单位','如下','子',
                 '其中','进一步','年末','三年','公司','万元','集团','发行人']
    # 删掉指定字典的词
    deleteCompanyTxt(trueWordTxt,outTxt, companyList)


# 切词，选词，，去掉叠词，汇总成一个大文件
def cutAndSelectTxt(punctuation):

    pdfPath = "e:\\pdf\\"
    # 由pdf转化而来，但未经处理的txt保存的目录
    txtPath='e:\\pdf\\allTxt\\'
    # 备份pdf文件目录，处理完成的pdf文件，需要删掉，同时在\bak目录下保存一份
    pdfBakPath="e:\\pdf\\pdfbak\\"

    # 公司文件路径,在文件中去掉这些词
    companyTxtFile="E:\\pdf\\companytxt\\stopwords.txt"

    oneTxt = "e:\\pdf\\cutAndMakeOneTxtByThulac.txt"

    # 定义总开始时间,便于计算本次导入花费的总时间
    begin_localtime=datetime.now()

    # 准备工作，pdf备份的目录是否存在，不在则新建
    if not os.path.exists(pdfBakPath):
        os.makedirs(pdfBakPath)

    # 初始化公司名称列表
    companyList=[]
    companyList=getCompanyList(companyTxtFile)
    print(len(companyList))

    # 第一步，获得指定目录下txt文件名称的列表
    PdfList=getAllFileName(txtPath, ".txt")

    # 第二步，创建目录，保存本次处理完成的分词txt文件，文件目录根据日期时间来生成
    mydate=str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))


    i=0  # 统计当前处理的文件个数
    totalNumber=len(PdfList)  # 获得本次需要处理的文件个数
    begin_time=datetime.now()  # 本次开始处理的时间

    tempFile=pdfPath + "temp.txt"
    outFile=pdfPath + "outTxt.txt"
    logTxt="E:\\pdf\\oneTxtNoDigitNoWordNoRepeat_logTxt.txt"
    # 对文件列表进行循环，开始处理数据
    for filename in PdfList:

        print("正在处理的txt文件名称为：《" + str(filename) + "》，请稍后")
        # 先对txt文件处理，把公司名称字符串从文件中删掉
        txtFile = txtPath + filename


        # 首先删除，然后拷贝文件同时更名为temp.txt
        if os.path.exists(tempFile):
            os.remove(tempFile)
        shutil.copy(txtFile, tempFile)

        # thulac 由清华大学自然语言处理与社会人文计算实验室研制推出的一套中文词法分析工具包
        # jieba 被称为python最好用的
        # pkuseg 北京大学语言计算与机器学习研究组发布的
        # smq  不做任何切割

        # 删除指定的词
        deleteCompanyTxtByAll(tempFile, companyList, outFile)

        # 切词
        makeWordTxt(outFile, outFile,"pkuseg")

        # 最后去掉叠词和数字，字母，输出到一个文件中
        selectWord(outFile,oneTxt,logTxt,filename,punctuation)



        # # 删掉指定字典的词
        # deleteCompanyTxt(outFile, companyList)



        # 最后去掉叠词和数字，字母，输出到一个文件中
        # selectWord(outFile, oneTxt, logTxt, filename, punctuation)
        # ======================================================

        # 获得当前时间,计算本次处理文件的时间
        end_time=datetime.now()

        i=i + 1
        desc="共有" + str(totalNumber) + "个文件，已完成" \
             + str(i) + "个，剩余：" + str(totalNumber - i) \
             + "个。本次开始时间：" + str(begin_localtime) \
             + "当前：《" + filename + "》"
        print(desc)

    # 打印一下时间，看看用了多久
    desc=str(mydate) + "本次文件全部处理完成！具体时间为："

    end_localtime=datetime.now()

    print(str(begin_localtime))
    print(str(end_localtime))


def processingPDF():
        # 需要处理的pdf目录
        pdfPath="E:\\pdf\\回函 new platform（latest0606)\\"
        # 输出txt文件的目录，以后每次启动程序，分词后的txt都保存在这个总目录下
        txtPath='e:\\pdf\\txt\\'
        # 备份pdf文件目录，处理完成的pdf文件，需要删掉，同时在\bak目录下保存一份
        pdfBakPath="e:\\pdf\\pdfbak\\"

        pdfErrorPath="e:\\pdf\\error\\"

        # 公司文件路径,在文件中去掉这些词
        companyTxtFile = "E:\\pdf\\companytxt\\stopwords.txt"

        # 定义总开始时间,便于计算本次导入花费的总时间
        begin_localtime=datetime.now()

        # 准备工作，pdf备份的目录是否存在，不在则新建
        if not os.path.exists(pdfBakPath):
            os.makedirs(pdfBakPath)

        # 初始化公司名称列表
        companyList = []
        companyList = getCompanyList(companyTxtFile)
        print(len(companyList))

        # 第一步，获得指定目录下pdf文件名称的列表
        PdfList=getAllFileName(pdfPath, ".pdf")

        # 第二步，创建目录，保存本次处理完成的分词txt文件，文件目录根据日期时间来生成
        mydate=str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))
        # 根据日期时间字符串，拼出需要的目录名称
        create_path=txtPath + mydate + "\\"
        # 判断本次生成的目录是否存在，不存在就新建一个
        isExists=os.path.exists(create_path)
        if not isExists:
            os.makedirs(create_path)

        # 第三步，目录已经成功建立，开始本次文件处理
        if os.path.exists(create_path):
            i=0  # 统计当前处理的文件个数
            totalNumber=len(PdfList)  # 获得本次需要处理的文件个数
            begin_time=datetime.now()  # 本次开始处理的时间

            # 对文件列表进行循环，开始处理数据
            for filename in PdfList:

                print("正在处理的pdf文件名称为：《" + str(filename) + "》，请稍后")

                # 需要处理的pdf文件，文件名称加上目录，完整的pdf文件路径加名称
                mypdfFile=pdfPath + filename
                # 定义备份pdf的文件
                mypdfFileBak=pdfBakPath + filename
                # 定义一个临时文件，用来临时保存pdf转化成txt，但没有分词
                tempFile=pdfPath + "temp.txt"
                # 定义需要输出的处理的好的分词txt的文件名称，此处需要处理filename变量中保存的文件名称，要把.pdf修改成.txt
                outFile=create_path + os.path.splitext(filename)[0] + ".txt"

                if os.path.exists(mypdfFile):
                    # pdf文件转化成txt文件，同时返回文件页数
                    myPageNumber=pdfToTxt(mypdfFile, outFile)  #
                    # myPageNumber=pdfToTxt(mypdfFile, tempFile)

                    if (myPageNumber == -1):
                        myErrorPDF=pdfErrorPath + "error.log"
                        print("无法处理页数问题，已写入日志！" + myErrorPDF)
                        with open(myErrorPDF, 'a') as f1:
                            f1.write("无法处理页数问题：" + filename + ", 请手工处理！\n")
                        winsound.Beep(262, 2000)
                    else:
                        # 以下内容注释掉，先生成txt文件====================

                        # 先对txt文件处理，把公司名称字符串从文件中删掉
                        # deleteCompanyTxt(tempFile,companyList)

                        # 把txt文件进行分词，并按照要求保存到生成的目录下

                        # thulac 由清华大学自然语言处理与社会人文计算实验室研制推出的一套中文词法分析工具包
                        # jieba 被称为python最好用的
                        # pkuseg 北京大学语言计算与机器学习研究组发布的
                        # smq  不做任何切割
                        # makeWordTxt(tempFile, outFile,"smq")

                        # 生成txt文件========================================

                        # 获得当前时间,计算本次处理文件的时间
                        end_time=datetime.now()

                        i=i + 1
                        desc="共有" + str(totalNumber) + "个文件，已完成" \
                             + str(i) + "个，剩余：" + str(totalNumber - i) \
                             + "个。本次开始时间：" + str(begin_localtime) \
                             + "当前：《" + filename + "》"
                        print(desc)

                    # 无论是否正确处pdf，都删除，有错误写日志文件中
                    os.remove(mypdfFile)

                    # # 写错误日志，保存在e盘下面根目录
                    # desc="pdf转化错误！" + mypdfFile + ",发生时间：" + str(datetime.now()) + "\n"
                    # with open("e:\\processingPDF.log", 'a') as file_object:
                    #     file_object.write(desc)
                    # print(desc)
        else:
            print("指定目录不存在！")

            # 打印一下时间，看看用了多久
        desc=str(mydate) + "本次文件全部处理完成！具体时间为："

        end_localtime=datetime.now()

        print(str(begin_localtime))
        print(str(end_localtime))


def deleteFinishTxt():
    with open("e:\\pdf\\oneTxtNoDigitNoWordNoRepeat_logTxt.txt", 'r', encoding='UTF-8') as f:
        txtLines = f.readlines()

        m=0
        # 对每一行进行循环
        for line in txtLines:
            k = 0
            i=0
            j=0

            while k <= len(line):

                x=line[k:k + 1]
                if x == "：":
                    i = k
                if x == ",":
                    j = k
                    txtFile = line[i+1:j]
                    m = m + 1

                    mypdfFile = "E:\\pdf\\allTxt\\" + txtFile
                    if os.path.exists(mypdfFile):
                        os.remove(mypdfFile)
                        print(str(m) + ":" + txtFile)
                    break
                k = k + 1
        print("wancheng")

if __name__ == '__main__':
    # 定义特殊符号字典，用来过滤删除这些特殊字符
    # punctuation="""″！）”“：（⒑⒓⒔⒖⒗⒘⒙㈧σακ♭ヒγΥΓω￠δΝΣηε∞ˇ±⌒⒄※ψ扌艹卩れ灬犭ス阝ネリギもキたふなドォヨを宀钅夂饣″冖丨刂忄礻氵△●¤・Ξ∴★【ˉ〓▲△巛灬？｡。,．.�→◆冫＂＃＄％＆＇（）＊＋－〈／：:；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    # # # 对txt文件处理，包括切割，去掉关键词，去掉特殊符号，最终生成一个txt文件
    # cutAndSelectTxt(punctuation)


    # 去掉非词
    # outTxt = "E:\\pdf\\getTrueWordFromTxt\\cutAndMakeOneTxtByThulac-3.txt"
    # trueWordTxt = "E:\\pdf\\getTrueWordFromTxt\\cutAndMakeOneTxtByThulac.txt"
    # getTrueWordFromTxt(outTxt,trueWordTxt)


    # 测试删除各种符号的函数
    # txt = "34343,.。。。zhongguo 中国"
    # getNoNuberString(txt)

    # 处理pdf文件，转换成txt
    # processingPDF()

    # 挑出没有处理的pdf，这些pdf都是不能正确打开的，存在一定问题的文件
    # selectUnableToProcessPDF()

    # 生成一个txt文件，去掉一个词和标点符号，叠词，数字等
    # makeOneTxt()


    # # 打印一共多少行
    # with open("e:\\pdf\\oneTxtNoDigitNoWord.txt", 'r', encoding='UTF-8') as f:
    #     txtLines = f.readlines()
    # print(len(txtLines))

    # # 测试函数  ,从stopwords.txt文件中读取公司列表，目前有588069个行
    # companyTxtFile="E:\\pdf\\companyTxt\\stopwords.txt"
    # getCompanyList(companyTxtFile)


    # top50中文词云
    # txtPath = "e:\\pdf\\test.txt"
    # pngPath = "e:\\pdf\\top50_cn.png"
    # outPath = "e:\\pdf\\top50_cn.txt"
    # getWordCount(txtPath, outPath,51)  # 统计词的频率，前50个
    # getWrodColud(txtPath,pngPath, 51)  # 绘制图云,前50个

    # # 生成英文top50词库文件，用来生成英文词云
    # inTxt="e:\\pdf\\test.txt"
    # txtPath = "e:\\pdf\\test_50Eng.txt"
    # wordListTxt="e:\\pdf\\top50_cn_english.txt"
    # replaceCNtoEng(inTxt,txtPath,wordListTxt)

    topicTxt = "E:\\pdf\\top50图形\\top100-english\\top100-5.txt"
    errorCloudTxt="E:\\pdf\\top50图形\\top100-english\\color.txt"
    cloudTxt = "E:\\pdf\\top50图形\\top100-english\\txtFileStringCn.txt"
    makeCloudWord(topicTxt,errorCloudTxt,cloudTxt)

    # # top50英文词云
    # txtPath = "e:\\pdf\\test_50Eng.txt"
    # pngPath = "e:\\pdf\\top50_Eng.png"
    # outPath = "e:\\pdf\\top50_Eng.txt"
    # getWordCount(txtPath, outPath,51)  # 统计词的频率，前50个
    # getWrodColud(txtPath,pngPath, 51)  # 绘制图云,前50个
