import os
import sys
import time
import kpi_names
from pages.base_page import Base_view
from appium.webdriver.common.mobileby import MobileBy 
from hs_logger import logger



root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, '/../lib/')
sys.path.append(lib_dir)
from search_page import SearchPage

class HomePage(Base_view):
    
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        #self.homepage_element=(MobileBy.ID,'com.ril.ajio:id/rotatingParent')
        self.SEARCH_BAR=(MobileBy.ID,'com.ril.ajio:id/llpsTvSearch')
        self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start'] = int(round(time.time() * 1000))
        self.driver.launch_app()
        self.confirm_launch()
        #time.sleep(6)
        self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end'] = int(round(time.time() * 1000))
        self.session_data.app_launch_time = self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end'] - self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start']
        print("cold Launch time = ", self.session_data.app_launch_time)
        self.session_data.pass_count += 1

    def confirm_launch(self):
        self.session_data.status="Fail_launch"
        try:
            #time.sleep(30)
            self.waitlong_for(self.SEARCH_BAR)    
        except:
            print("Error in homepage")

    def search_bar(self):
        self.wait_for(self.SEARCH_BAR).click()
        print("hi")
        SearchPageObject = SearchPage.instance(self.driver, self.session_data)
        #instance(self.driver, self.session_data)
        print("2")
        SearchPageObject.search_bar_2()
        SearchPageObject.filter_products()
        SearchPageObject.select_product()
        logger.info("home page pass")

        #send_keys(SEARCH_KEYWORD+'\n')

    
    