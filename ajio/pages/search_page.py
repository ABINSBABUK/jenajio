import os
import sys
from lib import kpi_names 
from pages.base_page import Base_view
from appium.webdriver.common.mobileby import MobileBy
from lib.hs_logger import logger
from product_page import Product_page
import time


root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, '/../lib/')
sys.path.append(lib_dir)

class SearchPage(Base_view):
        
        
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        self.FILTER_BUTTON=(MobileBy.ID,'com.ril.ajio:id/plp_filter_view')
        self.SEARCH_BAR_TEXT_FIELD=(MobileBy.ID,'com.ril.ajio:id/searchETV')
        self.GENDER_BUTTON=(MobileBy.ID,'com.ril.ajio:id/facet_row_name_tv')
        self.INFANTS_CHECKBOK=(MobileBy.ID,'com.ril.ajio:id/general_facet_value_row_tv')
        self.APPLY_FILTER_BUTTON=(MobileBy.ID,'com.ril.ajio:id/filter_view_apply_filter_tv')
        self.PRODUCTS=(MobileBy.ID,'com.ril.ajio:id/plp_row_product_iv')
        self.PRICE_TEXT_FIELD=(MobileBy.ID,'com.ril.ajio:id/product_price_gst_tv') #price inclusive of all taxes  text field
        self.SUGGESTION_FIELD=(MobileBy.ID,'com.ril.ajio:id/search_suggestion')
        # self.searchlist=(MobileBy.ID,'com.ril.ajio:id/plp_row_product_iv')
    
    def search_bar_2(self,SEARCH_KEYWORD='Shirts'):
        self.wait_for(self.SEARCH_BAR_TEXT_FIELD).send_keys(SEARCH_KEYWORD)
        
        # self.wait_for(self.SEARCH_BAR_TEXT_FIELD).send_keys('\n')
        self.driver.execute_script("mobile:performEditorAction", {'action': 'done'})
        self.wait_for(self.SUGGESTION_FIELD).click()
        try:
             self.wait_for(self.SUGGESTION_FIELD).click()
        except:
            print("Suggesion failed")
        self.session_data.kpi_labels[kpi_names.SEARCH_TIME]['start'] = int(round(time.time() * 1000))
        #time.sleep(10)
        self.wait_for(self.PRODUCTS)    
        self.session_data.kpi_labels[kpi_names.SEARCH_TIME]['end'] = int(round(time.time() * 1000))
        self.session_data.search_time = self.session_data.kpi_labels[kpi_names.SEARCH_TIME]['end'] - self.session_data.kpi_labels[kpi_names.SEARCH_TIME]['start']
        print("Time to load search = ", self.session_data.search_time)
        self.session_data.pass_count += 1





    def filter_products(self,FILTER='gender'):
        self.wait_for(self.FILTER_BUTTON).click()
        if FILTER=="gender":
            self.wait_for(self.GENDER_BUTTON).click()
        self.wait_for(self.INFANTS_CHECKBOK).click()
        self.wait_for(self.APPLY_FILTER_BUTTON).click()

    def select_product(self):
        self.wait_for(self.PRODUCTS).click()
        try:
            self.waitlong_for(self.PRICE_TEXT_FIELD).text!=""
        except :
            self.driver.back()
            self.wait_for(self.PRODUCTS).click()
            #self.select_product()
        ProductPageObject = Product_page.instance(self.driver, self.session_data)
        ProductPageObject.buy_product()
        logger.info("search page pass")
    