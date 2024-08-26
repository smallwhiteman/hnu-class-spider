import time


import requests

from function import *


print("本程序仅供个人学习,请在下载后的24小时内删除！")
print('用户滥用造成的一切后果与作者无关！')
print('使用者请务必遵守当地法律！')
print('本程序不得用于商业用途，仅限学习交流,否则由此产生的一切后果与作者无关')
print("-------------------------------------------------------")
print("welcome to hnu-class-spider v1.0.0")
print("课程库更新时间:2024-6-   ")
print("作者:湖大双发豌豆(你也可以叫我豌豆大帝)")
print("-------------------------------------------------------")
"""token = input("请输入token:")
cookieData = input("请输入coookie:")"""
with open(os.path.join(base_dir, "config.txt"), 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        token, cookieData = line.strip().split('|', 1)
print(token)
print(cookieData)
"""token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2MiOiIyMDIzMDgwMTAzMTIiLCJleHAiOjE3MTgyOTU3MzUsInNpZCI6IjgxYTE3NTBiLTlkMTYtNDQyMC05ZmVkLWRmM2Q4MmFiN2Q3MSJ9.P8RmiBHe969ySzAoudHSuh8BDUH3_LD6d8jOw2EhU2g"
cookieData = "authcode=202308010312;casLogin=1;SESSION=81a1750b-9d16-4420-9fed-df3d82ab7d71;token="""""
headersStrData = f"""
   POST /resService/jwxtpt/v1/xsd/stuCourseCenterController/saveStuXk?resourceCode=XSMH0303&apiCode=jw.xsd.courseCenter.controller.StuCourseCenterController.saveStuXk&sf_request_type=ajax HTTP/1.1
Host: hdjw.hnu.edu.cn
Connection: keep-alive
Content-Length: 1027
userRoleCode: student
locale: zh_CN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0
Simulated-By: 
Content-Type: application/json
Accept: application/json, text/plain, */*
X-Requested-With: XMLHttpRequest
userAgent: 
app: PCWEB
TOKEN: {token}
Origin: http://hdjw.hnu.edu.cn
Referer: http://hdjw.hnu.edu.cn/Njw2017/student/student-choice-center/student-select-course.html
Accept-Encoding: gzip, deflate
Accept-Language: en,ja;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5
Cookie: {cookieData}
"""
check_headersStrData = f"""
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
App: PCWEB
Connection: keep-alive
Content-Length: 2
Content-Type: application/json
Cookie: {cookieData}
Host: hdjw.hnu.edu.cn
Locale: zh_CN
Origin: http://hdjw.hnu.edu.cn
Referer: http://hdjw.hnu.edu.cn/Njw2017/index.html
Simulated-By:
Token: {token}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
Useragent:
Userrolecode: student
X-Requested-With: XMLHttpRequest
"""

"""if checkcookieislegal(cookieData,check_headersStrData) == 200:
    print("cookie登录成功,状态码200")"""



# 获取用户输入的老师名字列表
teachers_input = input("请输入要抢的老师名字(中间用英文逗号隔开,如 王强,李四): ")
teachers = [teacher.strip() for teacher in teachers_input.split(',')]

# 读取class_id文件

class_ids = []
with open(os.path.join(base_dir, "class_id.txt"), 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split(',')
        course_id = parts[0].strip()
        teacher_names = [name.strip() for name in parts[1:]]  # 剩余部分是老师的名字列表
        class_ids.append((course_id, teacher_names))

# 匹配老师并输出对应的课程ID
matched_ids = []
result = {}
for teacher in teachers:
    result[teacher] = []
    for course_id, teacher_names in class_ids:
        if teacher in teacher_names:
            result[teacher].append(course_id)
            matched_ids.append(course_id)  # 添加到匹配列表中

# 输出结果
for teacher, courses in result.items():
    if courses:
        print(f"{teacher} : {', '.join(courses)}")
    else:
        print(f"{teacher} 没有找到对应的课程ID")

# 输出匹配到的课程ID列表
if(matched_ids == []):
    print("-------------------------------------------------------")
    print("退出程序,错误原因:没有找到匹配课程ID")
    exit(0)
else:
    print("-------------------------------------------------------")
    print("匹配完成,当前任务池:", matched_ids)



with open(os.path.join(base_dir,"match.json"), 'w', encoding='utf-8') as match_file:
    match_file.write('')

# 读取template.json文件
with open(os.path.join(base_dir,"template.json"), 'r', encoding='utf-8') as template_file:
    template_data = json.load(template_file)



# 初始化一个空列表，用于存储替换后的数据
match_data = []

# 遍历matched_ids，将template.json中的id值替换
for match_id in matched_ids:
    for item in template_data:
        new_data = item.copy()  # 创建item的副本
        new_data['id'] = match_id  # 替换id值
        match_data.append(new_data)  # 将替换后的数据添加到match_data中

# 将match_data写入match.json文件
with open(os.path.join(base_dir,"match.json"), 'w', encoding='utf-8') as match_file:
    json.dump(match_data, match_file, ensure_ascii=False, indent=4)

print("操作完成，match.json文件已生成。")

# 读取 class.json 文件的内容
with open(os.path.join(base_dir,"match.json"), 'r', encoding='utf-8') as file:
    json_data_list = json.load(file)

total = len(json_data_list)

while True:
    model = input("请输入阿拉伯数字:1.定点秒抢模式2.循环捡漏模式")
    if model == '1':
        break
    elif model == '2':
        break
    else:
        print("输入不是1或2，请重新输入")


if model == '1':
    print("开启定点秒抢模式,请在准点按ENTER键,默认每2s发送一次请求")
    input("按下ENTER键立即开始运行!")
    while (1):
        json_data_list = chooseClass(cookieData, headersStrData, json_data_list)
        if(json_data_list == []):
            print("程序退出,原因:全部课程均已抢到")
            exit(0)
        print(f"抢课进度:\033[34m{total - len(json_data_list)}/{total}\033[0m")
        time.sleep(2)
else:
    print("开启循环捡漏模式,捡漏模式将在1s后开始运行,默认每2s发送一次请求")
    time.sleep(1)
    while (1):
        json_data_list = chooseClass(cookieData, headersStrData,json_data_list)
        if(json_data_list == []):
            print("程序退出,原因:全部课程均已抢到")
            exit(0)
        print(f"抢课进度:\033[34m{total - len(json_data_list)}/{total}\033[0m")
        time.sleep(0.5)


