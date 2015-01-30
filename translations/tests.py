from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from translations.views import home_page
from translations.models import TranslationUnit

class HomePage(TestCase):

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
        
        self.assertEqual(TranslationUnit.objects.count(), 1)
        new_transunit = TranslationUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')

        
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method='POST'

        request.POST['source_text'] = "Test source string"
        request.POST['target_text'] = 'Test target string'
        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/tms/new-translation-memory/')
    
    def test_home_page_saves_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        
        self.assertEqual(TranslationUnit.objects.count(), 0)

    def test_display_all_items_from_database(self):
        TranslationUnit.objects.create(source='sample1', target='sample2')
        TranslationUnit.objects.create(source='sample3', target='sample4')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('sample1', response.content.decode())
        self.assertIn('sample2', response.content.decode())
        self.assertIn('sample3', response.content.decode())
        self.assertIn('sample4', response.content.decode())

class TMViewTest(TestCase):
    def test_display_all_items(self):
        TranslationUnit.objects.create(source='sample1', target='sample2')
        TranslationUnit.objects.create(source='sample3', target='sample4')

        response = self.client.get('/tms/new-translation-memory/')
        
        self.assertContains(response, 'sample1')
        self.assertContains(response, 'sample2')
        self.assertContains(response, 'sample3')
        self.assertContains(response, 'sample4')


class TranslationUnitModelTest(TestCase):

    def test_saving_and_retrieving(self):
        first_translation_unit = TranslationUnit()
        first_translation_unit.source = "Source"
        first_translation_unit.target = "Target"

        first_translation_unit.save()

        second_translation_unit = TranslationUnit()
        second_translation_unit.source = 'The 2nd Source'
        second_translation_unit.target = 'snd target'

        second_translation_unit.save()

        saved_translation_units = TranslationUnit.objects.all()
        self.assertEqual(saved_translation_units.count(), 2)
       
        first_saved_translation_unit = saved_translation_units[0]
        second_saved_translation_unit = saved_translation_units[1]
        self.assertEqual(first_translation_unit, first_saved_translation_unit)
        self.assertEqual(second_saved_translation_unit, second_translation_unit)

        