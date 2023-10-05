<img src="https://i.ibb.co/sJ9hKXp/Avologger.png" width="300">

# Avologger
[![built with Python3](https://img.shields.io/badge/Built%20with-Python3-blue.svg)](https://www.python.org/)

### A generic logging class for Python

Basic setup and usage are simple.  Just import the class and create a Logger instance with a location to save the log file, it will handle everything else!  
The log files will even be capped at a configurable limit and rotated after they have reached the limit.

To install (via pip):
Next run the install command:
```bash
pip install avologger
```

To install (via source):
Download the source files as an archive and extract them on your computer.

Next run the install command:
```bash
python setup.py install
```

Usage (for more detailed example see avologger_sample.py in sample directory):
```python
from avologger import Logger

def main():
    log = Logger("/logs/test.log")

    log.info("This is a test...")
    log.error("We have a problem!")

if __name__ == "__main__":
    main()
```

### Attributes
*   Log File Location
*   Logger Name (Default: Calling script)
*   Max Log File Size {in Megabytes} (Default: 1 MB)
*   Log File Backup Count (Default: 10)
*   Logging Level (Default: INFO)
*   Log Format (Default: %(levelname)s: [%(name)s]: %(asctime)s - %(message)s)
*   Date Format (Default: %m/%d/%Y %H:%M:%S)

All attributes are configurable, and all except log file location have default values.

### Additional Features
*   Timing decorator (captures the run time of wrapped functions)
*   Logs any uncaught exeptions with the addition of 1 line to your code

### Logging Levels
*   DEBUG
*   INFO
*   WARNING
*   ERROR
*   CRITICAL
*   EXCEPTION

### Log File Sample Output
<img src="https://i.ibb.co/bWv8QfL/Avologger-Sample.png">