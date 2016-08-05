# tested with python 2.7.11 and python 3.5.2

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

class MyMail:
    def __init__(self, 
            subject, 
            recipients, 
            sender="neised@phys.ethz.ch",
            body=""
            ):
        self.subject = subject
        self.recipients = recipients
        self.body = body
        self.sender = sender
        self.username_pw = ("neised", "262144Dphy")
        self.attachments = []

    def send(self):
        msg = MIMEMultipart()
        msg['From']=self.sender
        msg['Subject']=self.subject
        msg['To'] = ", ".join(self.recipients)
        msg.preamble = "preamble goes here"
        
        if self.attachments:
            self._attach(msg)
        
        msg.attach(MIMEText(self.body, 'plain'))
        
        s = smtplib.SMTP_SSL("smtp.phys.ethz.ch", 465)
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


