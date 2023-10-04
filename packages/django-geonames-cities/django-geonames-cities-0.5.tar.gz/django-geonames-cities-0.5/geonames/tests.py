from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json


class ApiCountriesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_not_authenticated(self):
        response = self.client.get('%s%s' % (reverse('geonames:countries'), '?term=tal'))
        #302 relocated al login
        self.assertEqual(response.status_code, 302)

    def test_authenticated(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('%s%s' % (reverse('geonames:countries'), '?term=tal'))
        self.assertEqual(response.status_code, 200)

    def test_finds_italy(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('%s%s' % (reverse('geonames:countries'), '?term=tal'))
        parsed_content = json.loads(response.content)
        '''
            {
              'id': 110,
              'label': 'Italy',
              'code': 'IT',
              'value': 'Italy',
              'data_loaded': False,
              'nic_type': '',
              'nic_input_mask': '',
              'it_codice_catastale': None
            }
        '''
        finds_italy = False
        for c in parsed_content:
            if c['code'] == 'IT':
                finds_italy = True
        self.assertIs(finds_italy, True)

    def test_finds_andorra_city(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('%s%s' % (reverse('geonames:municipalities'), '?term=AndOR&country_id=1'))
        parsed_content = json.loads(response.content)
        '''
            [
              {
                'id': 6,
                'label': 'Andorra la Vella',
                'value': 'Andorra la Vella',
                'content_type': 'geonamesadm1',
                'content_type_id': 8
              }
            ]
        '''
        finds_andorra_city = False
        for c in parsed_content:
            if c['label'] == 'Andorra la Vella':
                finds_andorra_city = True
        self.assertIs(finds_andorra_city, True)
