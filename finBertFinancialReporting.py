
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import re,time,json
# tested in transformers==4.12.4
import transformers
# transformers.__version__


# SentimentAnalysis:
# ["label": "Neutral", "score": 0.9968947172164917]
# ESG_Classification:
# ["label": "None", "score": 0.9722527265548706]
# FLS_Classification:
# ["label": "Not FLS", "score": 0.9639619588851929]


# 情感分类
def SentimentAnalysis(txtlist):
    finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

    nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)
    results = nlp(txtlist)

    print(results)
    return results

# ESG评级关注的主要是公司自身在环境、社会和治理层面所面临的潜在风险，
# 而不一定是公司自身的业务和行为对于人类和地球造成的正面或负面影响。
def ESG_Classification(txtlist):
    finbert=BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-esg', num_labels=4)
    tokenizer=BertTokenizer.from_pretrained('yiyanghkust/finbert-esg')

    nlp=pipeline("text-classification", model=finbert, tokenizer=tokenizer)
    results=nlp(txtlist)

    print(results)
    return  results

# 前瞻性声明（FLS）
def FLS_Classification(txtlist):
    finbert=BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-fls', num_labels=3)
    tokenizer=BertTokenizer.from_pretrained('yiyanghkust/finbert-fls')

    nlp=pipeline("text-classification", model=finbert, tokenizer=tokenizer)
    results=nlp(txtlist)

    print(results)
    return results

if __name__ == '__main__':

    # 测试最大能够读取的字符长度
    maxLength = 240  # 400

    article_1 = "E:\\嘟嘟资料\\FinBERT\\20221109_stock\\Lululemon_Athletica_2021.txt"
    article_1 = "E:\\嘟嘟资料\\FinBERT\\20221109_stock\\lululemon_athletica_inc.txt"

    outTxt_1 = "E:\\嘟嘟资料\\FinBERT\\20221109_stock\\lululemon_athletica_inc_FinBERT.txt"

    str_1 = ''

    # 概述
    with open(outTxt_1, 'a') as f1:
        jsonData_stock = "文件名称：lululemon_athletica_inc.txt,按照" + str(maxLength) \
                         + "个单词划分为每小段，分别计算FinBERT Sentiment、FinBERT ESG、FinBERT Forward-looking："
        f1.write(jsonData_stock + "\n")
        f1.write("FinBERT Sentiment，Output: Positive, Neutral or Negative\n")
        f1.write("FinBERT ESG,       Output:Environmental, Social, Governance or None\n")
        f1.write("FinBERT Sentiment, Output:Specific-FLS , Non-specific FLS, or Not-FLS\n")
        f1.write("===============================================\n")


    with open(article_1, 'r', encoding='UTF-8') as f:

        txtLines=f.readlines()
        myLine=""
        # 读取文章，同时把空格去掉
        for line in txtLines:
            line=line.replace("\n", " ")
            line=line.strip()
            line=line.lstrip()

            myLine=myLine + " " + line
            # if len(myLine) >= getMaxLength:
            #     break

    # 按照.分拆句子
    result_list=re.split(r'[.]', myLine)

    # 循环拆分后的句子，分成512个词一组进行计算结果
    myCount = 0  # 统计计算了多少次
    thisSentenceLen=0  # 单词计数器，每次的语句要小于512才行
    sentenceContext = ""  # 切割的小文章，每篇小文章要小于512个词

    print("小文章，单词数量小于" + str(maxLength) + "个,用时如下：")
    localtime=time.localtime(time.time())
    thisBeginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    print(thisBeginTime)

    txtlist=[]
    for mySentence in result_list:
        # 对句子进行拆分单词
        arr=mySentence.split()
        # 判断多少个词
        senteceLength = len(arr)
        thisSentenceLen = senteceLength + thisSentenceLen
        # 如果当前小文章长度加上本次句子的长度大于512个，则不在相加
        if thisSentenceLen <= maxLength:
            # 把每句话连起来
            mySentence = mySentence + "."
            sentenceContext = sentenceContext + " " + mySentence
        else:
            txtlist.append(sentenceContext)

            # 计算时间

            temp1 = ""
            temp2=""
            temp3=""

            temp1 = SentimentAnalysis(txtlist)

            temp2 = ESG_Classification(txtlist)

            temp3 = FLS_Classification(txtlist)

            myCount = myCount + 1
            # 追加的形式打开


            with open(outTxt_1, 'a') as f1:
                f1.write("" + str(myCount) + "---\n")
                jsonData_stock1=json.dumps(temp1[0], ensure_ascii=False)
                jsonData_stock2=json.dumps(temp2[0], ensure_ascii=False)
                jsonData_stock3=json.dumps(temp3[0], ensure_ascii=False)
                # 去除首尾的中括号
                jsonData_stock= "  SentimentAnalysis:[" + jsonData_stock1[1:len(jsonData_stock1) - 1]
                f1.write(jsonData_stock + "\n")

                jsonData_stock=" ESG_Classification:[" + jsonData_stock2[1:len(jsonData_stock2) - 1]
                f1.write(jsonData_stock + "\n")

                jsonData_stock=" FLS_Classification:[" + jsonData_stock3[1:len(jsonData_stock3) - 1]
                f1.write(jsonData_stock + "\n")
            txtlist=[]

            # 初始化，继续生成下一个小文章
            sentenceContext = ""  # 内容为空
            thisSentenceLen = 0  # 长度为空


    # 最后一个小文章
    if thisSentenceLen > 0 :
        txtlist.append(sentenceContext)
        myCount=myCount + 1

    if len(txtlist) > 0 :
        SentimentAnalysis(txtlist)

    localtime=time.localtime(time.time())
    thisBeginTime=str(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    print("结束时间：" + thisBeginTime)

    # str_1 = myLine
    #
    # print(str_1)
    # print('str_1:' + str(len(str_1)))
    #
    # with open(article_2, 'r', encoding='UTF-8') as f:
    #     txtLines=f.readlines()
    #     myLine=""
    #     for line in txtLines:
    #         # line=line.replace("\n", "")
    #         line=line.strip()
    #         line=line.lstrip()
    #
    #         myLine=myLine + " " + line
    #
    #         # if len(myLine) >= getMaxLength:
    #         #     break
    # str_2=myLine
    # print('str_2:' + str(len(str_2)))
    # # print(str_2)
    # #
    #
    #
    #
    # txtlist = []
    # txtlist.append(str_1)
    # # txtlist.append(str_2)
    #
    # print(len(txtlist))
    #
    # SentimentAnalysis(txtlist)

    # ESG_Classification(txtlist)
    # #
    # FLS_Classification(txtlist)
