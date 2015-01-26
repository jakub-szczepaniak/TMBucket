from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_translations_and_retrieve(self):
        #User goes to main page of the TM bucket

        self.browser.get('http://localhost:8000/')
        #and sees index page with 'TMBucket as a browser title'

        assert 'TMBUcket' in self.browser.title
        #User is prompted to enter text and its translation.
        #'This is personal matter of the squirrel'-> 'Das ist ein Privateingelegenheit des Eichhornchens' 
        #after confirming the entry with clicking 'commit' page updates
        #and the entered items are visible (source and target texts) on the list
        #there is an editing box again, prompting for further entry
        #User enters another text:
        #'My cat peed in the suitcase' -> 'Meine Katze hat in einem Koffer gepinkelt'
        #page updates againa and shows both items on the list
        #in the right-top corner, there is a unique URL generated for entries
        # visiting this URL with the new browser shows entered items
        #User closes the windows
        self.fail('Finish your test!')
if __name__=='__main__':
    unittest.main(warnings='ignore')
