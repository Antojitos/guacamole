import string
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

HOST = '0.0.0.0'
PORT= 5000

UPLOAD_DIR = os.path.join(BASE_DIR, 'files')

MONGO_DBNAME = 'guacamole'

SHARD_CHARS = string.letters + string.digits
SHARD_DEPTH = 6
SHARD_LENGTH = 4

HASH_BLOCKSIZE = 65536

TAGS_SEPARATOR = ','