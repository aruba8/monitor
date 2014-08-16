__author__ = 'erik'

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils.logerconf import Logger
from utils.configparser import Parser
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'))
email_template = env.get_template('email_base_template.html')
logger = Logger()
log = logger.get_logger()


class Emailer():
    def __init__(self):
        self.config = Parser()

    def init_msg(self, subject, body):
        message = MIMEMultipart('alternative')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self.config.get_login()
        message['To'] = self.config.to.__str__()
        part = MIMEText(email_template.render(body=body), 'html', _charset='utf-8')
        message.attach(part)
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