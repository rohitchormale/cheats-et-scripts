"""
Create MIME Message 
"""
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.Utils import formatdate
#from email.header import Header
try:
    from cStringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO


ATTACH_FILE = "/tmp/foo.bar"
OUT_FILE = "/tmp/bar.foo"

#headers
msg = MIMEMultipart()
msg['To'] = 'foo@example.com'
msg['From'] = 'xxx@xxx.com'
msg['Subject'] = "Test"
mime_msg['Date'] = formatdate(localtime=True) 

#text message
txtmsg = MIMEText('Please find attachment.')
msg.attach(txtmsg)

# attach file 
try:
    fp = open(ATTACH_FILE, )
    temp = MIMEAudio(fp.read())
    temp.add_header('content-disposition', 'attachment', filename=OUT_FILE)
    fp.close()
    msg.attach(temp)
except (Exception, e):
    print e

final_msg = StringIO(mime_msg.as_string())
#now send ur MIME message using `python/SMTP.py` or 'twisted/esmptFactory.py'

