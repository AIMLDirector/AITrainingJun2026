# if <condition>:
#     <action>

# if <condition>:
#     <action>
# else:
#     <action>


# if <condition>:
#     <action>
# elif <condition>:
#     <action>
# else:
#     <action>

# # Nested if statements
# if <condition1>:
#     if <condition2>:
#         <action>
#     else:
#         <action>

# if <condition1> and <condition2>:
#     <action>
# else:
#     <action>

# if <condition1> or <condition2>:
#     <action>
# else:
#     <action>

# if not <condition>:
#     <action>
# else:
#     <action>


a = 10
b = 20
c = 30

if a > b:
    print("a is greater than b")


if a > b:
    print("a is greater than b")
else:
    print("a is not greater than b")


if a > b:
    print("a is greater than b")
elif a == b:
    print("a is equal to b")
else:
    print("a is less than b")


if b > a and b > c:
    print("b is the greatest")
elif c > a and c > b:
    print("c is the greatest")
elif a > b and a > c:
    print("a is the greatest")
else:
    print("All numbers are equal")


user_input = input("Enter a number: ")



if not user_input.isdigit():
    print("Invalid input. Please enter a number.")
else:
    print("You entered:", user_input)


# if user_input is None:
#     print("No input provided.")

user_input1 = input("Enter your text: ")

if  "data engineering" in user_input1.lower():
    print("you are asking question related with data engineering field")
else:
    print("you are asking question related with other field", user_input1)  


# input : input length is greater than 50 words , Action : use openai model else google mode
# if the input contains the word - data engineering , data analytics, data scientist - use the model open ai else  llama4 model 

