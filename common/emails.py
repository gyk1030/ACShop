# Author:gyk

# 简单邮件传输协议
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 发送邮件
def to_send(code, email, FROM, SUBJECT, HOST):
    try:
        # 发送邮件主体到对方的邮箱中
        message = MIMEMultipart('related')
        message_html = MIMEText('您正在重置密码，若非本人操作请忽略。验证码：%s' % code, 'plain', 'utf-8')
        message.attach(message_html)

        message['From'] = FROM  # 设置邮件发件人
        message['To'] = email  # 设置邮件收件人
        message['Subject'] = SUBJECT  # 设置邮件标题
        email_client = smtplib.SMTP_SSL(host='smtp.163.com')  # 获取简单邮件传输协议的证书
        email_client.connect(HOST, 465)  # 设置发件人邮箱的域名和端口，端口为465

        email_client.login(FROM, '654321kong')
        email_client.sendmail(from_addr=FROM, to_addrs=email.split(','), msg=message.as_string())
        # 关闭邮件发送客户端
        email_client.close()
        return True, '邮件发送成功'
    except Exception as e:
        return False, '发送邮件超时'
