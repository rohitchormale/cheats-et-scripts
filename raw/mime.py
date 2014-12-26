"""
Create MIME Message 
"""
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart


ATTACH_FILE = "/tmp/foo.bar"

#headers
msg = MIMEMultipart()
msg['To'] = self.config['email']
msg['From'] = 'ivr@xxx.com'
msg['Subject'] = self.caller_id

#text message
txtmsg = MIMEText('Please find attachment.')
msg.attach(txtmsg)

# attach file 
try:
    fp = open(ATTACH_FILE, )
    temp = MIMEAudio(fp.read())
    temp.add_header('content-disposition', 'attachment', filename=self.outfile)
    fp.close()
    msg.attach(temp)
except Exeption as e:
    print e

#now send ur MIME message using `python/SMTP.py` or 'twisted/esmptFactory.py'

