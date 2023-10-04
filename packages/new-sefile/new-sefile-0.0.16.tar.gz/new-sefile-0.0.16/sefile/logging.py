"""
This file contain all custom logging. In the past this CLI tool used this custom logging, 
but for some reason, i removed it. because it's annoying when i work on this CLI tool in development environment. 
So i'm not using this logging for all next update. But, still i don't want to delete this file, 
because maybe it can be useful in any stuff that i created in the future
"""
# search/logs.py

from sefile import (
    dataclass,
    os, 
    pathlib, 
    logging,
    )
from sefile.exception import exception_factory


def log_file():
    fullpath = os.path.join(pathlib.Path.cwd(), 'search', 'logs')
    has_dir = os.path.isdir(fullpath)
    
    if has_dir:
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target
    else:
        pathlib.Path(fullpath).mkdir(exist_ok=False)
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target

@dataclass(frozen=True)
class CustomLogging:
    format_log: str = '%(name)s | %(asctime)s %(levelname)s - %(message)s'

    def __str__(self) -> None:
        return f"({self.format_log})"

    def __repr__(self) -> None:
        return f"{self.__class__.__name__}({self.format_log})"
    
    def info_log(self, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.INFO)
        logging.info(message)
    
    def error_log(self, exception, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.ERROR)
        logging.error(message)
        raise exception_factory(exception, message)
    
    def debug_log(self, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.DEBUG)
        logging.debug(message)
    
    def warning_log(self, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.WARNING)
        logging.warning(message)
    
    def critical_log(self, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.CRITICAL)
        logging.critical(message)
    
    def notset_log(self, message: str) -> None:
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=self.format_log,
                            level=logging.NOTSET)
        logging.error(message)

