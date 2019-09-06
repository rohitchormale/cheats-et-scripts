#/usr/bin/env python2.7

"""
POC for implementing mutex mechanism using twisted defer
1. Lock requested by Foo
2. Lock requested by Bar
3. Lock acquired by Foo
4. Lock will be released by Foo after sometime
5. Lock will be acquired by queued Bar
"""


from twisted.internet import reactor, defer
mutex = defer.DeferredLock()


def foo():
    print("Lock requested by foo")
    mdf = mutex.acquire()

    def process():
        print("Lock acquired successfully by foo")
        print("Lock will be released after 5 sec")
        reactor.callLater(5, mutex.release)

    mdf.addCallback(lambda x:process())


def bar():
    print("mutex request by bar")
    mdf = mutex.acquire()

    def process():
        print("Lock acquired successfully by bar")
        reactor.stop()

    mdf.addCallback(lambda x:process())


def main():
    foo()
    bar()


if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
