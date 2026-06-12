# for i in range(10):
#     print(i)    

# print("_________________")

# for i in range(1, 11):  
#     print(i)

# print("_________________")

# for i in range(1, 11, 2):  
#     print(i)

import subprocess, time
for i in range(5):
    subprocess.run(["df", "-h"])
    time.sleep(2)
    print("__________________________________________________")

