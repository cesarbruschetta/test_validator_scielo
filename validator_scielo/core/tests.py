""" module to teste api """
import os
from PIL import Image
from django.test import TestCase
from django.utils.six import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase


class TestHomePageView(TestCase):
    """ test to home page  """
    
    def test_get_method(self):
        """ teste the method get """
        
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)


class TestAPIView(APITestCase):
    """ Test to Api view """
    
    def setUp(self):
        super(TestAPIView, self).setUp()
 
        self.xml_file = open(os.path.join(settings.BASE_DIR, 'sample_xml.xml'))

    def test_get_method(self):
        """ test the method get """
        
        resp = self.client.get(reverse('validators-view'))
        self.assertEqual(resp.status_code, 200)

    def test_count_errors_xml(self):
        """ test numbers of error in file """
        
        resp = self.client.put(reverse('validators-view'),
                                data={'file': self.xml_file})
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertEqual(len(data['errors']), 74)
        
    def test_invalid_xml(self):
        """ test if invalid xml file """
        
        resp = self.client.put(reverse('validators-view'),
                               data={'file': self.xml_file})
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertFalse(data['valid'])
                 
    def test_invalid_file(self):
        """ test invalid format file """
        
        file = BytesIO()
        Image.new('RGB', (100, 100)).save(file, 'PNG')
        file.seek(0)

        resp = self.client.put(reverse('validators-view'),
                               data={'file': file})
        self.assertEqual(resp.status_code, 400)
        
        data = resp.json()
        self.assertEqual('Invalid file type', data['detail'])                 
                 
    def test_not_file(self):
        """ test not send file to api """
        
        resp = self.client.put(reverse('validators-view'))
        self.assertEqual(resp.status_code, 400)
        
        data = resp.json()
        self.assertEqual('Empty content', data['detail'])

    def test_xml_file_not_parsed(self):
        """ test if file xml not parsed """
        
        xml_file = ContentFile(b'<xml>ERROR FILE</xml>', name='test_file.xml')

        resp = self.client.put(reverse('validators-view'),
                               data={'file': xml_file})
        self.assertEqual(resp.status_code, 400)
        
        data = resp.json()
        self.assertIn('Error', data['detail'])
        