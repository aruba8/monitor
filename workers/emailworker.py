__author__ = 'erik'

import smtplib
from email.header import Header
from email.mime.text import MIMEText

from utils.logerconf import Logger
from utils.configparser import Parser


logger = Logger()
log = logger.get_logger()


class Emailer():
    def __init__(self):
        self.config = Parser()


    def init_msg(self, subject, text):
        message = MIMEText(text, _charset='utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self.config.get_login()
        message['To'] = self.config.to.__str__()
        return message

    def send_email(self, message):
        try:
            smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465, timeout=10)
            smtp.set_debuglevel(0)
            smtp.login(self.config.get_login(), self.config.get_password())
            smtp.sendmail(message['From'], self.config.get_to(), message.as_string())
            smtp.close()
            log.info('Successfully sent email')
        except smtplib.SMTPException:
            log.error('Error: unable to send email')