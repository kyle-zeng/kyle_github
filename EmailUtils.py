# coding:utf-8

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr

import smtplib


class EmailUtils(object):

    @staticmethod
    def __format__addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    @staticmethod
    def send_mail():
        # 发件人邮箱地址
        from_addr = '50****68@qq.com'

        # 邮箱密码， qq邮箱是授权码
        password = '****'

        # 收件人邮箱地址
        to_addr = 'zengkaihua10@126.com'

        smtp_server = 'smtp.qq.com'
        # 设置邮件消息

        msg = MIMEText('<html><body><h1>hello</h1><p>异常网页<a href= "http://www.baidu.com">百度</a>'\
                       '<p></body></html>', 'html', 'utf-8')
        msg['from'] = EmailUtils.__format__addr('kyle的爬虫之路<%s>' % from_addr)
        msg['to'] = EmailUtils.__format__addr('kyle的爬虫之路管理员<%s>' % to_addr)
        msg['subject'] = Header('kyle的爬虫之路-猎聘爬虫运行状态', 'utf-8').encode()

        # 发送邮件
        try:
            server = smtplib.SMTP_SSL(smtp_server, 465)

            server.login(from_addr, password)

            server.sendmail(from_addr, [to_addr], msg.as_string())

            server.quit()
        except smtplib.SMTPException as e:
            print '\n\n发送邮件出现错误,错误信息是:{}\n\n'.format(e.smtp_error)  # 错误信息乱码
