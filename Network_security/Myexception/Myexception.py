import sys
from Network_security.logger.logger import logging

def get_exception_detail(error_message, detail:sys):
    _,_,exc_tb = detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    exception_detail = f"Error occurred in script: {file_name} at line number: {line_number} with error message: {error_message}"
    return exception_detail

class CustomException(Exception):
    def __init__(self, error_message, detail:sys):
        super().__init__(error_message)
        self.error_message = error_message
        self.detail = detail
        self.exception_detail = get_exception_detail(error_message, detail)
        logging.error(self.exception_detail)
    def __str__(self):
        return self.exception_detail