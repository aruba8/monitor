from email.header import Header
from email.mime.text import MIMEText

__author__ = 'erik'

import smtplib


class Emailer():
    def __init__(self):
        from ConfigParser import ConfigParser

        self.config = ConfigParser()
        self.config.read('config.ini')
        self.login = self.config.get('EmailConfigs', 'sender')
        self.password = self.config.get('EmailConfigs', 'password')
        self.to = self.config.get('EmailConfigs', 'to').split(',')

    def init_msg(self, subject, text):
        message = MIMEText(text, _charset='utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self.login
        message['To'] = self.to.__str__()
        return message


    def send_email(self, message):
        try:
            smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465, timeout=10)
            smtp.set_debuglevel(0)
            smtp.login(self.login, self.password)
            smtp.sendmail(message['From'], self.to, message.as_string())
            smtp.close()
            print "Successfully sent email"
        except smtplib.SMTPException:
            print "Error: unable to send email"


if __name__ == '__main__':
    e = Emailer()
    print e.to