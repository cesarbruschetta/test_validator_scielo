import os

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings


# Create your tests here.
class TestAPIView(APITestCase):

    def setUp(self):
        super(TestAPIView, self).setUp()
 
        self.xml_valid_file = open(os.path.join(settings.BASE_DIR, 'sample_xml_valid.xml'))
        self.xml_invalid_file = open(os.path.join(settings.BASE_DIR, 'sample_xml_invalid.xml'))

    def test_valid_xml(self):
        
        resp = self.client.put(reverse('validators-view'),
                                data={'file': self.xml_valid_file})
                                
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertTrue(data['valid'])
        pri
        
    def test_invalid_xml(self):
        
        resp = self.client.put(reverse('validators-view'),
                               data={'file': self.xml_invalid_file})
                                
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertFalse(data['valid'])
                 