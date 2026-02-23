"""
content = assignment
course  = Python Advanced
 
date    = 02.16.2026
email   = tedsandifer@gmail.com
"""


"""
0. CONNECT the decorator "print_process" with all sleeping functions.
   Print START and END before and after.

   START *******
   main_function
   END *********


1. Print the processing time of all sleeping functions.
END - 00:00:00


2. PRINT the name of the sleeping function in the decorator.
   How can you get the information inside it?

START - long_sleeping

"""


import time


#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args):
        
        print(f'{func} has started')
        start_time = time.time()

        func(args)                  # main_function

        end_time = time.time()
        duration = end_time - start_time

        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)

        process_time = (f'{int(hours):02}:{int(minutes):02}:{round(seconds, 3)}')
        print(f'{func} completed with a process time of: {process_time}')
    return wrapper


#*********************************************************************
# FUNC
@print_process
def short_sleeping(name):
    time.sleep(.1)
    print(name)

@print_process
def mid_sleeping(name):
    time.sleep(2)

@print_process
def long_sleeping(name):
    time.sleep(4)


short_sleeping("so sleepy")

mid_sleeping()

long_sleeping()
