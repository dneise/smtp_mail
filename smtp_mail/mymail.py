# tested with python 2.7.11 and python 3.5.2
import os
from shutil import copy
import json

import sys
import ast
from datetime import datetime

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

config = read_config_file()

class MyMail:
    def __init__(self, 
            subject, 
            recipients, 
            sender=config["default_sender"],
            body=""
            ):
        self.subject = subject
        recipients = [r if r not in config["contacs"] else config["contacts"][r] for r in recipients]
        self.recipients = recipients
        self.body = body
        self.sender = sender
        self.username_pw = (
            config["smtp"]["username"], 
            config["smtp"]["password"]
        ),
        self.attachments = []

    def send(self):
        msg = MIMEMultipart()
        msg['From']=self.sender
        msg['Subject']=self.subject
        msg['To'] = ", ".join(self.recipients)
        msg['Date'] = time.asctime()
        msg.preamble = "preamble goes here"
        
        if self.attachments:
            self._attach(msg)
        
        msg.attach(MIMEText(self.body, 'plain'))
        
        s = smtplib.SMTP_SSL(config["smtp"]["host"], config["smtp"]["port"])
        s.login(*self.username_pw)
        s.sendmail(self.sender, self.recipients, msg.as_string())
        s.quit()
    

    def add_text(self, text):
        self.body = self.body+'\n'+text

    def _attach(self,msg):
        for f in self.attachments:
        
            ctype, encoding = mimetypes.guess_type(f)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
                
            maintype, subtype = ctype.split("/", 1)
            if maintype == "text":
                fp = open(f)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(f, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(f, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(f, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=f)
            attachment.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(attachment)
    
    def addattach(self, files):
        self.attachments = self.attachments + files


config_file_path = os.path.join(os.environ['HOME'], '.smtp_mail', "config.json")

def copy_template_to_config_path():
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    copy(
        src=os.path.join(_ROOT, 'config.json_template'),
        dst=config_file_path
    )

def read_config_file():
    if not os.path.isfile(config_file_path):
        copy_template_to_config_path()

    with open(config_file_path, "r") as config_file:
        confg = json.load(config_file)
    return config
