#coding:utf-8
import requests
import datetime
import pyperclip
import re
from temporary_email.temp_email import TemporaryEmail
headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
#发送邮箱验证码
def send_email():
    url = "https://sockboom.net/auth/send"
    #email: pwmhrs73890@chacuo.net
    #{"ret":1,"msg":"\u9a8c\u8bc1\u7801\u53d1\u9001\u6210\u529f\uff0c\u8bf7\u67e5\u6536\u90ae\u4ef6\u3002"}
    try:
        r_json = requests.post(url,{'email': email_adr},headers=headers).json()
        if r_json['ret'] == 1:
            print(r_json['msg'])
            return True
        else:
            return False
    except IndexError:
        print("注册邮件发送失败，请检查网站是否可以打开！")
        return False

#轮询邮箱验证码
def check_email():
    while True:
        #检查邮件
        timeNow = datetime.datetime.now().strftime("%H:%M:%S")
        print("正在查询验证码: " + temp_email.get_email_address() + " " + timeNow)
        if temp_email.check_received_email():
            #输出邮件
            content = temp_email.get_email_content()
            reg = "(?<=(<b>)).{6}(?=<)"
            ver_code = re.search(reg,content).group()
            return ver_code

#填写注册
def register_up(email_code):
    url = "https://sockboom.net/auth/register"
    data = {
        "email": email_adr,
        "name": username,
        "aff": 0,
        "passwd": email_adr,        #账号密码同号
        "repasswd": email_adr,
        "wechat": 'wechat',
        "imtype": 'imtype',
        "emailcode": email_code
    }
    r_json = requests.post(url,data,headers=headers).json()
    #{'ret': 1, 'msg': '注册成功'}
    if r_json['ret'] == 1:
        print(r_json['msg'])
        return True
    else:
        print(r_json['msg'])
        return False

temp_email =  TemporaryEmail() #临时邮件对象
email_adr = temp_email.get_email_address()      #邮件地址
reg = ".+(?=@)"
username = re.search(reg,email_adr).group()     #注册用户名

print("临时邮箱地址：" + email_adr)

#发送邮箱验证码
print("正在发送注册邮件")
while(True):
    if send_email():
        break
#查询验证码
emailcode = check_email()
#注册
over_time = datetime.datetime.now() + datetime.timedelta(days = 1)  #日期+1天
if register_up(emailcode):
    user_info = "账号失效日期：" + over_time.strftime("%Y-%m-%d %H:%M") + "\n账号：" + username + "\n密码：" + email_adr
    print("\n-----------------------------\n" + user_info + "\n-----------------------------\n")
#查询订阅地址
#登陆
user_url = "https://sockboom.net/user"
login_url = 'https://sockboom.net/auth/login'
data = {
    'email': email_adr,
    'passwd': email_adr
}
session = requests.Session()        #Session自动处理Cookie
state = session.post(login_url,data,headers=headers).json()
if state['ret'] == 1:
    print("登陆成功")
else:
    print("登陆出现问题：" + state['msg'])
#截取订阅地址
user_page = session.get('https://sockboom.net/user/',headers=headers).text
reg = "(?<=(no\">))https://sockboom.me/.+(?=<)"
sub = re.search(reg,user_page).group()
print("订阅地址已复制到剪贴板：" + sub)
#保存注册信息
f = open('sockboom账号.txt','a')
f.write("\n-----------------------------\n" + user_info + "\n-----------------------------\n")
f.write("\n订阅地址：" + sub + '\n')
print("账户文件已保存")
f.close()
pyperclip.copy(sub) #保存到剪贴板
