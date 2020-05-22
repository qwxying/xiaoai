import smtplib  # 导入发邮件的库
from email.mime.text import MIMEText  # 邮件文本


def send_email(task_id):
    SMTPServer = "smtp.163.com"  # smtp服务器
    From = "qwxying@163.com"  # 发邮件的地址
    TO = "qwxying@qq.com"
    password = "lm141114"  # 发送者邮箱的密码
    # message = "标注任务量:  " + bvpct + ' ' + bvl + "\n检查任务量:  " + jcpct + ' ' + jcl  # 设置发送的内容
    message = "(づ｡◕ᴗᴗ◕｡)づ 来做任务咯"
    msg = MIMEText(message)  # 转换成邮件文本
    msg["Subject"] = task_id + "领取成功"  # 标题
    msg["From"] = From  # 发送者
    msg["To"] = TO  # 接收者
    mailServer = smtplib.SMTP(SMTPServer, 25)  # 创建SMTP服务器/端口号
    mailServer.login(From, password)  # 登录邮箱
    mailServer.sendmail(From, TO, msg.as_string())  # 发送邮件
    mailServer.quit()  # 退出邮箱
