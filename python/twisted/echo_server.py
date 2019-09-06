#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
`Twisted Echo Server`
"""

__author__ = 'Rohit Chormale'


from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """
    Echo server protocol
    """
    def connectionMade(self):
	print("%s | New connection" %self.transport.getPeer())
	welcome_msg = """###################################\r\n"""
        msg1 = """      Welcome to Echo Server         \r\n"""
        msg2 = """###################################\r\n"""
        self.transport.write(welcome_msg+msg1+msg2)
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
	print("Client at %s: %s" %(self.transport.getPeer(), data))
        self.transport.write(data)

    def connectionLost(self, reason):
        print("%s | connection lost | reason - %s" %(self.transport.getPeer(), reason))


def get_echo_factory():
    """return factory with echo protocol"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    return factory


def start_echo_server(port, interface):
    factory = get_echo_factory()
    reactor.listenTCP(port, factory, interface=interface)
    reactor.run()


def validate(port, interface):
    import socket
    try:
        if not (1025 <= int(port) <= 65535):
            raise ValueError
        if not interface.lower() == "localhost":
            socket.inet_aton(interface)
	return True
    except ValueError:
        return False
    except socket.error:
        log.msg("Validation | Invalid IP")
        return False
    return True


def main():
    # Take args from user
    interface = raw_input("Enter an interface (default 127.0.0.1): ")
    interface = interface.strip()
    if interface == "": 
        interface = "127.0.0.1"

    port = raw_input("Enter a port (default 9999): ")
    port = port.strip()
    if port == "": 
        port = 9999

    # Validate args 
    if validate(port, interface):
        start_echo_server(int(port), interface)
    else:
        print("Invalid arguments. Exiting !!!")
        sys.exit(1)


if __name__ == '__main__':
    main()
