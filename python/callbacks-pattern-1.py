callbacks = []


def addCallback(func):
    callbacks.append(func)


def cleanup():
    for func in callbacks:
        func()


if __name__ == "__main__":
    def foo():
        print("In foo")
    addCallback(foo)
    cleanup()
