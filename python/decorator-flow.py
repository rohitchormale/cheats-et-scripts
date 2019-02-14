
def first_decorator(func):
    def wrapper(*args, **kwargs):
        print("in 1st dec before req")
        x = func(*args, **kwargs)
        print("in 1st dec after req")
        return x
    return wrapper

def second_decorator(func):
    def wrapper(*args, **kwargs):
        print("in 2nd dec before req")
        x = func(*args, **kwargs)
        print("in 2nd dec after req")
        return x
    return wrapper

@first_decorator
@second_decorator
def foo():
    print('in main func')
    return 'hola'


x = foo()
print(x)
