
'''
import smtplib 
#from email.MIMEMultipart import MIMEMultipart 
#from email.MIMEText import MIMEText

pwd = "qibXXC603NzwZrFc"
sendaddr = "neurobrave"
#msg = MIMEMultipart()

#msg['From'] = 'neurobrave@smtp2go.com'
#msg['To'] = 'oleg@neurobrave.com'
#msg['Subject'] = 'My Test Mail '
message = 'This is the body of the mail'
#msg.attach(MIMEText(message))
mailserver = smtplib.SMTP('mail.smtp2go.com',2525)
mailserver.login(sendaddr, pwd)
#mailserver.sendmail('neurobrave@smtp2go.com','oleg@neurobrave.com',msg.as_string())
mailserver.sendmail('oleg@neurobrave.com','oleg@neurobrave.com',"this is email text")

mailserver.quit()

'''

import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


def send_mail(send_from, send_to, subject, message, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    if len(files) > 0: 
        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

'''     
email_subj = "test subj"
email_msg = "test msg"
files = ["whatsnew.txt"]    
    
send_mail(send_from = 'oleg@neurobrave.com', send_to = 'oleg@neurobrave.com',
 subject = email_subj, message = email_msg, files=files,
 server = 'mail.smtp2go.com', port = 2525, username = "neurobrave", password="qibXXC603NzwZrFc")

'''