import datetime
LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4
}

LOG_COLORS = {
    'DEBUG': '\033[94m',  # Blue
    'INFO': '\033[92m',   # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',   # Red
    'CRITICAL': '\033[91m'  # Red
}


class Logger:
    def __init__(self, name, level=LOG_LEVELS['INFO']):
        self.name = name
        self.level = level

    def log(self, level, message):
        if LOG_LEVELS[level] >= self.level:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_message = f"{timestamp} - {level} - {self.name} - {message}"
            print(f"{LOG_COLORS[level]}{log_message}\033[0m")

    def debug(self, message):
        self.log('DEBUG', message)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def critical(self, message):
        self.log('CRITICAL', message)
