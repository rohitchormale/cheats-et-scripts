"""
To test,
python broadcast_server.py
Enter a port number: 1234

Now open another terminals and create multiple clients, may be using telnet
telnet localhost 9999

telnet localhost 9999

telnet localhost 9999

send message from one of the terminal window, it will be received by all remaining windows.
"""

import datetime
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class Chat(LineReceiver):

	def __init__(self,factory):
		self.factory = factory
		self.remote_ip = None

	def connectionMade(self):
		self.factory.clients.add(self)
		self.remote_ip = self.transport.getPeer().host
		print(f"[{datetime.datetime.now()}] {self.remote_ip} is connected")
		welcome_msg = b"****Welcome to 'awESomE chAtRoom`"
		self.sendLine(welcome_msg)

	def lineReceived(self, line):
		print(f"[{datetime.datetime.now()}] {self.remote_ip} > {line.decode('utf-8')}")
		for user in self.factory.clients:
			if user == self:
				continue
			msg = f"<{self.remote_ip}> {line}"
			user.sendLine(msg.encode('utf-8'))

	def connectionLost(self, reason):
		print(f"[{datetime.datetime.now()}] {self.remote_ip} is disconnected")
		for user in self.factory.clients:
			msg = f"****<{self.remote_ip}> has left room..."
			user.sendLine(msg.encode("utf-8"))
		self.factory.clients.remove(self)

class ChatFactory(Factory):
	def __init__(self):
		self.clients = set()

	def buildProtocol(self, addr):
		return Chat(self)


PORT = int(input("Enter a port number:"))
reactor.listenTCP(PORT, ChatFactory())
reactor.run()
