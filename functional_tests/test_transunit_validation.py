from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TransUnitValidationTest(FunctionalTest):
   
    def test_cannot_enter_blank_items(self) :
        #user goes to the home page
        # and hits enter on source and target boxes empty
        # page refreshes and notification is shown
        # that blank items cannot be submitted
        #user now adds some text to source and target
        #user clicks submit and items are added/displayed
        #user adds text to source but not to target
        #page refreshes and notification is shown that blank items cannot be
        #submitted
        #user adds some text to target but not to source
        #page refreshes and notification is shown that blank items cannot be 
        #submitted
        self.fail('Finish your test')



        


