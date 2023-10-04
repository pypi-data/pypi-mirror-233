# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:34:16 2019

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

import os

# gmail
from typing import List
import smtplib
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .fso import file_exists

## TODO
# async sendmail

class Gmail(object):
    # https://stackoverflow.com/questions/41403458/how-do-i-send-html-formatted-emails-through-the-gmail-api-for-python
    # https://mailtrap.io/blog/python-send-email-gmail/#:~:text=To%20send%20an%20email%20with%20Python%20via%20Gmail%20SMTP%2C%20you,Transfer%20Protocol%20(SMTP)%20server.
    # https://www.w3docs.com/learn-html/mime-types.html
    # https://stackoverflow.com/questions/3902455/mail-multipart-alternative-vs-multipart-mixed
    def __init__(self, server: str='smtp.gmail.com', 
                    port: int=465) -> None:
        self.server = server
        self.port = port

    def send_email(self, from_: str, password_app: str, 
                    email: MIMEMultipart) -> bool:
        with smtplib.SMTP_SSL(self.server, self.port) as server:
            email['From'] = from_
            server.login(from_, password_app)
            server.sendmail(from_, email['To'], email.as_string())

    @staticmethod
    def create_email(to: str, cc: str, bcc: str, subject: str, 
        body: str, attachments: List[str],
        subtype: str='plain') -> MIMEMultipart:

        email = MIMEMultipart()
        body = MIMEText(body, subtype)
        email['To'] = to
        email['Cc'] = cc
        email['Bcc'] = bcc
        email['Subject'] = subject

        email.attach(body)
        for attachment in attachments:
            _ = Gmail._attachment_from_filepath(attachment)
            email.attach(_)

        return email
    
    @staticmethod
    def _attachment_from_filepath(filepath: str) -> MIMEBase:
        if file_exists(filepath):
            filename = os.path.basename(
                os.path.realpath(filepath)
            )
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = 'application/octet-stream'
            type_, _, subtype = mimetype.partition('/')
            base_ = MIMEBase(type_, subtype)
            
            with open(filepath, 'rb') as f:
                base_.set_payload(f.read())

            encoders.encode_base64(base_)
            base_.add_header(
                'Content-Disposition',
                'attachment; filename="{filename}"'.format(filename=filename)
            )
            return base_
        else:
            logger.error('invalid filepath - {filepath}'.format(filepath=filepath))