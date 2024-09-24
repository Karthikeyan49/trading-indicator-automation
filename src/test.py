import threading
import time

# Define the first function to run in a separate thread
def function_one():
    while True:
        global thread_two
        print("Function One is running.")
        print("1")
        time.sleep(1)
        print(thread_two.is_alive())

# Define the second function to run in a separate thread
def function_two(q):
    # while True:
        global thread_two
        print("Function Two is running.")
        print(q)
        time.sleep(2)
              
# Create two threads for each function
thread_one = threading.Thread(target=function_one)
thread_two = threading.Thread(target=function_two,args=(1,))

# Start both threads
thread_one.start()
thread_two.start()