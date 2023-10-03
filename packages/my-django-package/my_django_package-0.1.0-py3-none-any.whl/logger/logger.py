from django.views import View
import logging
import logging.handlers

class LoggerView(View):

    def __init__(self, log_file, log_level=logging.INFO, max_size=1000000, backup_count=10):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create a rotating file handler that rotates every day and keeps 10 backup files
        handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=backup_count)
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        self.logger.addHandler(handler)
        
        # Create a console handler for output to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Set the maximum size of the log file
        handler.maxBytes = max_size


        # Set the log level based on the contents of the config file
        # self.set_log_level_from_file()
        
    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)

    def set_log_level_from_file(self, file_path='log_level.txt'):
        try:
            print(file_path)
            with open(file_path, 'r') as file:
                log_level = file.read().strip().upper()
                if log_level == 'DEBUG':
                    self.set_log_level(logging.DEBUG)
                elif log_level == 'INFO':
                    self.set_log_level(logging.INFO)
                elif log_level == 'WARNING':
                    self.set_log_level(logging.WARNING)
                elif log_level == 'ERROR':
                    self.set_log_level(logging.ERROR)
                elif log_level == 'CRITICAL':
                    self.set_log_level(logging.CRITICAL)
                else:
                    self.logger.warning(f"Invalid log level '{log_level}' specified in file '{file_path}'")
        except Exception as e:
            self.logger.warning(f"Error loading log level from file '{file_path}': {str(e)}")