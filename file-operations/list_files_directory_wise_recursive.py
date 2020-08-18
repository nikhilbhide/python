import os
import glob

def list_directories(directories):
    if directories is not None  and len(directories) > 0:
        for directory in directories:
            print(directory)

def explore_directory_recursively(current_dir,separator):
    print(separator + current_dir)
    items=os.listdir(current_dir)
    files = []
    subdirs = []
    for item in items:
        if os.path.isfile(os.path.join(current_dir,item)):
            files.append(item)
        else:
            subdirs.append(item)
    #now iterator over files
    for file in files:
        print(separator + "--" + file)
    #now iterator over subdirectories
    for dir in subdirs:
        explore_directory_recursively(os.path.join(current_dir,dir),separator+"--")

def run():
    print("Enter directory to be explored : ")
    directory_name = input()
    explore_directory_recursively(directory_name,"")

if __name__ == "__main__":
    run()