from emailworker import Emailer

__author__ = 'erik'

emailer = Emailer()
message = emailer.init_msg("Test", "Hello!!!")

if __name__ != '__main__':
    emailer.send_email(message)