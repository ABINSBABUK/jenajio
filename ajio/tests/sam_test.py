import time
import pytest 
from pages.home_page import HomePage
class TestSample:
	
	test_name = "AJIO_PYTEST"
	package = 'com.ril.ajio'
	activity = 'com.ril.ajio.launch.activity.SplashScreenActivity'
	bundle_id = "com.ril.ajiofnl"

	def test_sample(self, launch):
		HomePageObject = launch
		HomePageObject.search_bar()
        

