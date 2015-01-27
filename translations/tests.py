from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from translations.views import home_page


class NewPage(TestCase):

    def test_root_url_resolves_to_home_page(self):

        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode(), expected_html)
    def test_home_page_can_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['source_text'] = "Test source string"
        request.POST['target_text'] = 'Test target string'
        response = home_page(request)
        
        self.assertIn('Test source string', response.content.decode())
        #self.assertIn('Test target string', response.content.decode())
        expected_html = render_to_string(
                        'home.html', 
                        {'source_item_text': 'Test source string',
                        'target_item_text': 'Test target string'
                         }
            )
        self.assertEqual(response.content.decode(), expected_html)
        