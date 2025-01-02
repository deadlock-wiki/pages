from loguru import logger
import sys
import os
from src.utils.file import write_file
from src.utils.constants import DIRS
from src.utils.parameters import Parameters
import time
params = Parameters()

def setup_logger():
    # Create log dir if it doesn't exist
    if not os.path.exists(DIRS['logs']):
        os.mkdir(DIRS['logs'])
    if not os.path.exists(DIRS['logs-archive']):
        os.mkdir(DIRS['logs-archive'])

    # current time in format: 2021-07-01 12-00-00, used in log name
    current_time = time.strftime('%Y-%m-%d %H-%M-%S')

    # Move existing log file to archive
    log_file_name = f'{DIRS['logs']}/{current_time}.log'
    for file in os.listdir(DIRS['logs']):
        if file.endswith('.log'):
            os.rename(f'{DIRS['logs']}/{file}', f'{DIRS['logs-archive']}/{file}')
    
    # setup custom logger
    logger.remove(0)
    log_level = params.get_param('LOG_LEVEL') 
    logger.add(
        sys.stderr,
        level=log_level,
        format='<white><dim>{time:YYYY-MM-DD HH:mm:ss.SSS} | </dim>'
        '</white><level>{level:<7} <dim>|</dim> <normal>{message}</normal></level>',
    )
    logger.add(
        log_file_name,
        level=log_level,
        format='<white><dim>{time:YYYY-MM-DD HH:mm:ss.SSS} | </dim>'
        '</white><level>{level:<7} <dim>|</dim> <normal>{message}</normal></level>',
    )
    # Usage:
    # logger.trace("This is a trace message") - hidden if verbose is false
    # logger.info("This is an info message") - always shown, use lightly
    # logger.warning("This is a warning message") - always shown, use if user 
    #   should be able to decide if they need to take action
    # logger.error("This is an error message") - always shown