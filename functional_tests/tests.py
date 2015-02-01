from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys

class NewVisitorTest(StaticLiveServerTestCase):


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
    

    def test_can_enter_translations_and_retrieve(self):
        #User goes to main page of the TM bucket
        self.browser.get(self.server_url)
        #and sees index page with 'TMBucket' as a browser title and 
        #a header mentioning Translation Repository (bucket)
        header_text = self.browser.find_element_by_tag_name('h1')

        self.assertIn('TMBucket', self.browser.title)
        self.assertIn('TMBucket', header_text.text)
        
        #User is prompted to enter text and its translation.
        inputbox = self.browser.find_element_by_id('id_source_text')
        inputbox2 = self.browser.find_element_by_id('id_target_text')

        self.assertEqual('Enter source text', inputbox.get_attribute('placeholder'))
        self.assertEqual('Enter translation text', inputbox2.get_attribute('placeholder'))
        
        #User enters the text and its translation
        #'This is personal matter of the squirrel'-> 'Das ist ein Privateingelegenheit des Eichhornchens'
        inputbox.send_keys('This is personal matter of the squirrel')
        inputbox2.send_keys('Das ist ein Privateingelegenheit des Eichhornchens') 
        
        #after confirming the entry with hiting 'enter', page reloads
        inputbox2.submit()

        #there is a new URL of lodaed page
        new_list = self.browser.current_url
        
        self.assertRegex(new_list, '/tms/.+')

        #and the entered items are visible (source and target texts) in the table
        
        table = self.browser.find_element_by_id('id_translation_table')
        rows = table.find_elements_by_tag_name('td')
        
        self.check_for_element_in_table('1: This is personal matter of the squirrel')
        self.check_for_element_in_table('Das ist ein Privateingelegenheit des Eichhornchens')

        #there is an editing box again, prompting for further entry
        #User enters another text:
        #'My cat peed in the suitcase' -> 'Meine Katze hat in einem Koffer gepinkelt'

        inputbox = self.browser.find_element_by_id('id_source_text')
        inputbox2 = self.browser.find_element_by_id('id_target_text')
        
        self.assertEqual('Enter source text', inputbox.get_attribute('placeholder'))
        self.assertEqual('Enter translation text', inputbox2.get_attribute('placeholder'))
        
        inputbox.send_keys('My cat peed in the suitcase')
        inputbox2.send_keys('Meine Katze hat in einem Koffer gepinkelt') 
        inputbox2.submit()

        #page updates againa and shows both items on the list
        self.check_for_element_in_table('1: This is personal matter of the squirrel')
        self.check_for_element_in_table('Das ist ein Privateingelegenheit des Eichhornchens')
        self.check_for_element_in_table('2: My cat peed in the suitcase')
        self.check_for_element_in_table('Meine Katze hat in einem Koffer gepinkelt')
                
        #User closes the windows
        self.browser.refresh()
        self.browser.quit()

        #new user comes to the home page
        self.browser = webdriver.Chrome()
        self.browser.get(self.server_url)
        
        #there is no sign of already entered items
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertNotIn('This is personal matter of the squirrel', page_text)
        self.assertNotIn('My cat peed', page_text)

        #User2 enters his own text and translation
        
        inputbox = self.browser.find_element_by_id('id_source_text')
        inputbox2 = self.browser.find_element_by_id('id_target_text')
        inputbox.send_keys('Click here')
        inputbox2.send_keys('Klicken Sie hier')
        inputbox2.submit()
        #page reloads and new URL is created
        yet_new_list = self.browser.current_url

        self.assertRegex(yet_new_list, '/tms/.+')

        #1st URL and 2nd URL are different
        self.assertNotEqual(yet_new_list, new_list)
        #2nd user can see only his items, not items from the 1st user
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Meine Katze', page_text)
        self.assertIn('Klicken', page_text)
       
    def test_layout_and_styles(self):
        #user goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        #input boxes are centered
        inputbox = self.browser.find_element_by_id('id_source_text')
        inputbox2 = self.browser.find_element_by_id('id_target_text')

        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'])/ 2,
            512,
            delta=40)
        #one below the other
        self.assertAlmostEqual(
            inputbox2.location['x'] + inputbox2.size['width']/2,
            512,
            delta=40)

        #after entering the first transunits
        #the transunits are also displayed centered


        


