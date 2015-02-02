from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TransUnitValidationTest(FunctionalTest):
   
    def test_cannot_enter_blank_items(self) :
        #user goes to the home page
        self.browser.get(self.server_url)
        # and hits enter on source and target boxes empty
        self.browser.find_element_by_id('id_source_text').submit()

        # page refreshes and notification is shown
        # that blank items cannot be submitted
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't submit empty string")
        #user now adds some text to source and but not to target
        self.browser.find_element_by_id('id_source_text').send_keys('Sample text')
        self.browser.find_element_by_id('id_target_text').sumbit()
        #page refreshes and notification is shown that blank items cannot be
        #submitted
        error = self.browser.find_element_by_css_selector('.has_error')

        self.self.assertEqual(error.text, "You can't submit empty string")

        #user tries to submit only target text
        input2 = self.browser.find_element_by_id('id_target_text').send_keys('Beispiel')
        input2.submit()
        #page refreshes and same notification is visible
        error = self.browser.find_element_by_css_selector('.has_error')
        self.self.assertEqual(error.text, "You can't submit empty string")        
        
        #finally user adds both source and target texts
        self.browser.find_element_by_id('id_source_text').send_keys('Sample text')
        self.browser.find_element_by_id('id_target_text').send_keys('Beispiel')
        self.browser.find_element_by_id('id_target_text').submit()

        #page refreshes and elements are visible in the table

        table = self.browser.find_element_by_id('id_translation_table')

        self.check_for_element_in_table('Sample text')
        self.check_for_element_in_table('Beispiel')

        self.browser.refresh()



        


