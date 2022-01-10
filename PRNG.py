import random

# open file, making workable variable
f = open("prng-service.txt", "r+")
file = f.read()

# looks for the command
if "run" in file:

    # deletes everything to leave a blank txt
    f.truncate(0)
    f.seek(0)

    # generate random number
    rand_num = random.randint(1, 100)
    rand_num = str(rand_num)

    # write number to file
    f.write(rand_num)


f.close()  # done here
