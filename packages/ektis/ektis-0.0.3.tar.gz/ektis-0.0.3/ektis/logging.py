import logging
import os

from datetime import datetime


# 로그 폴더 생성
if os.path.exists("logs") == False:
    os.makedirs("logs")

# 포맷 설정
stream_formatter = logging.Formatter(
    "| %(asctime)s | %(levelname)s | - [!] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_formatter = logging.Formatter(
    "| %(asctime)s | %(levelname)s | - [!] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 로깅 모듈 설정
log = logging.getLogger("logger")
log.setLevel("DEBUG")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

# 포맷 적용 및 포맷 설정
now = datetime.now().strftime("%Y-%m-%d")

file_handler = logging.FileHandler(filename=f"logs/{now}.log", mode="a", encoding="UTF-8")
file_handler.setFormatter(file_formatter)

# 핸들러 추가
log.addHandler(stream_handler)
log.addHandler(file_handler)