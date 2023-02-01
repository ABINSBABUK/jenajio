import os
import sys
from pages.base_page import Base_view
from appium.webdriver.common.mobileby import MobileBy
from hs_logger import logger

'''
root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, '/../lib/')
sys.path.append(lib_dir)

class Checkout_page(Base_view):


    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        self.PROCEED_PAYMENT_BUTTON=(MobileBy.ID,'com.ril.ajio:id/fragment_cart_list_tv_proceed')



    def checkout_product(self):
        self.wait_for(self.PROCEED_PAYMENT_BUTTON).click()
        logger.info("product page pass")
        self.session_data.status = 'PASSED CHECKOUT'
        '''