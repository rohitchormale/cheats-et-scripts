#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
This recipe provides example of typical twisted service framework application.
Run as `twistd -y twisted-daemon-example.tac`
""" 

__author__ = "Rohit Chormale"


from twisted.application import service, internet
from twisted.web.static import File
from twisted.web import server
from twisted.internet import protocol
from twisted.python import log
from twisted.python.logfile import DailyLogFile
log.startLogging(DailyLogFile.fromFullPath("/tmp/foo.log"))


class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)         

                 
def getEchoService(port, interface="127.0.0.1"):
    factory = protocol.ServerFactory()
    factory.protocol = EchoProtocol
    return internet.TCPServer(int(port), factory, interface=interface)             
                 

def getWebService(port, interface="127.0.0.1"):
    resource = File("/tmp")
    site = server.Site(resource)
    return internet.TCPServer(int(port), site, interface=interface)


application = service.Application("Foo")
mainService = service.MultiService()
getWebService(4444).setServiceParent(mainService)
getWebService(5555).setServiceParent(mainService)
getEchoService(6666).setServiceParent(mainService)         
mainService.setServiceParent(application)
    
