from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import importlib

def class_for_name(module_name, class_name):
    """
    This is a helper method to get a class reference dynamically
    """
    dir_name = importlib.import_module(module_name)
    return getattr(dir_name, class_name)


class Base_view(object):
    

    def __init__(self,driver,session_data) :
        self.session_data = session_data
        self.driver=driver
        self.wait= WebDriverWait(self.driver, 10)
        self.waitlong= WebDriverWait(self.driver, 60)

    def wait_for(self,locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def waitlong_for(self,locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find(self,locator):
        return self.driver.find_element(*locator)
    @classmethod
    def instance(cls, driver, session_data):
        plat = session_data.os.lower()
        klass = cls.__name__
        if plat != 'android':
            klass = f'{klass}IOS'
        return class_for_name('pages', klass)(driver, session_data)    