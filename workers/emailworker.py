from email.header import Header
from email.mime.text import MIMEText

import os


__author__ = 'erik'

import smtplib
from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()


class Emailer():
    def __init__(self):
        from ConfigParser import ConfigParser

        self.config = ConfigParser()
        self.__cfile = open(os.path.join(os.getcwd(), 'config.ini'), 'r')
        self.config.readfp(self.__cfile)
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
            log.info('Successfully sent email')
        except smtplib.SMTPException:
            log.error('Error: unable to send email')