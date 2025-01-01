from loguru import logger
import os
import sys
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.utils.wiki import Wiki
from src.utils.parameters import Parameters
from src.utils.logger import setup_logger
from src.core.reading import PageReader
from src.core.writing import PageWriter
from src.core.validation import DiffValidator

params = Parameters()
setup_logger()



wiki = Wiki(params.get_param('BOT_WIKI_USER'), params.get_param('BOT_WIKI_PASS'))
page_reader = PageReader(wiki)
#page_reader.run()

page_writer = PageWriter()
#page_writer.run()

diff_validator = DiffValidator()
diff_validator.run()