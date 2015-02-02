from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


   
    
class LayoutAndStylingTest(FunctionalTest): 
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
        self.fail('Finish test!')
        #after entering the first transunits
        #the transunits are also displayed centered





        


