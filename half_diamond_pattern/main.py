import os

def print_stars(num):
    if num < 1:
        return
    stars = '*'
    count = 0 

    while(count < num - 1):
        stars = stars + " " + "*"
        count = count + 1

    print (stars)
print("How many diomands to be starred")
try:
    num_starred_diomands = int(input())
except:
    print("Allowed input is a number")
    os._exit()
    
step = 0
for count in range(0,num_starred_diomands):
    if count < num_starred_diomands/2:
        step = step + 1
    else:
        step = step - 1
    print_stars(step)