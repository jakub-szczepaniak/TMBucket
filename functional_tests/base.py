from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        
        self.browser.refresh()
        self.browser.quit()
    def check_for_element_in_table(self,row_text):
        
        table = self.browser.find_element_by_id('id_translation_table')
        rows = table.find_elements_by_tag_name('td')
        
        self.assertIn(row_text, [row.text for row in rows])
    def get_source_input_box(self):
        return self._get_input_box('id_source')
    def get_target_input_box(self):
        return self._get_input_box('id_target')
    def _get_input_box(self, id_input):
        return self.browser.find_element_by_id(id_input)
    




        


