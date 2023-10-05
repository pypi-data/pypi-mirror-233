import os
import sys
import uuid
import logging
from avologger import Logger

script_path = sys.path[0]

def gen_rand_log_name():
    """Generates a random 32 character log name from a UUID

    Returns:
        str: log file name
    """
    
    return f"{uuid.uuid4().hex}.log"

def set_log_path(log_name):
    """Sets the log path by joining the script path and the log name

    Args:
        log_name (str): log file name

    Returns:
        str: path to log file
    """
    
    return os.path.join(script_path, log_name)

def test_create_instance():
    """Tests the creation of the log object instance
    """
    
    log_name = gen_rand_log_name()
    log_path = log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name)

    assert isinstance(log, Logger) == True
    
    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)
    
def test_log_file_creation():
    """Tests that a log file is created
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name)

    assert os.path.exists(log_path) == True
    
    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_debug_log_msg():
    """Tests DEBUG level logging
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="DEBUG")

    found = False

    log_msg = "This is a test DEBUG message."

    log.debug(log_msg)
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True
    
    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)
    
def test_info_log_msg():
    """Tests INFO level logging
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="INFO")

    found = False

    log_msg = "This is a test INFO message." 

    log.info(log_msg)
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_warning_log_msg():
    """Tests WARNING level logging
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="WARNING")

    found = False

    log_msg = "This is a test WARNING message." 

    log.warning(log_msg)
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_error_log_msg():
    """Tests ERROR level logging
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="ERROR")

    found = False

    log_msg = "This is a test ERROR message." 

    log.error(log_msg)
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_critical_log_msg():
    """Tests CRITICAL level logging
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="CRITICAL")

    found = False

    log_msg = "This is a test CRITICAL message." 

    log.critical(log_msg)
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_exception_log_msg():
    """Tests EXCEPTION logging level with and without an exception
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="INFO")

    found = False

    log_msg = "This is a test EXCEPTION message." 
    exc_msg = "Caught exception:"

    log.exception(log_msg)
    
    ## Throw and catch a simple exception to test if the stack is logged
    try:
        x = 5 / 0
    except Exception as e:
        log.exception(f"Caught exception: {e}")
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        if exc_msg in data:
            found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

def test_timing_decorator():
    """Tests the optional timing decorator function wrapper with a subfunction
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="INFO")

    @log.timing
    def sub_function(x):
        """Just sleep for x seconds

        Args:
            x (int): time to sleep in seconds
        """
        import time
        
        time.sleep(x)
    
    sub_function(3)  
    
    found = False

    log_msg = "time taken:" 

    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if log_msg in data:
        found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)

## (FIXED) Having an issue with this since the code run under Pytest, it is catching the exception first before my hook
## even when using Pytest to raise the exception it is not the same as an uncaught exception.    
def test_uncaught_exception():
    """Test the global exception hook logging 
    """
    
    log_name = gen_rand_log_name()
    log_path=set_log_path(log_name)
    log = Logger(log_path, logger_name=log_name, logging_level="INFO")

    ## Set the exception hook
    sys.excepthook = log.my_excepthook

    found = False

    exc_msg = "ZeroDivisionError"

    ## Throw a simple exception and pass it to the uncaught exception hook to test if the stack is logged
    ## This part was tricky to figure out because of the way that Pytest handles exceptions in testing.]
    try:
        x = 5 / 0
    except ZeroDivisionError:
        log.my_excepthook(*sys.exc_info())
    
    assert os.path.exists(log_path) == True
    
    with open(log_path, "r") as rf:
        data = rf.read()
        
    if exc_msg in data:
            found = True
    
    assert found == True

    logging.shutdown()
    if os.path.exists(log_path):
        if os.path.isfile(log_path):
            os.remove(log_path)
