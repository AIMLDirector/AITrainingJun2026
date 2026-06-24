def func1():
    a = 10
    print(a)



# argument - static arguments, dynamic arguments, default arguments, infinite arguments

# static arguments
def func2(firstname):
    print("Hello", firstname)


func2("John")

# default arguments
def func3(firstname="john",lastname="doe",age=30):
    print("Hello", firstname + " " + lastname + ", you are " + str(age) + " years old.")    


func3("JOHN", "DOE", 35)


# infinite arguments - *args, **kwargs
def func4(*args):
    print("Arguments passed:", args)


func4(1, 2, 3, "hello", [1, 2, 3], {"key": "value"})


#dynamic arguments
First_name = input("Enter your first name: ")
Last_name = input("Enter your last name: ")
Age = input("Enter your age: ")

def func5(firstname, lastname, age):
    print("Hello", firstname + " " + lastname + ", you are " + str(age) + " years old.")

func5(First_name, Last_name, Age)

# firstname = First_name = input("Enter your first name: ")

def add_numbers(num1, num2):
    return num1 + num2

output_result = add_numbers(5, 10)

print("The sum is:", output_result)


def add_numbers1(num1, num2):
    sum = num1 + num2
    return sum

output_result1 = add_numbers1(10, 10)

print("The sum is:", output_result1)



def add_numbers2(num1:int, num2:int) -> int:
    sum = num1 + num2
    return sum

output_result2 = add_numbers2(20.5, 10)

print("The sum is:", output_result2)


def add_numbers3(num1:int, num2:int) -> int:
    if not isinstance(num1, int) or not isinstance(num2, int):
        raise TypeError("Both arguments must be integers.")
    sum = num1 + num2
    return sum

try:
    output_result3 = add_numbers3(20.5, 10)
    print("The sum is:", output_result3)
except TypeError as e:
    print("Error:", e)