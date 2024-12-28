from loguru import logger
import os
import sys
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.utils.parameters import Parameters
params = Parameters()

# setup custom logger
logger.remove(0)
log_level = 'TRACE' if params.is_truthy('VERBOSE') else 'INFO'
logger.add(
    sys.stderr,
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

logger.trace('Trace Test')
logger.info('Info Test')