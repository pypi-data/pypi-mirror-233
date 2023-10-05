import logging
import time

# create a class for our log performance test
class MT_PerformanceLogging1:
    def __init__(self, logger_name, log_level=logging.INFO): # craeting function for the  performance 
        self.logger = logging.getLogger(logger_name)  # set the log levels 
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # set the formatter for the logs
        self.handler = logging.StreamHandler()  # using console /stream handler        
        self.handler.setLevel(log_level)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    # logic for the performance test 
    def performance_log(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()       # initial starting time for the performance test
            result = func(*args, **kwargs)
            end_time = time.time()        # final  time for the performance test
            execution_time = end_time - start_time  # duration for the code to take excute the output 
            # logger info gives you the info of the code (function name and excution duration)
            self.logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")

            return result  # after all return the result 
        return wrapper   # return to wrapper function 








