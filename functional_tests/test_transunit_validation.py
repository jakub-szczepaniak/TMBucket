from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class TransUnitValidationTest(FunctionalTest):
   
    def test_cannot_enter_blank_items(self) :
        #user goes to the home page
        self.browser.get(self.server_url)
        # and hits enter on source and target boxes empty
        self.get_source_input_box().submit()

        # page refreshes and notification is shown
        # that blank items cannot be submitted
        errors = self.browser.find_element_by_css_selector('.has-error')
        self.assertIn(errors.text, "You can't submit empty source string\nYou can't submit empty target string")
        

        #user now adds some text to source and but not to target
        self.get_source_input_box().send_keys('First Sample text')
        self.get_target_input_box().submit()
        #page refreshes and notification is shown that blank items cannot be
        #submitted
        error = self.browser.find_element_by_css_selector('.has-error')

        self.assertEqual(error.text, "You can't submit empty target string")
        #this time user adds both source and target texts
        self.browser.get(self.server_url)
        self.get_source_input_box().send_keys('Proper Sample text')
        self.get_target_input_box().send_keys('Gutes Beispiel')
        self.get_target_input_box().submit()
        #items are visible on the page
       
        
        self.check_for_element_in_table('1: Proper Sample text')
        self.check_for_element_in_table('Gutes Beispiel')
        #user tries to submit only target text
        self.browser.get(self.server_url)
        self.get_target_input_box().send_keys('Beispiel')
        self.get_target_input_box().submit()
        
        #page refreshes and same notification is visible
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't submit empty source string")        
        self.browser.get(self.server_url)
        #finally user adds both source and target texts
        self.get_source_input_box().send_keys('Sample text')
        self.get_target_input_box().send_keys('Beispiel')
        self.get_target_input_box().submit()

        #page refreshes and elements are visible in the table

        table = self.browser.find_element_by_id('id_translation_table')

        self.check_for_element_in_table('1: Sample text')
        self.check_for_element_in_table('Beispiel')

        self.browser.refresh()



        


