import sys
from src.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
    
        _,_,exc_traceback = error_detail.exc_info()

        self.error_message = error_message,
        self.line_number = exc_traceback.tb_lineno
        self.file_name = exc_traceback.tb_frame.f_code.co_filename

    def __str__(self):

        error = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,
            self.line_number, 
            str(self.error_message)
        )

        logging.error(error)
        return error