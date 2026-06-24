
def decorator_func(func):  # main function 
    def wrapper():
        print("This is a decorator function.")
        func()
    return wrapper


@decorator_func
def test_func():   # sub function1
    print("This is the test function.")


@decorator_func
def test_func1(): # sub function2 
    print("This is the test function 1.")   

test_func()
test_func1()