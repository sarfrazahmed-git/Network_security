import os
import logging
from datetime import datetime
import sys
Log_file = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_path = os.path.join(os.getcwd(), "logs", Log_file)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


if __name__ == "__main__":
    from  Network_security.Myexception.Myexception import CustomException
    logging.info("logging module initialized")
    try:
        1/0
    except Exception as e:
        raise CustomException(f"An error occurred: {e}", sys)