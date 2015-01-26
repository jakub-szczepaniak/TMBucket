from django.core.urlresolvers import resolve
from django.test import TestCase
from translations.views import home_page


class NewPage(TestCase):

    def test_root_url_resolves_to_home_page(self):

        found = resolve('/')
        self.assertEqual(found.func, home_page)