from __future__ import absolute_import
from __future__ import print_function
import time
from hs_api import hsApi


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
    parser.addoption('--os', '--os', dest='os',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="os")
    parser.addoption('--use_capture', '--use_capture', dest='use_capture',
                        type=str, nargs='?',
                        default="",
                        required=False,
                        help="use_capture")
    parser.addoption('--video_only', '--video_only', dest='video_only',
                        type=str, nargs='?',
                        default="true",
                        required=False,
                        help="video_only")
    parser.addoption('--control_lock', '--control_lock', dest='control_lock',
                        type=str, nargs='?',
                        default="",
                        required=False,
                        help="control_lock")


def init_args(request, session_data):
    session_data.udid = request.config.getoption("udid")
    session_data.use_capture = True if request.config.getoption("use_capture").lower()=="true" else False
    session_data.video_only = True if request.config.getoption("video_only").lower()=="true" else False
    session_data.control_lock = True if request.config.getoption("control_lock").lower()=="true" else False
    session_data.appium_input = request.config.getoption("appium_input")
    session_data.os = request.config.getoption("os")
    session_data.access_token = session_data.appium_input.split('/')[4]
    
    init_caps(session_data)

    return session_data  


def init_caps(session_data):
    # desired caps for the app
    session_data.desired_caps = {}
    session_data.desired_caps['platformName'] = session_data.os
    session_data.desired_caps['udid'] = session_data.udid
    session_data.desired_caps['deviceName'] = session_data.udid
    session_data.desired_caps['newCommandTimeout'] = 50000
    session_data.desired_caps['autoLaunch']=False

    # Android specific caps
    #session_data.os = "Android"
    if session_data.os.lower() == "android":
        session_data.desired_caps['appPackage'] = session_data.package
        session_data.desired_caps['appActivity'] = session_data.activity
        session_data.desired_caps['disableWindowAnimation'] = True
        session_data.desired_caps['unlockType'] = "pin"
        session_data.desired_caps['unlockKey'] = "1234"
        session_data.desired_caps['automationName'] = "UiAutomator2"

    # iOS spedific caps
    elif session_data.os.lower() == "ios":
        session_data.desired_caps['automationName'] = "XCUITest"
        try:
            session_data.package = session_data.bundle_id
        except: pass
        session_data.desired_caps['bundleId'] = session_data.package

    # Headspin caps
    
    session_data.desired_caps['headspin:controlLock'] = False
    if session_data.use_capture:
        if session_data.video_only:
            session_data.desired_caps['headspin:capture.video'] = True
            session_data.desired_caps['headspin:capture.network'] = False
        else:
            session_data.desired_caps['headspin:capture.video'] = True
            session_data.desired_caps['headspin:capture.network'] = True
            
    return session_data
