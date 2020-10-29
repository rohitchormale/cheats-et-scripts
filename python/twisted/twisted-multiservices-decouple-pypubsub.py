#!/usr/bin/env python
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
from twisted.application import internet
from twisted.python import log
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.python.logfile import DailyLogFile
log.startLogging(DailyLogFile.fromFullPath("test3.log"))
from pubsub import pub

####################################################################
# mock EchoServer - for testing - e.g. rabbitmq 
####################################################################

SERVER_PORT = 9999
SERVER_INTERFACE = '0.0.0.0'


class EchoServer(LineReceiver):

    def connectionMade(self):
        log.msg("@server | New client connected")

    def lineReceived(self, data):
        log.msg("@server | Data received from client | %s" % data)
        resp = b"server says > %s" % data
        self.sendLine(resp)

    def connectionLost(self, reason):
        log.msg("@server | Connection lost")


def startEchoServer():
    factory = protocol.ServerFactory()
    factory.protocol = EchoServer
    reactor.listenTCP(SERVER_PORT, factory, interface=SERVER_INTERFACE)


#############################################################
# EchoClient - here when connection made, subscribe required events
#############################################################
class EchoClient(LineReceiver):
    def connectionMade(self):
        self.sendLine(b"Testing connection")
        log.msg("@client | Connected to server")
        # subscribe required events
        pub.subscribe(self.post, 'rabbitmq')

    def lineReceived(self, line):
        log.msg("@client | %s" % line)

    def post(self, msg):
        log.msg("@client | msg received - %s" % msg)
        log.msg("@client | sending event")
        self.sendLine(b"msg from client")


def startEchoClient():
    factory = protocol.ClientFactory()
    factory.protocol = EchoClient
    reactor.connectTCP(SERVER_INTERFACE, SERVER_PORT, factory)


##########################
# web service
#############################
WEB_PORT = 7777
WEB_INTERFACE = '0.0.0.0'


class WebResource(Resource):
    def render_GET(self, request):
        log.msg("Event received in webservice")
        log.msg("Sending to echoclient via pubsub")
        pub.sendMessage('rabbitmq', msg="bar")
        return b"Success"


def startWebService():
    root = Resource()
    root.putChild(b"init", WebResource())
    factory = Site(root)
    reactor.listenTCP(WEB_PORT, factory, interface=WEB_INTERFACE)


if __name__ == "__main__":
    startEchoServer()
    startEchoClient()
    startWebService()
    reactor.run()