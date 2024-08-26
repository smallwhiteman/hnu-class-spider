import requests
import json
import os
import sys
base_dir =os.path.dirname(os.path.realpath(sys.argv[0]))
def convert_cookie_string_to_dict(cookie_str):#将ccokie转化为字典格式
    cookies = {}
    for item in cookie_str.split(';'):
        key, value = item.strip().split('=', 1)
        cookies[key] = value
    return cookies

def parseHeader(strData):#将header转化为字典格式
    header = {}
    for i in strData.split("\n"):
        if len(i.split(":")) == 2:
            key = i.split(":")[0].replace(" ", "")
            value = i.split(":")[1].replace(" ", "")
            header[key] = value
    return header

def checkcookieislegal(cookies,headers):#检查cookie token是否失效
    url = "http://hdjw.hnu.edu.cn/Njw2017/index.html#/student/student-course-list/"
    res = requests.get(url,cookies=convert_cookie_string_to_dict(cookies),headers=parseHeader(headers))
    return res.status_code

def chooseClass(cookies, headers,json_data_list):
    remain_list = []

    # 定义目标 URL
    url = 'http://hdjw.hnu.edu.cn/resService/jwxtpt/v1/xsd/stuCourseCenterController/saveStuXk?resourceCode=XSMH0303&apiCode=jw.xsd.courseCenter.controller.StuCourseCenterController.saveStuXk'

    # 发送多个 POST 请求并带上 JSON 数据
    for json_data in json_data_list:
        response = requests.post(
            url,
            cookies=convert_cookie_string_to_dict(cookies),
            headers=parseHeader(headers),
            json=json_data
        )
        # 打印响应状态码和响应内容
        print(response.status_code)
        response_data = response.json()
        print(response_data)
        text = response_data.get("errorCode")
        if  text == "success":
            print("\033[32m抢课成功!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m")
            print(f"\033[32m成功的课程 ID: {json_data['id']}\033[0m")

        elif text != 'success' :
            if text == 'eywxt.save.stuLimit.error':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:课程人数已满\033[0m")
            if text == 'eywxt.save.kbCt.error':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:课表冲突\033[0m")
            if text == 'eywxt.save.xfLimit.error':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:学分限制\033[0m")
            if text == 'unknownException':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:未知原因\033[0m")
            if text == 'eywxt.save.cantXkByCopy.error':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:已经有这门课了,无需再抢啦")
            if text == 'eywxt.save.msLimit.error':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:选课门数已超过要求控制")
            if text == '该课程无操作权限！':
                print(f"\033[31m课程ID: {json_data['id']}  ,抢课失败!!!原因:该课程这学期未开放")
            remain_list.append(json_data)
        else:
            print(f"错误!{response_data}")
            remain_list.append(json_data)

    return remain_list

