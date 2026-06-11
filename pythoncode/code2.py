# import the module first - internal or extern
# load the configuration and  environment variables
# initialize the static variables and constants
# main code -- condition , loop, function , class, exception handling
# executing the code 

# importing the module
import os
import pandas
import sys

# loading the configuration and environment variables
from dotenv import load_dotenv
load_dotenv() 
# initializing the static variables , constants, dynamic variables
a = 1
b = 2.5
c = "Hello"
d = input("Enter your name: ")

# main code
def func1():
    print("This is function 1")


# executing the code
if __name__ == "__main__":
    print("This is the main code")
    func1() 
