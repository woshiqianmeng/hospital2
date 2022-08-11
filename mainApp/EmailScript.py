# from smtplib import SMTP_SSL
#
# def email_1():
#     with SMTP_SSL(host="smtp.qq.com") as smtp :
#         smtp.login(user='771807480@qq.com',password='gswzzekxepfebcdc')
#         smtp.sendmail(from_addr="771807480@qq.com",to_addrs="yipei15913495063@163.com",msg="hello world")
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
class email():
    def demo2(to_addrs,yzm):
        with SMTP_SSL(host="smtp.qq.com") as smtp:
            smtp.login(user='771807480@qq.com', password='gswzzekxepfebcdc')
            msg = MIMEText("verification code:"+yzm, _charset="utf8")
            msg["Subject"] = "Verification code for login"
            smtp.sendmail(from_addr="771807480@qq.com", to_addrs= to_addrs, msg=msg.as_string())

if __name__ == '__main__':
    demo2()