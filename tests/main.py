import sys
import os
import shutil
import filecmp
import json
import unittest

# Path hack. http://stackoverflow.com/questions/6323860/sibling-package-imports
sys.path.insert(0, os.path.abspath('../guacamole'))
import guacamole

class GuacamoleTestCase(unittest.TestCase):

    def setUp(self):
        guacamole.app.config['TESTING'] = True
        
        self.app = guacamole.app.test_client()

        self.original_file_name = 'image.jpg'
        self.original_file_path = os.path.join('tests/fixtures', self.original_file_name)
        self.original_file = open(self.original_file_path, 'r')
        self.original_file_tags = 'Mexican, food,fiesta'

        if not os.path.exists('files'):
            os.makedirs('files')

    def tearDown(self):
        shutil.rmtree('files')
        pass

    def test_post_file(self):
        """Testing file upload"""

        response = self.app.post('/files/',
                buffered=True,
                content_type='multipart/form-data',
                data={
                    'file': (self.original_file, self.original_file_name)
                })

        uploaded_file_meta = json.loads(response.data)
        uploaded_file_path = os.path.join('files', uploaded_file_meta['uri'])

        assert '200' in response.status
        assert os.path.isfile(uploaded_file_path)
        assert filecmp.cmp(self.original_file_path, uploaded_file_path)

    def test_post_file_with_tags(self):
        """Testing file upload with tags"""

        response = self.app.post('/files/',
                buffered=True,
                content_type='multipart/form-data',
                data={
                    'file': (self.original_file, self.original_file_name),
                    'tags': self.original_file_tags
                })

        uploaded_file_meta = json.loads(response.data)
        uploaded_file_path = os.path.join('files', uploaded_file_meta['uri'])

        assert '200' in response.status
        assert '["mexican", "food", "fiesta"]' in response.data
        assert os.path.isfile(uploaded_file_path)
        assert filecmp.cmp(self.original_file_path, uploaded_file_path)

if __name__ == '__main__':
    unittest.main()