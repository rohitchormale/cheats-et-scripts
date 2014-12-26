from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor


p = Portal(FTPRealm('./'), [AllowAnonymousAccess(), FilePasswordDB("pass.dat")])
f = FTPFactory(p)
reactor.listenTCP(21, f)
reactor.run()
