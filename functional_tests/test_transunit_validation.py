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
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't submit empty string")
        #user now adds some text to source and but not to target
        self.get_source_input_box().send_keys('Sample text')
        self.get_target_input_box().submit()
        #page refreshes and notification is shown that blank items cannot be
        #submitted
        error = self.browser.find_element_by_css_selector('.has-error')

        self.assertEqual(error.text, "You can't submit empty string")
        #this time user adds both source and target texts
        self.get_source_input_box().send_keys('Sample text')
        self.get_target_input_box().send_keys('Beispiel')
        self.get_target_input_box().submit()
        #items are visible on the page
        table = self.browser.find_element_by_id('id_translation_table')

        self.check_for_element_in_table('1: Sample text')
        self.check_for_element_in_table('Beispiel')
        #user tries to submit only target text
        self.get_target_input_box().send_keys('Beispiel')
        self.get_target_input_box().submit()
        
        #page refreshes and same notification is visible
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't submit empty string")        
        
        #finally user adds both source and target texts
        self.get_source_input_box().send_keys('Sample text')
        self.get_target_input_box().send_keys('Beispiel')
        self.get_target_input_box().submit()

        #page refreshes and elements are visible in the table

        table = self.browser.find_element_by_id('id_translation_table')

        self.check_for_element_in_table('2: Sample text')
        self.check_for_element_in_table('Beispiel')

        self.browser.refresh()



        


