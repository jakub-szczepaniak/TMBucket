from django.test import TestCase
from django.utils.html import escape
from unittest import skip

from translations.models import TransUnit, TM
from translations.forms import TransUnitForm, EMPTY_SOURCE_ERROR, EMPTY_TARGET_ERROR


class HomePageTest(TestCase):
    maxDiff = None
    
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_transunit_form(self):
        response = self.client.get('/')

        self.assertIsInstance(response.context['form'], TransUnitForm)
class NewTMViewTest(TestCase):
    def post_invalid_input(self):
    
        return self.client.post(
            '/tms/new',
            data = {
            'source':"",
            'target':''})

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/tms/new',
            data = {
            'source':"Test source string",
            'target':'Test target string'})
        new_tm = TM.objects.first()
        self.assertRedirects(response,'/tms/{:d}/'.format(new_tm.id) )

    def test_saving_POST_request(self):
        
        self.client.post(
            '/tms/new',
            data = {
            'source':"Test source string",
            'target':'Test target string'})

        self.assertEqual(TransUnit.objects.count(), 1)
        new_transunit = TransUnit.objects.first()


        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')

    
    def test_invalid_input_renders_home_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_SOURCE_ERROR))

  
    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], TransUnitForm)


    def test_empty_items_are_not_saved(self):
        self.post_invalid_input()
        self.assertEqual(TransUnit.objects.count(), 0)
        self.assertEqual(TM.objects.count(), 0)

class TMViewTest(TestCase):
    def post_invalid_input(self):
        tm_to_use = TM.objects.create()
        return self.client.post(
            '/tms/{}/'.format(tm_to_use.id),
            data = {
            'source':"",
            'target':''})
    def test_displays_tunits_from_proper_tm(self):
        correct_tm = TM.objects.create()
        TransUnit.objects.create(
            source='sample1', 
            target='sample2', 
            tm=correct_tm)
        TransUnit.objects.create(
            source='sample3',
            target='sample4',
            tm=correct_tm)
        
        other_tm = TM.objects.create()
        TransUnit.objects.create(
            source='other text', 
            target='other translation',
            tm=other_tm)

        response = self.client.get('/tms/{:d}/'.format(correct_tm.id))
        

        self.assertContains(response, 'sample1')
        self.assertContains(response, 'sample2')
        self.assertContains(response, 'sample3')
        self.assertContains(response, 'sample4')

        self.assertNotContains(response, 'other text')
        self.assertNotContains(response, 'other translation')

    def test_uses_tms_template(self):
        tm = TM.objects.create()
        response = self.client.get('/tms/{:d}/'.format(tm.id))
        self.assertTemplateUsed(response, 'tms.html')
   


    def test_passed_correct_tm_to_template(self):
        first_tm = TM.objects.create()
        correct_tm = TM.objects.create()
        response = self.client.get(
            '/tms/{:d}/'.format(correct_tm.id))
        self.assertEqual(response.context['tm'], correct_tm)
        
    

    def test_can_save_POST_TransUnit_to_exisiting_tm(self):
        first_tm = TM.objects.create()
        correct_tm = TM.objects.create()

        self.client.post(
            '/tms/{}/'.format(correct_tm.id),
            data = {
            'source':"Test source string",
            'target':'Test target string'})
        
        self.assertEqual(TransUnit.objects.count(), 1)
        new_transunit = TransUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')
        self.assertEqual(new_transunit.tm, correct_tm)

    def test_POST_redirects_to_tms_view(self):
        other_tm = TM.objects.create()
        correct_tm = TM.objects.create()

        response = self.client.post(
            '/tms/{}/'.format(correct_tm.id),
            data = {
            'source':"Test source string",
            'target':'Test target string'})

        self.assertRedirects(response, '/tms/{:d}/'.format(correct_tm.id))
    
    
    def test_displays_transunit_form(self):
        new_tm = TM.objects.create()
        response = self.client.get(
            '/tms/{:d}/'.format(new_tm.id))
        
        self.assertIsInstance(response.context['form'], TransUnitForm)
        self.assertContains(response, 'name="source"')
        self.assertContains(response, 'name="target"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(TransUnit.objects.count(), 0)

    def test_for_invalid_input_renders_tms_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tms.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], TransUnitForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_TARGET_ERROR))


