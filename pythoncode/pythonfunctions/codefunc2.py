def func1():
    a = 10
    print(a)


def func2(firstname):
    print("Hello", firstname)


def func3(firstname="john",lastname="doe",age=30):
    print("Hello", firstname + " " + lastname + ", you are " + str(age) + " years old.")    

def func4(*args):
    print("Arguments passed:", args)


def func5(firstname, lastname, age):
    print("Hello", firstname + " " + lastname + ", you are " + str(age) + " years old.")


def add_numbers(num1, num2):
    return num1 + num2


def add_numbers1(num1, num2):
    sum = num1 + num2
    return sum



def add_numbers2(num1:int, num2:int) -> int:
    sum = num1 + num2
    return sum


def add_numbers3(num1:int, num2:int) -> int:
    if not isinstance(num1, int) or not isinstance(num2, int):
        raise TypeError("Both arguments must be integers.")
    sum = num1 + num2
    return sum
