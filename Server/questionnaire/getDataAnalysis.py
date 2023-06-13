import base64
import copy
import os.path

from io import BytesIO

from questionnaire.models import QuestionnaireRecords
from utils.custom import Response
from rest_framework.views import APIView
from Server.settings import formatResponseData, BASE_DIR


class GetDataAnalysisView(APIView):
    # 局部(本视图有效)认证类
    authentication_classes = []
    # 局部(本视图有效)权限类
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        获取问卷分析结果
        """
        data = copy.deepcopy(formatResponseData)
        try:
            problemList = request.data.get("problemList")

            # 异常拦截
            if not problemList:
                return Response(data=data, responseMsg="请求参数缺失", loggerMsg="请求参数缺失", isError=True)

            numberAndAnswerListDict = {number: [] for number in range(1, len(problemList) + 1)}
            questionnaireRecordList = QuestionnaireRecords.objects.all()
            for questionnaireRecord in questionnaireRecordList:
                questionnaireRecord = eval(questionnaireRecord.problemList)
                for problem in questionnaireRecord:
                    if not problem["answer"]:
                        problem["answer"] = ""
                    numberAndAnswerListDict[problem["number"]].append(problem["answer"])

            for number, answerList in numberAndAnswerListDict.items():
                # 饼图
                if number <= 8:
                    labelAndSizeDict = {}
                    for answer in answerList:
                        if answer not in labelAndSizeDict:
                            labelAndSizeDict[answer] = 1
                        else:
                            labelAndSizeDict[answer] += 1

                    labelSortedList = sorted(labelAndSizeDict, key=lambda label: labelAndSizeDict[label])
                    if len(labelSortedList) > 4:
                        labelSortedList = labelSortedList[::-1][:4]
                        labelAndSizeDict = {label: size for label, size in labelAndSizeDict.items() if
                                            label in labelSortedList}

                    problemList[number - 1]["answer"] = getPie(labelAndSizeDict.keys(), labelAndSizeDict.values())

                # 词云图
                else:
                    problemList[number - 1]["answer"] = getWordCloud("。".join(answerList))
            # 响应
            data["data"]["problemList"] = problemList
            return Response(data=data, loggerMsg=f"获取问卷分析结果：成功")

        except Exception as e:
            return Response(data=data, responseMsg="ServerError",
                            loggerMsg=f"请求处理失败: {e}", isError=True)


def getPie(labelList, sizeList):
    """
    饼图
    """
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib import rcParams
    font_path = os.path.join(BASE_DIR, "static", "msyh.ttc")
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    # 字体设置
    rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体
    rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
    rcParams['axes.unicode_minus'] = False  # 使坐标轴刻度标签正常显示正负号

    # 数据
    sizes = sizeList

    # 饼图的标签
    labels = labelList

    # 饼图的颜色
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral'][:len(labelList)]

    # 绘制饼图
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    # 返回图形
    return getPltImageSrc(plt)


def getWordCloud(text):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt  # 绘制图像的模块
    import jieba  # jieba分词

    # 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(text))

    wordcloud = WordCloud(
        # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
        font_path=os.path.join(BASE_DIR, "static", "msyh.ttc"),
        # 设置了背景，宽高
        background_color="white", width=1000, height=880).generate(cut_text)

    plt.imshow(wordcloud)
    plt.axis("off")
    return getPltImageSrc(plt)


def getPltImageSrc(plt):
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    imgBase64 = base64.b64encode(img.getvalue()).decode('utf8')
    return "data:image/png;base64,{}".format(imgBase64)
