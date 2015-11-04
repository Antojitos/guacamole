import os

from copy import copy
from werkzeug import secure_filename
from guacamole import app, db_client
from guacamole.tools import generate_sharded_path, get_tags, hash_file, get_file_size, get_time, get_mimetype


class File(object):
    internal_attributes = ('_id', 'file')

    """docstring for File"""
    def __init__(self, file, tags):
        self.file = file
        if tags:
            self.tags = get_tags(tags)
        self.name = secure_filename(file.filename)
        self.uri = os.path.join(generate_sharded_path(), self.name)
        self.hash = hash_file(file),
        self.size = get_file_size(file)
        self.upload_date = get_time()
        self.mime_type = get_mimetype(self.name)

    def get_meta(self):
        meta = copy(self.__dict__)

        for attribute in self.internal_attributes:
            if attribute in meta:
                del meta[attribute]
        
        return meta

    def save(self):
        self.save_to_disk()
        self.save_to_db()

    def save_to_disk(self):
        file_path = os.path.join(app.config['UPLOAD_DIR'], self.uri)
        file_folder = os.path.dirname(file_path)
        
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)

        self.file.save(file_path)

    def save_to_db(self):
        db_client.db.files.insert_one(self.get_meta())

    @staticmethod
    def find(criteria=None):
        return db_client.db.files.find(criteria)

    @staticmethod
    def find_one(criteria):
        return db_client.db.files.find_one(criteria)
