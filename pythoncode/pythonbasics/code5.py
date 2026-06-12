a = 10
b = 10.5
c = "We are learning python"

print(type(a))
print(type(b))
print(type(c))


def func1():
    print("printing within the function",a)
    d = 20
    print("printing within the function for d",d)


func1()
print("printing outside of the function",a)
print("printing outside of the function for d",d)