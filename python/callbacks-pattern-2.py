"""
Ref : Mininet clean.py
"""

class Cleanup(object):
    callbacks = []

    @classmethod
    def cleanup(cls):
        print("Cleaning up...")
        for callback in cls.callbacks:
            print("Calling callback...")
            callback()

    @classmethod
    def addCleanupCallback(cls, callback):
        if callback not in cls.callbacks:
            cls.callbacks.append(callback)


cleanup = Cleanup.cleanup
addCleanupCallback = Cleanup.addCleanupCallback


if __name__ == "__main__":
    def foo():
        print("in foo")
    addCleanupCallback(foo)
    cleanup()
