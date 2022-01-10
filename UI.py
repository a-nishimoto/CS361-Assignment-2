import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def start():
    # driver code that prompts user input
    while True:
        starter = input("Type 'meow' to get a random cat picture: ")
        if starter == "meow":
            # meow is the command to start the process
            with open("./prng-service.txt", "r+") as PRNG:
                # erase prng-service.txt of contents and insert run
                PRNG.truncate(0)
                PRNG.seek(0)
                PRNG.write("run")
                PRNG.close()
            break
        else:
            print("\nYou sure you don't want cat pictures?")

    os.system("python ./PRNG.py")


def pipe_to_imageservice():
    # reads pseudo-random number from prng-service.txt and transmits that to image-service.txt

    # save pseudo-random number
    with open("./prng-service.txt", "r") as PRNG:
        number = PRNG.read()
        PRNG.close()

    if number == "run":
        return

    # write number
    with open("./image-service.txt", "w") as IMG:
        IMG.truncate(0)
        IMG.seek(0)
        IMG.write(number)
        IMG.close()

    os.system("python ./image.py")


def pipe_from_imageservice():

    # read the path
    with open("./image-service.txt", "r") as IMG:
        path = IMG.read()[1:]

    # open the file
    os.startfile(fr"{os.getcwd()}{path}")


def on_modified(event):
    # print(event.src_path)

    if event.src_path == ".\prng-service.txt":
        pipe_to_imageservice()

    if event.src_path == ".\image-service.txt":
        pipe_from_imageservice()


if __name__ == "__main__":

    my_event_handler = PatternMatchingEventHandler(patterns=["*"], case_sensitive=True)
    my_event_handler.on_modified = on_modified

    path = "."
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True)
    my_observer.start()

    start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
