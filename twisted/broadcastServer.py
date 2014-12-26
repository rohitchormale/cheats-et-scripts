import datetime
from twisted.internet import protocol, reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class Chat(LineReceiver):

	def __init__(self,factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.clients.add(self)
		self.remote_ip = str(self.transport.getPeer().host)
		print '[%s] %s is connected' %(str(datetime.datetime.now()), str(self.remote_ip)) 		
		self.sendLine("****Welcome to 'awESomE chAtRoom`")

	def lineReceived(self, line):
		print "<%s> %s" %(self.remote_ip, line)
		for user in self.factory.clients:
			user.sendLine("<%s> %s" %(self.remote_ip, line))

	def connectionLost(self, reason):
		print '[%s] %s is disconnected' %(str(datetime.datetime.now()), str(self.remote_ip)) 		
		for user in self.factory.clients:
			user.sendLine('****<%s> has left room...' %(self.remote_ip))
		self.factory.clients.remove(self)

	class ChatFactory(Factory):
	def __init__(self):
		self.clients = set()
		
	def buildProtocol(self, addr):
		return Chat(self)		

PORT = int(raw_input("Enter a port number:"))
reactor.listenTCP(PORT, ChatFactory())
reactor.run()
