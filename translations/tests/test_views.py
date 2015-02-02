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


    def test_passed_correct_tm_to_template(self):
        first_tm = TM.objects.create()
        correct_tm = TM.objects.create()
        response = self.client.get(
            '/tms/{:d}/'.format(correct_tm.id))
        self.assertEqual(response.context['tm'], correct_tm)
        
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/tms/new',
            data = {
            'source_text':"Test source string",
            'target_text':'Test target string'})
        new_tm = TM.objects.first()
        self.assertRedirects(response,'/tms/{:d}/'.format(new_tm.id) )

class NewTransUnitTest(TestCase):   

    def test_can_save_TransUnit_to_exisiting_tm(self):
        first_tm = TM.objects.create()
        correct_tm = TM.objects.create()

        self.client.post(
            '/tms/{}/add_transunit'.format(correct_tm.id),
            data = {
            'source_text':"Test source string",
            'target_text':'Test target string'})
        
        self.assertEqual(TransUnit.objects.count(), 1)
        new_transunit = TransUnit.objects.first()

        self.assertEqual(new_transunit.source, 'Test source string')
        self.assertEqual(new_transunit.target, 'Test target string')
        self.assertEqual(new_transunit.tm, correct_tm)

    def test_redirects_to_tm_view(self):
        other_tm = TM.objects.create()
        correct_tm = TM.objects.create()

        response = self.client.post(
            '/tms/{}/add_transunit'.format(correct_tm.id),
            data = {
            'source_text':"Test source string",
            'target_text':'Test target string'})

        self.assertRedirects(response, '/tms/{:d}/'.format(correct_tm.id))
       