import os
import hashlib
import random
import time
import mimetypes

from guacamole import app

def reset_file(file):
    file.stream.seek(0)

def get_tags(tags_string):
    tags = [tag.strip().lower() for tag in tags_string.split(app.config['TAGS_SEPARATOR'])]
    return tags

def get_time():
    return int(time.time())

def get_mimetype(file_path):
    mimetypes.init()    
    return mimetypes.guess_type(file_path)[0]

def rewind_file(file):
    file.seek(0, os.SEEK_END)

def hash_file(file):
    hasher = hashlib.sha1()
    buffer = file.read(app.config['HASH_BLOCKSIZE'])
    while len(buffer) > 0:
        hasher.update(buffer)
        buffer = file.read(app.config['HASH_BLOCKSIZE'])
    rewind_file(file)
    return hasher.hexdigest()

def get_file_size(file):
    file_size = file.tell()
    rewind_file(file)
    return file_size

def generate_sharded_path():
    shard = generate_shard()
    sharded_path = os.path.join(*shard)
    return sharded_path

def generate_shard():
    random_string = generate_random_string()
    shard = [random_string[i:i+app.config['SHARD_LENGTH']] for i in range(0, len(random_string), app.config['SHARD_LENGTH'])]
    return shard

def generate_random_string():
    random_string = ''.join((random.choice(app.config['SHARD_CHARS'])) for x in range(app.config['SHARD_DEPTH'] * app.config['SHARD_LENGTH']))
    return random_string
