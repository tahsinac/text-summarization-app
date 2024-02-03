import os
import sys
import logging

# setting up the logging configuration
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir,"running_logs.log")
os.makedirs(log_dir, exist_ok=True)



# The `logging.basicConfig()` function is used to configure the logging module in Python. It sets up
# the logging configuration with the specified parameters.
logging.basicConfig(
    level= logging.INFO,
    format= logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

# The line `logger = logging.getLogger("textSummarizerLogger")` is creating a logger object named
# "textSummarizerLogger".
logger = logging.getLogger("textSummarizerLogger")