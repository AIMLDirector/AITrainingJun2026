# while <condition>:
#     <action>



# while <condition>:
#     if <condition>:
#         <action>
#     else:
#         <action>    
    

# while True:  # infinite loop
#     <action>
#      if condition:
#          break
         


# while True:  # infinite loop
#     <action>
#          break


while True:
    user_input = input("Enter a number (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break
    else:
        print(f"You entered: {user_input}")


count = 3

while True:
    user_name = input("Enter your name: ")
    user_password  = input("Enter your password: ")
    if user_name == "admin" and user_password == "password":
        print("Login successful!")
        break
    else:
        count -= 1
        print(f"Incorrect credentials. You have {count} attempts left.")
        if count == 0:
            print("Too many failed attempts. Exiting.")
            break 

tasks = ["Data cleaning", "Data transformation", "Data visualization"]

while tasks:
    current_task = tasks.pop(0)  # Get the first task
    print(f"Working on: {current_task}")



total_token = 0
max_token = 50

while total_token < max_token:
    user_input = input ("Enter a message (or 'exit' to quit): ")
    tokens = len(user_input.split())
    print(tokens)
    total_token += tokens
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break
    



  




    

