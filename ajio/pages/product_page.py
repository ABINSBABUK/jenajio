
import os
import sys
from pages.base_page import Base_view
from appium.webdriver.common.mobileby import MobileBy
from hs_logger import logger
#from checkout_page import Checkout_page

root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, '/../lib/')
sys.path.append(lib_dir)

class Product_page(Base_view):
        
        
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        self.ADD_TO_BAG_BUTTON=(MobileBy.ID,'com.ril.ajio:id/add_to_cart_tv')
        self.VIEW_BAG_BUTTON=(MobileBy.ID,'com.ril.ajio:id/add_to_cart_tv')
        #self.SIZE_BUTTON=(MobileBy.XPATH,"//android.widget.TextView[@text='2-3Y']”) com.ril.ajio:id/row_pdp_variable_size_tv
        self.SIZE_BUTTON=(MobileBy.ID,'com.ril.ajio:id/row_pdp_fixed_size_layout')
        self.ADD_TO_BAG_LARGE_BUTTON=(MobileBy.ID,'com.ril.ajio:id/add_to_cart_tv')

    def buy_product(self):
        self.waitlong_for(self.ADD_TO_BAG_BUTTON).click()
        try:
            self.waitlong_for(self.ADD_TO_BAG_BUTTON).click()
            self.waitlong_for(self.ADD_TO_BAG_BUTTON).click()
        except:
            pass
        self.wait_for(self.SIZE_BUTTON).click()
        self.wait_for(self.ADD_TO_BAG_LARGE_BUTTON).click()
        '''
        self.wait_for(self.VIEW_BAG_BUTTON).click()
        CheckoutPageObject = Checkout_page.instance(self.driver, self.session_data)
        CheckoutPageObject.checkout_product()
        logger.info("product page pass")'''


