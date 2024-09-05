import os

# redis config
REDIS_DB_HOST = "127.0.0.1"  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password

# mysql config
RELATION_DB_PWD = os.getenv("RELATION_DB_PWD", "123456")  # your relation db password
RELATION_DB_URL = f"mysql://ygq:ygq@172.27.54.34:3306/Crawler"

# sqlite3 config
# RELATION_DB_URL = f"sqlite://data/media_crawler.sqlite"