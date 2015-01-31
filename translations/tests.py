from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from translations.views import home_page
from translations.models import TransUnit, TM

class HomePage(TestCase):

    def test_root_url_resolves_to_home_page(self):

        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode(), expected_html)
   


class TMViewTest(TestCase):
    def test_displays_all_items(self):
        tm = TM.objects.create()
        TransUnit.objects.create(
            source='sample1', 
            target='sample2', 
            tm=tm)
        TransUnit.objects.create(
            source='sample3',
            target='sample4',
            tm=tm)

        response = self.client.get('/tms/new-translation-memory/')
        
        self.assertContains(response, 'sample1')
        self.assertContains(response, 'sample2')
        self.assertContains(response, 'sample3')
        self.assertContains(response, 'sample4')

    def test_uses_proper_template(self):
        response = self.client.get('/tms/new-translation-memory/')
        self.assertTemplateUsed(response, 'tms.html')
    def test_saving_POST_request(self):
        
        self.client.post(
            '/tms/new',
            data = {
            'source_text':"Test source string",
            'target_text':'Test target string'})

        self.assertEqual(TransUnit.objects.count(), 1)
        new_transunit = TransUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')

        
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/tms/new',
            data = {
            'source_text':"Test source string",
            'target_text':'Test target string'})
        self.assertRedirects(response,'/tms/new-translation-memory/' )
        



class TransUnitandTMModelTest(TestCase):

    def test_saving_and_retrieving(self):
        tm = TM()
        tm.save()


        first_translation_unit = TransUnit()
        first_translation_unit.source = "Source"
        first_translation_unit.target = "Target"
        first_translation_unit.tm = tm
        first_translation_unit.save()

        second_translation_unit = TransUnit()
        second_translation_unit.source = 'The 2nd Source'
        second_translation_unit.target = 'snd target'
        second_translation_unit.tm = tm
        second_translation_unit.save()

        saved_tm = TM.objects.first()
        self.assertEqual(saved_tm, tm)

        saved_translation_units = TransUnit.objects.all()
        self.assertEqual(saved_translation_units.count(), 2)
       
        first_saved_translation_unit = saved_translation_units[0]
        second_saved_translation_unit = saved_translation_units[1]
        
        self.assertEqual(first_translation_unit, first_saved_translation_unit)
        self.assertEqual(first_saved_translation_unit.tm, tm)
        self.assertEqual(second_saved_translation_unit, second_translation_unit)
        self.assertEqual(second_saved_translation_unit.tm, tm)

        