from FlaskDemo.model import SparkApi

# 以下密钥信息从控制台获取
appid = "12ddc6cd"  # 填写控制台中获取的 APPID 信息
api_secret = "ODc2YmNhYmE4Y2M2NzQ4MzZmYzYxM2E3"  # 填写控制台中获取的 APISecret 信息
api_key = "dd83233f1bb94964b2d572cc1140deb5"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
domain = "generalv3"  # v1.5版本
# domain = "generalv2"    # v2.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text = []


# length = 0

def getText(role, content):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text


def getLocalText(role, content, text):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text


def myQuestion(text, headers):
    myText = []
    Input = text
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    # print("星火:", end="")
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question, header=headers)
    ans = getText("assistant", SparkApi.answer)
    if type(SparkApi.answerDict[headers["UserId"]]) == "string":
        resp = SparkApi.answerDict[headers["UserId"]]
    else:
        resp = SparkApi.answerDict[headers["UserId"]][len(SparkApi.answerDict[headers["UserId"]]) - 1]
    # ans2 = getText("assistant", SparkApi.answerDict[headers["UserId"]])
    myTextFinal = getLocalText("assistant", resp, myText)
    print(SparkApi.answerDict)
    finallyAnswer = ans[len(ans) - 1]["content"]
    # print(text)
    # print(ans[len(ans)-1]["content"])
    return myTextFinal[0]["content"]


if __name__ == '__main__':
    text.clear()
    # while 1:
    #     Input = input("\n" + "我:")
    #     question = checklen(getText("user", Input))
    #     SparkApi.answer = ""
    #     print("星火:", end="")
    #     SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    #     getText("assistant", SparkApi.answer)
    #     # print(str(text))
    res = myQuestion("你好", {
        "UserId": "114514",
        "Content": "",
        "Authorization": "Bearer your_token",
        "Content-Type": "application/json"
    })
    # print(res)
