import os.path
from datetime import datetime
from loguru import logger


class LogUtils:
    def __init__(self, config: dict):
        self.log_dir = config['log']['output_dir']
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        today_timestamp = datetime.today().strftime('%Y-%m-%d')
        self.log_file_path = os.path.join(self.log_dir, f"{today_timestamp}.log")
        self.loguru_file_path = os.path.join(self.log_dir, f"{today_timestamp}-loguru.log")

    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        with open(self.log_file_path, 'a') as file:
            file.write(log_message)

    def open_file_logger(self):
        logger.add(self.loguru_file_path)




