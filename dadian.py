import os
import re
import json

f = open("./log/2020-12-17-13-39-34.log", 'r', encoding='utf-8', errors='ignore')
lines = f.readlines()
flines = len(lines)
content = []

'''
表达式 .* 的意思很好理解，就是单个字符匹配任意次，即贪婪匹配。
表达式 .*? 是满足条件的情况只匹配一次，即懒惰匹配
'''

# regex = re.compile(r'\[requestbody\s*is\s*(.*?)\]'))
text = r"行为路径打点\-{3}(.*?)\]"
regex = re.compile(text)
# regex = re.compile(r'requestBody is\s*(.*?)\]')


# 逐行匹配数据.
for i in range(flines):
    # if "savelogs" not in lines[i]:
    #     continue
    match = regex.search(lines[i])
    if match is not None:
        print('----------------------')
        # print(match.group(1))
        # print(json.loads(match.group(1)))
        # print(type(json.loads(match.group(1))))
        a = json.loads(match.group(1))
        print(json.dumps(a,sort_keys=True,indent=4,ensure_ascii=False))
        # content.append(match.group(1))
# print(content)
# for item in content:
#     print(json.dumps(item, indent=2))

