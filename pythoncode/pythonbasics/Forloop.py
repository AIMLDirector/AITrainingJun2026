
l1 = [1,2,3,4,5]

for i in l1:
    print(i)


for i in l1:
    if i % 2 == 0:
        print(i)


eventlist = []
oddlist = []

for i in l1:
    if i % 2 == 0:
        eventlist.append(i)
    else:
        oddlist.append(i)

print("Even numbers:", eventlist)
print("Odd numbers:", oddlist)


for i in l1:
    if i == 3:
        print("Found 3")
        break
    else:
        print(i)    


logs = ["Error: File not found", 
"Warning: Low disk space",
"Info: User logged in", 
"Error: Out of memory"]

errorlist = []
for i in logs:
    i = i.lower()
    print(i)
    if "error" in i:
        i = i.split(":")[1].strip()
        errorlist.append(i)


print("Error logs:", errorlist)  


email_id = ["user@xyz.com", "kumar@gmail.com", "sam@yahoo.com"]

domainlist = []

for i in email_id:
    domain = i.split("@")[1]
    domainlist.append(domain)

print("Email domains:", domainlist)

command_path = ["/usr/bin/python", "/usr/local/bin/python3", "/bin/bash", "/usr/bin/java"]

for i in command_path:
    command_name = i.split("/")[-1].strip()
    print("Command name:", command_name)


    
