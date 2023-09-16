import requests
import json
import hashlib
import time

input = {
    "input": "知乎，是一个中文互联网高质量问答社区和创作者聚集的原创内容平台，于2011年1月正式上线，以“让人们更好地分享知识、经验和见解，找到自己的解答”为品牌使命。知乎凭借认真、专业、友善的社区氛围、独特的产品机制以及结构化和易获得的优质内容，聚集了中文互联网科技、商业、影视、时尚、文化领域最具创造力的人群，已成为综合性、全品类、在诸多领域具有关键影响力的知识分享社区和创作者聚集的原创内容平台，建立起了以社区驱动的内容变现商业模式。 [1]知乎，2017年11月8日入选时代影响力·中国商业案例TOP30。 [2] 2019年10月21日，胡润研究院发布《2019胡润全球独角兽榜》，知乎排名第138位。 [3] 6月6日原有的“知识市场”业务升级为“知乎大学”。 [4] 7月，知乎完成新一轮融资，融资额接近3亿美元。 [5] 2019年8月12日，知乎宣布完成F轮融资，总额4.34亿美元。 [6]截至2020年12月，知乎上的总问题数超过4400万条，总回答数超过2.4亿条。在付费内容领域，知乎月活跃付费用户数已超过250万，总内容数超过300万，年访问人次超过30亿。 [7]知乎以问答业务为基础，经过近十年的发展，已经承载为综合性内容平台，覆盖“问答”社区、全新会员服务体系“盐选会员”、机构号、热榜等一系列产品和服务，并建立了包括图文、音频、视频在内的多元媒介形式。 [8]2022年4月22日，知乎在港交所实现双重上市 [45] 。",
    "prompt": "问答",
    "question": "知乎在世界上的影响力怎么样",
    "<ans>":"",
}

input2 = {
    "prompt": "问答",
    "question":"根据以下主题[计算机视觉] \n判断以下句子[自然语言处理]是不是和以上主题存在关联\nA:以上句子和以上主题讲述的话题存在关联\nB:以上句子和以上主题讲述的话题不存在任何关联\n\n请只回答选项 (A或者B)",
    "<ans>": ""
}

input3 = {
    "prompt": "问答",
    "question":"根据以下材料[1. 金陵饭店 - 以其正宗的南京菜而闻名。他们的招牌菜包括鸭血粉丝汤、盐水鸭等。] \n判断以上材料是否和以下句子矛盾[不能直接包括餐馆的招牌菜]\nA:以上材料满足以上句子的要求\nB:以上材料完全和以上句子矛盾\n\请只回答选项 (A或者B)",
    "<ans>":""
}

input4 = {'prompt': '问答', 'question': '以下材料定义了学术诚信[1. 学生不得询问课程作业的答案、不得询问考试的答案] \n请更具以上材料，判断学生的问题是否违反了学术诚信[请问教授第三张PPT讲的Java的语法是什么意思]\nA:学生的问题更接近以上材料中的学术诚信\nB:学生的问题不接近以上材料中的学术诚信\n\\请只回答选项 (A或者B)', 
          '<ans>': ''}

endpoint_name = "cpm-bee-230915034844EVUY"
ak = "21580531531411eeb4eb0242ac120004"
sk = "naj4HJrZZe7V5pKL4g#x#AJ-QEzOTOxO"
host = "saas-1222385307.us-west-2.elb.amazonaws.com"

timestemp = str(int(time.time()))
hl = hashlib.md5()
hl.update(f"{timestemp}{sk}".encode(encoding='utf-8'))
sign = hl.hexdigest()

url = f"http://{host}/inference"

payload = {
   "endpoint_name": endpoint_name,
   "input": json.dumps(input4),
   "ak": ak,
   "timestamp": timestemp,
   "sign": sign
}

response = requests.post(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
if response.status_code != 200:
    print(response.reason, response.text)
else:
    obj_json = response.json()
    if obj_json['code'] != 0:
        print(obj_json)
    else:
        data_str = obj_json['data']['data']
        data_obj = json.loads(data_str)
        print(data_obj)