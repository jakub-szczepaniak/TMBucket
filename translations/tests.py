from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from translations.views import home_page
from translations.models import TranslationUnit, TM

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

    def test_uses_tm_view_template(self):

        new_tm = TM.objects.create()
        response = self.client.get('/tms/{id:d}'.format(id=new_tm.id))

        self.assertTemplateUsed(response, 'tms.html')

    def test_display_TU_for_given_TM(self):
        
        correct_trans_mem = TM.objects.create()
        
        TranslationUnit.objects.create(source='sample1', target='sample2', tm=correct_trans_mem)
        TranslationUnit.objects.create(source='sample3', target='sample4', tm=correct_trans_mem)

        response = self.client.get('/tms/{id:d}'.format(id=correct_trans_mem.id))

        self.assertContains(response, 'sample1')
        self.assertContains(response, 'sample2')
        self.assertContains(response, 'sample3')
        self.assertContains(response, 'sample4')
        self.assertNotContains(response, 'sample10')

    def test_can_save_POST_request(self):
        
        self.client.post('/tms/new', 
                    data = {'source_text':"Test source string",
                    'target_text': 'Test target string'}
                    )
        
        self.assertEqual(TranslationUnit.objects.count(), 1)
        
        new_transunit = TranslationUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')

    def test_redirects_after_POST(self):
                
        response = self.client.post(
            '/tms/new',
            data = {'source_text':"Test source string",
                    'target_text': 'Test target string'}
            )
        new_tm = TM.objects.first()
        self.assertRedirects(response, '/tms/{id:d}'.format(id=new_tm.id))
    
    def test_can_save_POST_to_proper_list(self):
    
        first_tm = TM.objects.create()
        second_tm = TM.objects.create()

        self.client.post(
            '/tms/{:d}/add_item'.format(second_tm.id),
            data = {'source_text':"Test source string",
                    'target_text': 'Test target string'}
            )

        self.assertEqual(TranslationUnit.objects.count(), 1)

        new_transunit = TranslationUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.tm, second_tm.id)

    def test_redirects_to_view_list(self):
        other_tm = TM.objects.create()
        correct_tm = TM.objects.create()

        response = self.client.post(
            '/tms/{:d}/add_item'.format(correct_tm.id),
            data = {'source_text':"Test source string",
                    'target_text': 'Test target string'}
            )

        self.assertRedirects(response, '/tms/{:d}/'.format(correct_tm.id))


        
class TMandTUModelTest(TestCase):

    def test_saving_and_retrieving(self):
        tm = TM()
        tm.save()
        first_translation_unit = TranslationUnit()
        first_translation_unit.source = "Source"
        first_translation_unit.target = "Target"
        first_translation_unit.tm = tm

        first_translation_unit.save()

        second_translation_unit = TranslationUnit()
        second_translation_unit.source = 'The 2nd Source'
        second_translation_unit.target = 'snd target'
        second_translation_unit.tm = tm
        second_translation_unit.save()

        saved_tm = TM.objects.first()
        self.assertEqual(saved_tm, tm)

        saved_translation_units = TranslationUnit.objects.all()
        self.assertEqual(saved_translation_units.count(), 2)
       
        first_saved_translation_unit = saved_translation_units[0]
        second_saved_translation_unit = saved_translation_units[1]
        self.assertEqual(first_translation_unit.source, first_saved_translation_unit.source)
        self.assertEqual(first_translation_unit.tm, tm)
        self.assertEqual(second_saved_translation_unit.target, second_translation_unit.target)
        self.assertEqual(second_saved_translation_unit.tm, tm)

        