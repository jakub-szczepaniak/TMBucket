from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    def check_for_element_in_table(self,row_text):
        table = self.browser.find_element_by_id('id_translation_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_enter_translations_and_retrieve(self):
        #User goes to main page of the TM bucket

        self.browser.get('http://localhost:8000/')
        #and sees index page with 'TMBucket' as a browser title and 
        #a header mentioning Translation Repository (bucket)

        self.assertIn('TMBucket', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('TMBucket', header_text.text)
        #User is prompted to enter text and its translation.
        inputbox = self.browser.find_element_by_id('id_source_text')
        self.assertEqual('Enter source text', inputbox.get_attribute('placeholder'))
        inputbox2 = self.browser.find_element_by_id('id_target_text')
        self.assertEqual('Enter translation text', inputbox2.get_attribute('placeholder'))
        #User enters the text and its translation
        #'This is personal matter of the squirrel'-> 'Das ist ein Privateingelegenheit des Eichhornchens'
        inputbox.send_keys('This is personal matter of the squirrel')
        inputbox2.send_keys('Das ist ein Privateingelegenheit des Eichhornchens') 
        
        #after confirming the entry with hiting 'enter', page reloads
        inputbox2.submit()

        #and the entered items are visible (source and target texts) in the table
        table = self.browser.find_element_by_id('id_translation_table')
        rows = table.find_elements_by_tag_name('td')
        self.check_for_element_in_table('1: This is personal matter of the squirrel')
        self.check_for_element_in_table('Das ist ein Privateingelegenheit des Eichhornchens')


        
        #there is an editing box again, prompting for further entry
        #User enters another text:
        #'My cat peed in the suitcase' -> 'Meine Katze hat in einem Koffer gepinkelt'
        inputbox.send_keys('My cat peed in the suitcase')
        inputbox2.send_keys('Meine Katze hat in einem Koffer gepinkelt') 

        inputbox2.submit()

        #page updates againa and shows both items on the list
        self.check_for_element_in_table('1: This is personal matter of the squirrel')
        self.check_for_element_in_table('Das ist ein Privateingelegenheit des Eichhornchens')
        self.check_for_element_in_table('2: My cat peed in the suitcase')
        self.check_for_element_in_table('Meine Katze hat in einem Koffer gepinkelt')
        
        
        #in the right-top corner, there is a unique URL generated for entries
        # visiting this URL with the new browser shows entered items
        #User closes the windows
        self.fail('Finish your test!')
if __name__=='__main__':
    unittest.main(warnings='ignore')
