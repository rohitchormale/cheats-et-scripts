#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
This recipe prvoides example of twisted manhole service.
Run as `twistd -y twisted-manhole-example.tac`
In following example, you can connect to twisted manhole service as follows -
`ssh foo@127.0.0.1 -p 7777`
To disconnect,
`Ctrl-d`
"""

__author__ = "Rohit Chormale"


from twisted.application import service, internet


def getManholeService(port, interface="127.0.0.1"):
    def getManholeFactory(namespace, **kwargs):
        def getManhole(arg):
            return manhole.ColoredManhole(namespace)
        from twisted.conch import manhole, manhole_ssh
        realm = manhole_ssh.TerminalRealm()
        realm.chainedProtocolFactory.protocolFactory = getManhole
        from twisted.cred import portal, checkers
        p = portal.Portal(realm)
        p.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(**kwargs))
        return manhole_ssh.ConchFactory(p)
    return internet.TCPServer(int(port), getManholeFactory(globals(), foo="bar", baz="qux"), interface=interface)


def getWebService(port, interface="127.0.0.1"):
    from twisted.web.static import File
    from twisted.web import server
    resource = File("/tmp")
    site = server.Site(resource)
    return internet.TCPServer(int(port), site, interface=interface)


application = service.Application("Foo")
mainService = service.MultiService()
getManholeService(7777).setServiceParent(mainService)
getWebService(9999).setServiceParent(mainService)
mainService.setServiceParent(application)
