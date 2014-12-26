from twisted.web import proxy, http
from twisted.internet import reactor, protocol
from twisted.python import log
import sys

log.startLogging(sys.stdout)

class ProxyFactory(http.HTTPFactory):
	protocol = proxy.Proxy

PORT = int(raw_input('Enter a port number:'))
reactor.listenTCP(PORT, ProxyFactory())
reactor.run()
