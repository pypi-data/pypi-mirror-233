import datetime

class CustomLogger:
    def __init__(self, log_file='custom.log'):
        self.log_file = log_file

    def log(self, message, level='INFO'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        colored_level = {
            'INFO': '\033[92mINFO\033[0m',
            'WARNING': '\033[93mWARNING\033[0m',
            'ERROR': '\033[91mERROR\033[0m',
            'DEBUG': '\033[94mDEBUG\033[0m'
        }.get(level, level)
        
        log_entry = f'{timestamp} - [{colored_level}] - {message}\n'
        with open(self.log_file, 'a') as log_file:
            log_file.write(log_entry)

    def log_info(self, message):
        self.log(message, 'INFO')

    def log_warning(self, message):
        self.log(message, 'WARNING')

    def log_error(self, message):
        self.log(message, 'ERROR')

    def log_debug(self, message):
        self.log(message, 'DEBUG')