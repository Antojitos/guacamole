import unittest
import guacamole
import json
import filecmp

from os import path


class GuacamoleTestCase(unittest.TestCase):

    def setUp(self):
        guacamole.app.config['TESTING'] = True
        self.app = guacamole.app.test_client()

        self.original_file_name = 'image.jpg'
        self.original_file_path = path.join('test', self.original_file_name)
        self.original_file = open(self.original_file_path, 'r')
        self.original_file_tags = 'Mexican, food,fiesta'

    def tearDown(self):
        pass

    def test_post_file(self):
        """Testing file upload: response http status, uploaded file present and identical to original"""

        response = self.app.post('/files/',
                buffered=True,
                content_type='multipart/form-data',
                data={
                    'file': (self.original_file, self.original_file_name),
                    'tags': self.original_file_tags
                })

        uploaded_file_meta = json.loads(response.data)
        uploaded_file_path = path.join('files', uploaded_file_meta['uri'])

        assert '200' in response.status
        assert path.isfile(uploaded_file_path)
        assert filecmp.cmp(self.original_file_path, uploaded_file_path)

if __name__ == '__main__':
    unittest.main()
