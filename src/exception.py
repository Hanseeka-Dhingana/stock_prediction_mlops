import sys  # sys interact with the runtime module
# from src.logger import logging  

def error_message_detail(error, error_detail : sys):
    
    # Get the traceback object (The "Black Box" of the crash)
    # exc_info() returns 3 things: (Type, Value, Traceback). 
    # We ignore the first two (_) and keep the third (exc_tb).
    _,_,exc_tb = error_detail.exc_info()
    
    # From the traceback object, we can get the file name 
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Custom message to returned in which file, which line number and what error occured.
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
     file_name,exc_tb.tb_lineno, str(error))
    
    
    return error_message



# Custom Exception class that inherits from the built-in Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail :sys):
        
        # Call the constructor of the parent Exception class
        super().__init__(error_message)
        
        # Create a detailed error message using the helper function
        self.error_message = error_message_detail(error_message, error_detail = error_detail)
        
    # String representation of the CustomException    
    def __str__(self):
        return self.error_message
        
    

# if __name__ == "__main__":
#     try:
#         a = 1 / 0  # This will raise a ZeroDivisionError
#     except Exception as e:
#         custom_exception = CustomException(e, sys)
#         logging.info("Custom Exception Message: {}".format(custom_exception))