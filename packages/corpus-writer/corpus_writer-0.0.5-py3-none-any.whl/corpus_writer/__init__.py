__version__ = "0.0.4"

from .dumper import SafeDumper
from .logger import LOG_FILE, file_logging, setup_logging
from .writer import get_opinion_files_by_year, update_markdown_opinion_file

setup_logging()
file_logging()
