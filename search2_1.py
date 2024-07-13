import re  # 正则匹配库，用于模式匹配
import requests  # HTTP库，用于发送网络请求
from bs4 import BeautifulSoup  # HTML解析库，用于解析HTML文档
import time  # 时间库，用于添加延时
import random  # 随机库，用于生成随机数


def visit():
    url = 'https://faculty.xidian.edu.cn/yxsz.jsp?urltype=tree.TreeTempUrl&wbtreeid=1020'
    content = requests.get(url)  # 发送HTTP GET请求获取网页内容
    content.encoding = 'utf-8'  # 确保以UTF-8编码读取内容
    soup = BeautifulSoup(content.text, 'lxml')  # 使用BeautifulSoup解析HTML内容
    final_str = ''
    for x in soup.find_all('div', attrs={"class": "li-b"}):  # 找到所有class为"li-b"的div元素
        final_str += str(x)
        final_str1 = final_str.replace('&amp;', '&')  # 替换HTML转义字符

    # 使用正则表达式查找所有符合条件的学院URL
    college_url = re.findall(
        'xyjslb.jsp.*urltype=tsites.CollegeTeacherList&wbtreeid=1020&st=0&id=.*&lang=zh_CN#collegeteacher', final_str1)

    return college_url  # 返回所有学院的URL列表


def replace_special_str(line):
    for ch in line:
        if ch in "u[]|\'":  # 移除特殊字符
            line = line.replace(ch, "")
    return line


# def visit_every_college(college_url):
#     content = requests.get(college_url)  # 发送HTTP GET请求获取学院页面内容
#     content.encoding = 'utf-8'  # 确保以UTF-8编码读取内容
#     rule = '&nbsp;&nbsp;1/(.*)&nbsp;</td>'  # 匹配总页数的正则表达式
#     Number_of_page = re.findall(rule, content.text)  # 查找总页数
#     Number_of_page = replace_special_str(str(Number_of_page))  # 移除特殊字符
#     Number_of_page = int(Number_of_page)  # 转换为整数
#     match_rule = 'http://faculty.xidian.edu.cn/.*/zh_CN/index.htm'  # 匹配教师个人页面URL的正则表达式
#     final_content = []
#     for i in range(1, (Number_of_page + 1), 1):
#         aim_url = 'https://faculty.xidian.edu.cn/xyjslb.jsp?totalpage=' + str(Number_of_page) + '&PAGENUM=' + str(
#             i) + '&urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1601&lang=zh_CN'
#         aim_url = 'https://faculty.xidian.edu.cn/xyjslb.jsp?totalpage=' + str(Number_of_page) + '&PAGENUM=' + str(
#             i) + '&urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1601&lang=zh_CN'
#         page_content = requests.get(aim_url)  # 发送HTTP GET请求获取每一页的内容
#         page_content.encoding = 'utf-8'  # 确保以UTF-8编码读取内容
#         final_content.extend(re.findall(match_rule, page_content.text))  # 查找并添加所有教师个人页面URL
#     return final_content  # 返回所有教师个人页面URL列表
def visit_every_college(college_url):
    content = requests.get(college_url)
    content.encoding = 'utf-8'  # 确保以 UTF-8 编码读取内容
    rule = '&nbsp;&nbsp;1/(.*)&nbsp;</td>'
    Number_of_page = re.findall(rule, content.text)
    Number_of_page = replace_special_str(str(Number_of_page))
    Number_of_page = int(Number_of_page)
    match_rule = 'http://faculty.xidian.edu.cn/.*/zh_CN/index.htm'
    final_content = []

    # 提取参数部分
    params = re.search(r'urltype=tsites\.CollegeTeacherList&wbtreeid=\d+&st=0&id=\d+&lang=zh_CN', college_url).group()

    for i in range(1, (Number_of_page + 1), 1):
        aim_url = f'https://faculty.xidian.edu.cn/xyjslb.jsp?totalpage={Number_of_page}&PAGENUM={i}&{params}'
        page_content = requests.get(aim_url)
        page_content.encoding = 'utf-8'  # 确保以 UTF-8 编码读取内容
        final_content.extend(re.findall(match_rule, page_content.text))
    return final_content


def spide_teacher_Intro(url_i):
    result = requests.get(url_i)  # 发送HTTP GET请求获取教师个人页面内容
    result.encoding = 'utf-8'  # 确保以UTF-8编码读取内容
    time.sleep(random.randint(0, 1))  # 随机等待0到3秒，模拟人为操作，避免被反爬虫机制发现
    soup = BeautifulSoup(result.text, "lxml")  # 使用BeautifulSoup解析HTML内容

    # 查找教师简介所在的div元素
    div = soup.find("div", attrs={"class": "t_grjj_nr"})
    if div is None:
        div = soup.find("div", attrs={"class": "pro-content"})
        if div is None:
            div = soup.find("div", attrs={"class": "rightfont"})
            if div is None:
                div = soup.find("div", attrs={"class": "t_jbxx_nr"})
                if div is None:
                    return ""
    # str1 = div.text.strip()  # 获取div元素中的文本内容，并去除首尾空白字符
    str1 = div.text.strip().replace('\n', ' ').replace('\r', '').replace('/ Personal Profile', '').replace('+', '')

    div2 = soup.find("div", attrs={"class": "t_photo"})
    if div2 is None:
        div2 = soup.find("div", attrs={"class": "dianzan"})
        if div2 is None:
            return str1
    str2 = div2.text.strip().replace('\n', ' ').replace('\r', '')

    return str2 + "的个人简介:" + str1   # 返回教师简介文本内容


def write_file(filename, final_content):
    with open(filename, 'w', encoding='utf-8') as f:  # 以写模式打开文件，编码方式为UTF-8
        double_teacher_num = len(final_content)
        print(final_content)
        # 以写的方式打开文件，编码方式是utf-8
        for i in range(0, double_teacher_num, 2):  # 从0开始，步长为2
            this_teacher = spide_teacher_Intro(final_content[i])
            print(i)
            f.write('\n')
            # link = "第" + str(int((i / 2) + 1)) + "个老师的个人简介:"
            # f.write(link)
            # f.write('\n')
            f.write(this_teacher.replace('\xa0', ' '))
            f.write('\n')


def obt_filename():
    url = 'https://faculty.xidian.edu.cn/yxsz.jsp?urltype=tree.TreeTempUrl&wbtreeid=1020'
    content = requests.get(url)  # 发送HTTP GET请求获取网页内容
    content.encoding = 'utf-8'  # 确保以UTF-8编码读取内容
    soup = BeautifulSoup(content.text, "lxml")  # 使用BeautifulSoup解析HTML内容
    second_content = ''
    for x in soup.find_all('div', attrs={"class": "li-b"}):  # 找到所有class为"li-b"的div元素
        second_content += str(x)
    rule = 'collegeteacher">(.*)</a>'  # 匹配学院名称的正则表达式
    college_name = re.findall(rule, second_content)  # 查找所有学院名称
    return college_name  # 返回学院名称列表


def main():
    college_list = visit()  # 先获取所有二级学院的列表
    print('Successful access to college list')
    print(college_list)

    college_num = len(college_list)  # 获取学院个数
    print('Number of successful Colleges')
    print(college_num)

    # 现在可以确认爬取所有学院是没有问题的
    college_name = obt_filename()  # 获取所有学院名
    print('Successfully obtained all college names')
    print(college_name)
    # 上面获取学院名也没有问题，下面就是分别读取每一页的内容然后写文件出了问题

    for i in range(college_num - 1):
        # 这一步是遍历学院
        college_url_aim = "https://faculty.xidian.edu.cn/" + college_list[i]
        teacher_url = visit_every_college(college_url_aim)
        print(len(teacher_url))
        print(i)
        print(college_name[i])
        i = str(i)
        file_name = "D:\\pyjy\\" + str(college_name[int(i)]) + '.txt'
        write_file(file_name, teacher_url)  # 将这个系的系名，还有所有老师的url传进写文件的函数


if __name__ == '__main__':
    main()  # 调用main函数，开始程序执行
