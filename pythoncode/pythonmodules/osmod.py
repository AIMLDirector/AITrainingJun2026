import os

from os import makedirs, getcwd


# os.makedirs, getcwd, chdir, listdir, isfile, isdir, islink,rename, remove, os.path

current_dir = os.getcwd()
print("Current Directory:", current_dir)
changed_dir = os.chdir('/Users/premkumargontrand/AITrainingJun2026/pythoncode/pythonbasics')  

print("List of files and directories in the current directory:", os.listdir(current_dir))
print("List of files and directories in the changed directory:", os.listdir(changed_dir))  
changed_dir = list(os.listdir(changed_dir))
print(type(changed_dir))
for i in changed_dir:
    if os.path.isfile(i):
        print(f"{i} is a file.")
    elif os.paht.isdir(i):
        print(f"{i} is a directory.")
    elif os.path.islink(i):
        print(f"{i} is a symbolic link.")
    else:
        print(f"{i} is neither a file nor a directory.")

file_name = "sample.txt"

if os.path.exists(file_name):
    print(f"{file_name} exists.")
    os.remove(file_name)
else:
    print(f"{file_name} does not exist.")
    with open(file_name, 'w') as f:
        f.write("This is a sample file created for demonstration purposes.")
        f.close()

