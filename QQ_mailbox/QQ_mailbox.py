from email.mime.text import MIMEText
from email.header import Header
import logging
import smtplib

class QQ_mailbox:
    def __init__(self,sender,password):
        self.sender = sender
        self.password = password
    
    def send_email(self,receiver,subject,content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(self.sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header(subject)
        try:
            smtp_obj = smtplib.SMTP("smtp.qq.com")
            smtp_obj.login(self.sender, self.password)
            smtp_obj.sendmail(self.sender, receiver, message.as_string())
            logging.info("邮件发送成功")
            smtp_obj.quit()
        except smtplib.SMTPException as e:
            logging.info(f"Error: 无法发送邮件 {e}")

    def fromCurriculum(self,data_Curriculum):
        text = ""
        for i in range(len(data_Curriculum)):
            for col in range(1,8):
                for row in range(5):
                    text += f"星期{col},第{row + 1}节,{data_Curriculum[i][row][col]}\n"
            text += "-" * 20 + "\n"
        return text

    def fromcwm(self,datas):
        text = ""
        for data in datas:
            for name in list(data):
                text += f"{name}:{data[name]}\n"
            text += "-" * 20 + "\n"
        return text

    def fromcwm2(self,datas):
        text = "-" * 20 + "\n"
        for data_dict in datas:
            text += f"""
            作品名称:{data_dict["Works_Name"]}\n
            总点击量:{data_dict["data"][1].split(":")[-1]}\n
            月点击量:{data_dict["data"][2].split(":")[-1]}\n
            周点击量:{data_dict["data"][3].split(":")[-1]}\n
            总推荐量:{data_dict["data"][5].split(":")[-1]}\n
            月推荐量:{data_dict["data"][6].split(":")[-1]}\n
            周推荐量:{data_dict["data"][7].split(":")[-1]}\n
            总收藏量:{data_dict["data2"][1]}\n
            总字数:{data_dict["data2"][2]}\n
            """
            text += "-" * 20 + "\n"
        return text
