import base64
import enum
import hashlib
import logging
import traceback
from copy import deepcopy
import smtplib, ssl
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from twilio.rest import Client

from .hivi_init import Manager


log = logging.getLogger(__name__)
manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
communicationConfig = manager.getCommunicationConfig()
# # if DEBUG :
# print("> hivipy.communication | communicationConfig:: ", communicationConfig)

"""

<TWILIO>
    <account_sid>AC1d203564502e334955e598babc8043c8</account_sid>
    <token>e20b3dc635a225aa725a5e3fb698574f</token>
</TWILIO>"""
class SMS():
    sender = None

    def __init__(self) -> None:
        self.sender = ('00' + str(int(communicationConfig['twilio']['sender']))) if (
            type(communicationConfig) == dict and
            'twilio' in communicationConfig.keys() and
            type(communicationConfig['twilio']) == dict and
            'sender' in communicationConfig['twilio'].keys()
        ) else None

    def send(self,
        body: str,
        recipient: str,
        sender = None,
    ):
        res = 1
        try:
            sender = deepcopy(sender) if sender is not None else self.sender
            client = Client(communicationConfig['twilio']['account_sid'], communicationConfig['twilio']['token'])

            message = client.messages.create(
                body=body,
                from_=sender,
                to=recipient
            )
            return message
        except Exception as err:
            res = 0
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

        return res

class Mailer:
    """Envoie de mail à une ou plusieurs personnes
    """

    def send(self, subject: str = None, body: str = None, sender = None, recipient: str = None, attachment: list = []):
        res = 1
        try:
            host = communicationConfig['mail']['server']
            port = communicationConfig['mail']['port']
            username = communicationConfig['mail']['username']
            password = communicationConfig['mail']['password']
            ssl = communicationConfig['mail']['useSSL']
            tls = communicationConfig['mail']['useTLS']
            sender = sender if type(sender) == str and len(sender) > 0 else communicationConfig['mail']['defaultSender']
            recipient = recipient if type(recipient) == str and len(recipient) > 0 else None
            attachment = list(
                filter(
                    lambda attach: type(attach) == str and len(attach) > 0,
                    attachment,
                )
            ) if type(attachment) in (list, tuple) else []
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender

            if(len(attachment) > 0):
                for index, attach in attachment:
                    with open(attach, 'r') as f:
                        part = MIMEApplication(f.read(), Name=basename(attach))
                        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attach))
                        msg.attach(part)

            server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) if ssl == True else smtplib.SMTP(host, port)
            server.connect(host, port)
            if(tls):
                server.ehlo()
                server.starttls()
            server.ehlo()
            server.login(username, password)
            msg['To'] = recipient

            server.sendmail(from_addr = sender, to_addrs = recipient, msg = msg.as_string())

            res = 1
        except Exception as err:
            res = 0
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

        return res
    def sendHTML(self, subject: str = None, body: str = None, sender = None, recipient: str = None, attachment: list = []):
        res = 1
        try:
            host = communicationConfig['mail']['server']
            port = communicationConfig['mail']['port']
            username = communicationConfig['mail']['username']
            password = communicationConfig['mail']['password']
            ssl = communicationConfig['mail']['useSSL']
            tls = communicationConfig['mail']['useTLS']
            sender = sender if type(sender) == str and len(sender) > 0 else communicationConfig['mail']['defaultSender']
            recipient = recipient if type(recipient) == str and len(recipient) > 0 else None
            attachment = list(
                filter(
                    lambda attach: type(attach) == str and len(attach) > 0,
                    attachment,
                )
            ) if type(attachment) in (list, tuple) else []
            
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = sender

            if(len(attachment) > 0):
                for index, attach in attachment:
                    with open(attach, 'r') as f:
                        part = MIMEApplication(f.read(), Name=basename(attach))
                        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attach))
                        msg.attach(part)

            server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) if ssl == True else smtplib.SMTP(host, port)
            server.connect(host, port)
            if(tls):
                server.ehlo()
                server.starttls()
            server.ehlo()
            server.login(username, password)
            msg['To'] = recipient

            server.sendmail(from_addr = sender, to_addrs = recipient, msg = msg.as_string())

            res = 1
        except Exception as err:
            res = 0
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

        return res

    def sendMultiple(self, subject: str = None, body: str = None, sender = None, recipients: list = [], attachment: list = []):
        res = 1
        try:
            host = communicationConfig['mail']['server']
            port = communicationConfig['mail']['port']
            username = communicationConfig['mail']['username']
            password = communicationConfig['mail']['password']
            ssl = communicationConfig['mail']['useSSL']
            tls = communicationConfig['mail']['useTLS']
            sender = sender if type(sender) == str and len(sender) > 0 else communicationConfig['mail']['defaultSender']
            recipients = list(
                filter(
                    lambda recipient: type(recipient) == str and len(recipient) > 0,
                    recipients,
                )
            ) if type(recipients) in (list, tuple) else []
            attachment = list(
                filter(
                    lambda attach: type(attach) == str and len(attach) > 0,
                    attachment,
                )
            ) if type(attachment) in (list, tuple) else []
            
            msg = MIMEText(body, 'text')
            msg['Subject'] = subject
            msg['From'] = sender

            if(len(attachment) > 0):
                for index, attach in attachment:
                    with open(attach, 'r') as f:
                        part = MIMEApplication(f.read(), Name=basename(attach))
                        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attach))
                        msg.attach(part)

            server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) if ssl == True else smtplib.SMTP(host, port)
            server.connect(host, port)
            if(tls):
                server.ehlo()
                server.starttls()
            server.ehlo()
            server.login(username, password)
            for index, recipient in enumerate(recipients):
                msg['To'] = recipient

                server.sendmail(from_addr = sender, to_addrs = recipient, msg = msg.as_string())

            res = 1
        except Exception as err:
            res = 0
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

        return res
    def sendHTMLMultiple(self, subject: str = None, body: str = None, sender = None, recipients: list = [], attachment: list = []):
        res = 1
        try:
            host = communicationConfig['mail']['server']
            port = communicationConfig['mail']['port']
            username = communicationConfig['mail']['username']
            password = communicationConfig['mail']['password']
            ssl = communicationConfig['mail']['useSSL']
            tls = communicationConfig['mail']['useTLS']
            sender = sender if type(sender) == str and len(sender) > 0 else communicationConfig['mail']['defaultSender']
            recipients = list(
                filter(
                    lambda recipient: type(recipient) == str and len(recipient) > 0,
                    recipients,
                )
            ) if type(recipients) in (list, tuple) else []
            attachment = list(
                filter(
                    lambda attach: type(attach) == str and len(attach) > 0,
                    attachment,
                )
            ) if type(attachment) in (list, tuple) else []
            
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = sender

            if(len(attachment) > 0):
                for index, attach in attachment:
                    with open(attach, 'r') as f:
                        part = MIMEApplication(f.read(), Name=basename(attach))
                        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attach))
                        msg.attach(part)

            server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) if ssl == True else smtplib.SMTP(host, port)
            server.connect(host, port)
            if(tls):
                server.ehlo()
                server.starttls()
            server.ehlo()
            server.login(username, password)
            for index, recipient in enumerate(recipients):
                msg['To'] = recipient

                server.sendmail(from_addr = sender, to_addrs = recipient, msg = msg.as_string())

            res = 1
        except Exception as err:
            res = 0
            stack = str(traceback.format_exc())
            log.error(stack)

        return res