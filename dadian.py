import os
import re
import json

f = open("./145224.txt", 'r', encoding='utf-8', errors='ignore')
lines = f.readlines()
flines = len(lines)
content = []

# regex = re.compile(r'\[requestbody\s*is\s*(.*?)\]'))
# regex = re.compile(r'行为路径打点\-{3}(.*?)\]')
regex = re.compile(r'requestBody is\s*(.*?)\]')


# 逐行匹配数据.
for i in range(flines):
    if "savelogs" not in lines[i]:
        continue
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

