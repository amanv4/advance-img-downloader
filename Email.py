import smtplib

from config import email_config
import ssl
from Logger import Logging

logger_ins = Logging('Advance Image Extractor')  # Creating an instance of custom logger
logger_ins.initialize_logger()  # Instantiating the logger instance


class SendEmail:

    def __init__(self):
        
        # This function will instantiate the Email object
       
        try:
            self.email = email_config.email
            self.password = email_config.password
        except Exception as e:
            logger_ins.print_log('(Email.py(__init__) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

    def send_notification(self, reciever_email, message):
        
        # This function will be responsible for sending email to the requested user
       
        server = None
        try:
            smtp_server = 'smtp.gmail.com'
            port = 587
            context = ssl.create_default_context()

            server = smtplib.SMTP(smtp_server, port)
            server.starttls(context=context)
            server.login(self.email, self.password)
            logger_ins.print_log('Server login is successful now sending the email...', 'info')
            server.sendmail(self.email, reciever_email, message + '\n')
            logger_ins.print_log('Email sending successful', 'info')

        except Exception as e:
            logger_ins.print_log('(send_notification.py(__init__) - Something went wrong ' + str(e), 'exception')
            raise Exception(e)

        finally:
            if server:
                server.close()
