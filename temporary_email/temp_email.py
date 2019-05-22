# encoding:utf-8
import requests
import time
from lxml import etree
import json
import re


class TemporaryEmail:
    """临时邮箱
    使用https://temp-mail.org/zh/,
    监听并返回收到的邮件内容,用以接受验证码
    """

    def __init__(self):
        self.headers = {
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
        # 使用会话先获取邮箱id
        self.session = requests.Session()
        r = self.session.get('https://temp-mail.org/zh/', headers=self.headers)
        selector = etree.HTML(r.text)
        self.email_id = selector.xpath('//*[@id="mail"]/@value')
        self.mid = ''

    def get_email_address(self):
        return self.email_id[0]
#    <div class="col-box">
#       <a href="https://temp-mail.org/zh/view/25d1583a8463272577931cc3e076113d" title="SockBoom- 验证邮件">
#           <span class="inboxSenderName"><span class="bullets-ico is-active"></span></span>
#           <span class="inboxSenderEmail">eply@mail.sockboom</span>
#           <span class="inboxSubject subject-title d-none visable-xs-sm"><small>主题：</small> SockBoom- 验证邮件</span>
#       </a>
#    </div>

    def check_received_email(self):
        # 发送刷新检查是否有邮件并得到邮件资源位置
        time.sleep(2)   #刷新间隔
        r = self.session.get('https://temp-mail.org/zh/option/refresh/')
        selector = etree.HTML(r.text)
        try:
            mid = selector.xpath('//*[@title="SockBoom- 验证邮件"]/@href')
            if(len(mid) == 0):
                return False
            reg = "(?<=(view/)).+"
            self.mid = re.search(reg,mid[0]).group() 
            return True
        except IndexError:
            return False

    def get_email_content(self):

        # 获取邮件内容
        # https://temp-mail.org/zh/source/ + mid
        r2 = self.session.get('https://temp-mail.org/zh/source/' + self.mid)
        return r2.text


if __name__ == '__main__':
    t_email = TemporaryEmail()
    print(t_email.get_email_address())
    while True:
        if t_email.check_received_email():
            content = t_email.get_email_content()
            print(content)
            break
            
