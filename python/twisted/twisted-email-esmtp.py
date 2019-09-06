import sys
import getpass
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from twisted.internet import defer, protocol, reactor, task
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import getPage
from twisted.mail.smtp import ESMTPSenderFactory
try:
    from cStringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

username =   raw_input("Enter you email:")
passwd = getpass.getpass("Enter your password:")
from_addr = username
to_addrs = raw_input("Enter recipients, separated by comma ',':")
to_addrs = to_addrs.split(',')
to_addrs = [addr.strip() for addr in to_addrs if addr.strip()]
to_addrs.append(username)
smtp_host = 'smtp.gmail.com'
smtp_port = 587
msg = 'This is test msg'

def sendMsg():
    print 'Sending msg...'
    edf = defer.Deferred()
    f = ESMTPSenderFactory(username, passwd, from_addr, to_addrs,
                                   StringIO(msg), deferred=edf, retries=3, contextFactory=ClientContextFactory(), requireTransportSecurity=True)
    reactor.connectTCP(smtp_host, smtp_port, f)
    edf.addCallback(success)
    edf.addErrback(failure)

def success(result):
    print 'Success {0}'.format(result)
    reactor.stop()

def failure(error):
    print '***Error {0}'.format(error)
    reactor.stop()

reactor.callLater(3, sendMsg)

if __name__ == '__main__':
    reactor.run()
