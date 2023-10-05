from MT_Performancelogger import MT_PerformanceLogging1
# from src.MT_PY_Performancelogging.MT_Performancelogger import MT_PerformanceLogging1
# test code for our package 
# 

import datetime
import time

# import logging
# # Create an instance of PerformanceLogger
# from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger
# logger = PerformanceLogger(__name__)
# logging.basicConfig(level=logging.INFO,filename='normfunction.log' ,format='%(asctime)s - %(levelname)s - %(message)s')

# # Use the logger to measure function performance
# @logger.log_performance
# # example code to check the loggingperformance 
# # Diasum number =175
# # Disarum Number = 1¹ + 7² + 5³ = 1 + 49 + 125= 175
# # each digit is added with incrementation in power  and the addition of the powered value should be equal to actual input
# def my_function():
#     start_time = time.time()

#     current_time = datetime.datetime.now()

#     num=int(input('Enter Num value:'))

#     result=0

#     power=1

#     for x in str(num):

#         y=int(x)

#         result= result + y**power

#         power=power+1

#     if num==result:

#         print(f'The provide {num} is Disarum')

#     else:

#         print(f'The Provided {num} is Not a Disarum Number')

#     # time sleep function is used to add delay in the execution of a program

#     duration_to_add = datetime.timedelta(hours=0, minutes=1)

# # # Estimate the end time by adding the duration to the current time

#     ended_time = current_time  + duration_to_add
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     logging.info(f'Code execution completed. Elapsed time: started at {current_time} {(start_time *10**3):.4f}  ended at {ended_time} {(end_time *10**3):.4f} = {elapsed_time:.4f} seconds')

# # Call the function

# my_function()









from MT_Performancelogger import MT_PerformanceLogging1

import datetime

import time
import logging
# Create an instance of PerformanceLogger
logger = MT_PerformanceLogging1(__name__)
logging.basicConfig(level=logging.INFO, filename='decoresult.log', format='%(asctime)s - %(levelname)s - %(message)s')
def outer_addition(func):  #wrapped function
    @logger.performance_log
    def inner_addition(a, b):
        start_time = time.time()
        print("I'm in addition")
        sum_result = a + b
        print("Sum of", a, "and", b, "is", sum_result)
        print("Returning addition")
        func(sum_result, a)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Addition execution completed. Elapsed time: {elapsed_time} seconds')
    return inner_addition
def outer_subtraction(func):  #wrapped function
    @logger.performance_log
    def inner_substarction(a, b):
        start_time = time.time()
        print("I'm in subtraction")
        subtraction_result = a - b
        print("Subtraction of", a, "and", b, "is", subtraction_result)
        print("Returning subtraction")
        func(a, b)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Subtraction execution completed. Elapsed time: {elapsed_time} seconds')
    return inner_substarction
@logger.performance_log
@outer_addition
@logger.performance_log
@outer_subtraction
@logger.performance_log
def mOperations(a, b):
    start_time = time.time()
    print("I'm in mOperations")
    print("mOperations execution completed")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f'mOperations execution completed. Elapsed time: {elapsed_time} seconds')
mOperations(15, 10)
