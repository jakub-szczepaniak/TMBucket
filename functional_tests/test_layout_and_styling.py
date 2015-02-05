from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


   
    
class LayoutAndStylingTest(FunctionalTest): 
    def test_layout_and_styles(self):
        #user goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        #input boxes are centered
        inputbox = self.get_source_input_box()
        inputbox2 = self.get_target_input_box()

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
        inputbox.send_keys('this is sample source')
        inputbox2.send_keys('Es ist ein Beispiel')
        inputbox2.submit()
        
        #the transunits are also displayed centered
        table = self.browser.find_element_by_id('id_translation_table')
        self.assertAlmostEqual(
            table.location['x'] + table.size['width']/2,
            512,
            delta=40)
        
        
        





        


