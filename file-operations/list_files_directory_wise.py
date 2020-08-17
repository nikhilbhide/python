import os

def list_directories(directories):
    if directories is not None  and len(directories) > 0:
        for directory in directories:
            print(directory)

def run():
    print("Enter directory to be explored : ")
    directory_name = input()
    print(directory_name)
    if(directory_name == "."):
        list_directories(os.listdir("."))
        print("listing files and directory in the current directory")
    else:
        try:
            directories = os.listdir(directory_name)
            list_directories(directories)
        except FileNotFoundError:
            print("directory does not exist in the file system")

if __name__ == "__main__":
    run()