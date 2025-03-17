import sys
from object.logger import logging# Custom logger import

def error_message_detail(error, error_detail: sys):
    """
    Extracts detailed error information, including file name, line number, and error type.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_type = type(error).__name__  # Getting the error type

    error_message = (
        f"\n[ERROR DETAILS]\n"
        f"  - Error Type: {error_type}\n"
        f"  - File: {file_name}\n"
        f"  - Line: {line_number}\n"
        f"  - Message: {str(error)}\n"
    )

    return error_message


class objException(Exception):
    def __init__(self, error_message, error_detail):
        """
        :param error_message: The error message as a string.
        :param error_detail: System details for traceback extraction.
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

        # Logging the error
        logging.error(self.error_message)

    def __str__(self):
        return self.error_message
