from __future__ import absolute_import
from __future__ import print_function
import sys
import argparse
import os
import time
import random
import boto3
import subprocess
from six.moves import range
import uuid
import random

from selenium import webdriver         #changed
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

from appium import webdriver as AppiumWebdriver     #extra
from appium.webdriver.common.touch_action import TouchAction
sys.path.append('..lib/setup/py_modules_citi')
sys.path.append('..lib/setup/py_modules')
import citi_worthi_data
from hs_logger import logger
import pytest


###########here and conftest moving?
#check in to this

from mysql_insert_citi import MysqlDataInsert
from log_adb_info  import AdbDdata

script_dir = os.path.dirname(os.path.abspath(__file__))

def addoption(parser):
    parser.addoption('--udid', '--udid', dest='udid',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="udid")
    parser.addoption('--appium_input', '--appium_input', dest='appium_input',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="appium_input")
    parser.addoption('--device_os', '--device_os', dest='device_os',
                        type=str, nargs='?',
                        default=None,
                        required=True,
                        help="device_os")
    parser.addoption('--browser', '--browser', dest='browser',
                        type=str, nargs='?',
                        default=None,
                        required=True,
                        help="browser")
    parser.addoption('--device', '--device', dest='device',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="device")
    parser.addoption('--selenium_url', '--selenium_url', dest='selenium_url',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="selenium_url")
    parser.addoption('--env', '--env', dest='env',
                        type=str, nargs='?',
                        default=None,
                        required=True,
                        help="device")
    
    

def init_args(request, session_data):
    
    

    #	session_data.platform = request.config.getoption("platform")
    session_data.udid = request.config.getoption("udid")
    session_data.appium_input = request.config.getoption("appium_input")
    session_data.browser = request.config.getoption("browser")
    session_data.device_os = request.config.getoption("device_os")
    session_data.os = request.config.getoption("device_os")
    session_data.url = request.config.getoption("appium_input")
    session_data.device = request.config.getoption("device")
    session_data.env = request.config.getoption("env")
    session_data.selenium_url = request.config.getoption("selenium_url")
    session_data.reference =  str(int(round(time.time() * 1000)))
    session_data.session_id = None
    #Logs folder where all the log folders of each runs are stored
    session_data.logs_folder = os.getcwd()+ "/logs"
    if not os.path.exists(session_data.logs_folder):
        os.mkdir(session_data.logs_folder)
    
        

    #If iOS and iPad
    if session_data.device_os.lower() == "ios" :
        session_data.desired_caps = {}
        session_data.desired_caps['platformName'] = 'iOS'
        session_data.desired_caps['automationName'] = 'XCUITest'	
        session_data.desired_caps['autoDismissAlerts'] = True
        session_data.desired_caps['safariIgnoreFraudWarning'] = True
        session_data.desired_caps['udid'] = session_data.udid
        session_data.desired_caps['deviceName'] = session_data.udid
        session_data.desired_caps['browserName']="Safari"
        session_data.desired_caps['noReset'] = True
        #session_data.desired_caps['headspin:controlLock']= True
        session_data.desired_caps['startIWDP']= True
        session_data.driver = AppiumWebdriver.Remote(session_data.appium_input, session_data.desired_caps)
        

    elif session_data.device_os.lower() == "android":
        session_data.desired_caps = {}
        session_data.desired_caps['udid'] = session_data.udid
        session_data.desired_caps['platformName'] = "Android"
        session_data.desired_caps['deviceName'] = session_data.udid
        session_data.desired_caps['browserName'] = "Chrome"
        session_data.desired_caps['browser'] = 'Chrome'
        #session_data.desired_caps['headspin:capture.video']= True
        # session_data.desired_caps['chromedriverExecutable'] = "/Users/jomina/Downloads/chromedriver"
        session_data.desired_caps['chromedriverExecutable'] = "/home/pbox/Documents/HeadSpinAppiumDemo/io/headspin/citi_worthi/chromedriver"
        session_data.driver = AppiumWebdriver.Remote(session_data.appium_input, session_data.desired_caps)

    elif session_data.hs_platform:
        if not session_data.url:
            raise Exception("appium url not found")
        #xplatfrom_runs(session_data)

    else:
        print("!!! Invlaid OS or browser name")

    #Screenshot path
    caps= session_data.desired_capabilities
    session_data.browser_name= caps['browserName']
    session_data.screenshot_name = "{}_{}_{}.png".format(session_data.device_os.lower(), session_data.browser_name, session_data.reference)
    print(session_data.screenshot_name)
    session_data.screenshot_path = session_data.logs_folder+"/"+session_data.screenshot_name

    session_data.log_file_name = "{}_{}_{}.log".format(session_data.device_os.lower(), session_data.browser_name, session_data.reference)
    session_data.log_path = session_data.logs_folder+"/"+ session_data.log_file_name

    #if iphone or ipad, start device log
    if session_data.device_os.lower() == "ios" :
        session_data.process =subprocess.Popen("exec idevicesyslog -u {} > {}".format(session_data.udid, session_data.log_path), shell=True)


    if session_data.device_os.lower() in ['android', 'ios'] and session_data.device.lower() != "ipad" :
        session_data.mobile_device = True
    else:
        session_data.mobile_device = False
    
    if session_data.device_os.lower() == "windows":
        session_data.platform_name = "Windows"

    session_data.username = citi_worthi_data.username
    session_data.password = citi_worthi_data.password
    #session_data.url = citi_worthi_data.url
    #session_data.ngnix_url = citi_worthi_data.ngnix_url
    if session_data.env == "uat" :
        session_data.url = citi_worthi_data.url_uat
    if session_data.env == "staging" :
        session_data.url = citi_worthi_data.url_staging
    if session_data.env == "production" :
        session_data.url = citi_worthi_data.url_prod
    session_data.ngnix_url = citi_worthi_data.ngnix_url

    #Test data
    session_data.first_name = citi_worthi_data.first_name
    session_data.occupation = citi_worthi_data.occupation
    session_data.cities = citi_worthi_data.cities
    session_data.salary_lower_limit = citi_worthi_data.salary_lower_limit
    session_data.salary_upper_limit =  citi_worthi_data.salary_upper_limit
    #session_data.email_id  = uuid.uuid1().hex + "@ymail.com"
    
    session_data.email_id =  citi_worthi_data.email_id

    if session_data.udid =="64c1706421eaee2b3c2cb664743dd1d1f7eb919b":
        session_data.driver.orientation = "LANDSCAPE"
        session_data.driver.get('https://www.google.com')
    

    init_caps(session_data)
    return session_data
    logger.info("launch_fail")

def init_caps(session_data):
            if session_data.browser:
                browser_details = session_data.browser.split("_")
            session_data.browser = browser_details[0]
            auth_tocken = session_data.url.split("/")[4]

            try:
                if browser_details[1] != "system":
                     session_data.browser_version = browser_details[1]
            except:
                session_data.browser_version = None
            session_data.access_token = session_data.url.split('/')[4]
            if 'localhost' in session_data.url or '0.0.0.0' in session_data.url or not session_data.private_key_file:
                session_data.running_on_pbox = True

            session_data.valid_start = True
            session_data.relaunch_start = None
            session_data.data_kpi = None

            session_data.desired_caps = {}
            if session_data.browser.lower() == "chrome":
                session_data.desired_caps['browserName'] = "chrome"
                session_data.desired_caps['chromeOptions'] = {'w3c' : False}
                if session_data.os.lower()=="mac" or session_data.os.lower()=="debian":
                        session_data.desired_caps['browserVersion']= session_data.browser_version
            elif session_data.browser.lower() == "firefox":
                session_data.desired_caps['browserName'] = "firefox"
                if session_data.os.lower()=="mac" or session_data.os.lower()=="debian":
                        session_data.desired_caps['browserVersion']= session_data.browser_version
            elif session_data.browser.lower() == "safari" :
                session_data.desired_caps['browserName'] = "safari"
                session_data.desired_caps['browserVersion']= session_data.browser_version
            elif  session_data.browser.lower() == "edge":
                session_data.desired_caps['browserName'] = "MicrosoftEdge"
            else:
                raise Exception("DesiredCaps error")

            if session_data.use_capture:
                if session_data.video_only:
                     session_data.desired_caps['headspin:capture.video'] = True
                     session_data.desired_caps['headspin:capture.network'] = False
                else:
                     session_data.desired_caps['headspin:capture.video'] = True
                     session_data.desired_caps['headspin:capture.network'] = True

            print(session_data.desired_caps)
            session_data.driver = webdriver.Remote(session_data.url, session_data.desired_caps)
            session_data.driver.maximize_window()
            if not session_data.device_os or session_data.browser:
                session_data.print_help()
                example_args = [' ']
                example_args.append('--udid <udid>')
                example_args.append('--device_os <debian/ios/windows>')
                example_args.append('--browser <chrome/safari/edge/ie>')


