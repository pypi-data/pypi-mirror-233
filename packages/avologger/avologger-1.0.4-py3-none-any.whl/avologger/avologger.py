####################################################################################################
#	Author: Chris O'Brien
#	Created On: December 1, 2021
#	File: avologger.py
#	Description: A lightweight logging wrapper for Avo projects
####################################################################################################
import os
import sys
import inspect
import logging
import logging.handlers
from time import perf_counter
from functools import wraps

class Logger(object):
    def __init__(self, 
                log_file_location: str, 
                logger_name: str = "", 
                max_log_file_size_in_mb: int = 1, 
                log_file_backup_count: int = 10, 
                logging_level: str = "INFO", 
                log_format: str = "%(levelname)s: [%(name)s]: %(asctime)s - %(message)s", 
                date_format: str = "%m/%d/%Y %H:%M:%S"):
        """[summary]

        Args:
            log_file_location (str): The path where the log file resides/will be created
            logger_name (str, optional): The name of the logger object. Defaults to "".
            max_log_file_size_in_mb (int, optional): The maximum file size in MB before the log file is rotated. Defaults to 1.
            log_file_backup_count (int, optional): The maximum number of log files to retain before rotating. Defaults to 5.
            logging_level (str, optional): The minimum default logging level that will be captured. Defaults to "INFO".
            log_format (str, optional): The log message format string. Defaults to "%(levelname)s: [%(name)s]: %(asctime)s - %(message)s".
            date_format (str, optional): The datetime format string of the message timestamp. Defaults to "%m/%d/%Y %H:%M:%S".
        """
        if logger_name != "":
            self.logger_name = logger_name
        else:
            self.logger_name = self.__get_calling_file_name()
            
        self.log_file_location = log_file_location
        self.max_log_file_size_in_mb = max_log_file_size_in_mb
        self.log_file_backup_count = log_file_backup_count
        self.logging_level = logging_level
        self.log_format = log_format
        self.date_format = date_format

        self.__create_log_file()
        self.__setup_logger()

    def __create_log_file(self):
        """Private function to create the log file if it does not already exist.
        """
        # Get the directory portion
        directory = os.path.dirname(self.log_file_location)
        # Check if it exists and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Create the file
        if not os.path.isfile(self.log_file_location):
            with open(self.log_file_location, 'a') as logfile:
                logfile.close()

    def __calculate_max_log_file_size(self):
        """Private function to calculate the max log file size in bytes.

        Returns:
            int: The max filesize of the log file in bytes
        """
        return self.max_log_file_size_in_mb * 1048576

    def __get_calling_file_name(self):
        """Private function that gets the filename of the calling file so that
        multiple files can all log to the same log file but be differentiated.

        Returns:
            str: The name of the calling file.
        """
        frame=inspect.currentframe()
        frame=frame.f_back.f_back
        code=frame.f_code
        
        return code.co_filename

    def __setup_logger(self):
        """Private function that sets up the logger instance according to the passed in parameters.

        Returns:
            logger: logger object
        """
        # Set up a specific logger with our desired output level
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logging_level)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
            self.log_file_location,
            maxBytes=self.__calculate_max_log_file_size(),
            backupCount=self.log_file_backup_count,
            encoding='utf-8')

        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        return self.logger

    # Overloaded logger methods
    def debug(self, log_msg, *args, **kwargs):
        """Overload of the DEBUG level logger method.
        Here to allow for customization.

        Args:
            log_msg (str): The DEBUG log message 
        """
        self.logger.debug(log_msg, *args, **kwargs)

    def info(self, log_msg, *args, **kwargs):
        """Overload of the INFO level logger method.
        Here to allow for customization.

        Args:
            log_msg (str): The INFO log message
        """
        self.logger.info(log_msg, *args, **kwargs)

    def warning(self, log_msg, *args, **kwargs):
        """Overload of the WARNING level logger method.
        Here to allow for customization.


        Args:
            log_msg (str): The WARNING log message
        """
        self.logger.warning(log_msg, *args, **kwargs)

    def error(self, log_msg, *args, **kwargs):
        """Overload of the ERROR level logger method.
        Here to allow for customization.

        Args:
            log_msg (str): The ERROR log message
        """
        self.logger.error(log_msg, *args, **kwargs)
    
    def critical(self, log_msg, *args, **kwargs):
        """Overload of the CRITICAL level logger method.
        Here to allow for customization.

        Args:
            log_msg (str): The CRITICAL log message
        """
        self.logger.critical(log_msg, *args, **kwargs)
    
    def exception(self, log_msg, *args, **kwargs):
        """Overload of the EXCEPTION level logger method.
        Here to allow for customization.  Logs at the ERROR
        level with traceback info.

        Args:
            log_msg (msg): The EXCEPTION log message
        """
        self.logger.exception(log_msg, *args, **kwargs)

    def my_excepthook(self, exc_type, exc_value, exc_traceback):
        """Custom exception hook that intercepts and logs uncaught exceptions
        before passing them on to the system exception hook.  Invoked by using
        "sys.excepthook = log.my_excepthook" in the calling program.

        Args:
            exc_type (str): Exception type
            exc_value (str): Exception value (message)
            exc_traceback (str): Exception stack traceback
        """
        self.logger.exception("Logging an uncaught exception!",
                    exc_info=(exc_type, exc_value, exc_traceback))
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def timing(self, func):
        """
        Runtime wrapper for functions. Also returns args and kwargs.
        """
        @wraps(func)
        def wrap(*args, **kw):
            time_start = perf_counter()
            # run the func
            func_meta = func(*args, **kw)
            time_end = perf_counter()
            run_time = time_end - time_start

            # @NOTE: !r will return repr of func and :.8f is 8 decimal places
            all_meta = f"Function: {func.__name__!r}, args/kwargs: {[args, kw]}, time taken: {run_time:.8f} seconds"
            self.logger.info(all_meta)

            return func_meta
        return wrap
