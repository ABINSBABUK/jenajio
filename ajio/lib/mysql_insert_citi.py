from __future__ import absolute_import
from __future__ import print_function
import sys
import mysql.connector
import six.moves.configparser
# from .device_info import deviceInfo 
import socket
from datetime import datetime

class MysqlDataInsert:
        
        host_name= socket.gethostname()
 
        def read_config(self):
                
                db_config = six.moves.configparser.RawConfigParser()
                db_config.read('../setup/py_modules_citi/db.properties')
                db={}
                db_user = db_config.get('DB_Config', 'username')
                db_pass = db_config.get('DB_Config', 'password')
                db_name = db_config.get('DB_Config', 'database')
                db_host = db_config.get('DB_Config', 'host')
                self.CITY= db_config.get('DB_Config', 'city')

                db['user'] = str(db_user)
                db['pass'] = str(db_pass)
                db['host'] = str(db_host)
                db['name'] = str(db_name)

                return db

        def cursor_init(self,driver):

                #get info from sessionid (driver)
                caps= driver.desired_capabilities
                try:
                        self.udid= caps['udid']
                        is_desktop_test= False
                except:
                        self.udid= None
                        is_desktop_test= True

                try:
                        self.os= caps['platformName']
                except:
                        self.os= caps['platform']

                if self.os=="Android":
                        try:
                                self.package= caps['appPackage']
                        except:
                                self.package=None
                                self.browser_name= caps['browserName']
                elif self.os=="iOS":
                        try:
                                self.package= caps['bundleId']
                                self.browser_name= caps['browserName']
                        except:
                                self.package= None
                                self.browser_name= caps['browserName']
                else:
                        self.browser_name= caps['browserName']

                self.session_id=driver.session_id
                #Device info
                self.device_os_version= ""
                self.device_model= ""
                self.device_network= ""
                self.app_version= ""
                if self.udid is not None:
                        phoneInfo=deviceInfo()
                        self.device_os_version= phoneInfo.get_os_version(self.udid,self.os)
                        self.device_model= phoneInfo.get_device_model(self.udid,self.os)
                        self.device_network= phoneInfo.get_network_name(self.udid,self.os)      
                        if self.package is not None:
                                self.app_version= phoneInfo.get_app_version(self.udid,self.os,self.package)
                        else:
                                self.app_version= None

                if is_desktop_test:
                        try:
                                self.device_model= caps['platform']
                                self.device_os_version= caps['version']
                        except:
                                self.device_model= caps['platformName']

                db= self.read_config()

                self.cnx = mysql.connector.connect(user=str(db['user']),password=str(db['pass']), host=str(db['host']),database=str(db['name']))


        def citi_venture_browse_funds_metrics(self, driver, citi_investment_focus_filter_time, citi_investment_focus_filter_status, citi_total_fund_size_filter_time, citi_total_fund_size_filter_status, citi_min_investment_filter_time, citi_min_investment_filter_status, pass_count,fail_count,status_of_run,reference_key,session_id):

                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                cursor.execute('''INSERT INTO citi_venture_browse_funds_metrics( citi_investment_focus_filter_time, citi_investment_focus_filter_status, citi_total_fund_size_filter_time, citi_total_fund_size_filter_status, citi_min_investment_filter_time, citi_min_investment_filter_status, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count,fail_count,session_id) VALUES ( %s, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s,%s)''', (citi_investment_focus_filter_time, citi_investment_focus_filter_status, citi_total_fund_size_filter_time, citi_total_fund_size_filter_status, citi_min_investment_filter_time, citi_min_investment_filter_status, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(session_id)))

                self.cnx.commit()
                cursor.close()
                self.cnx.close()
        

        def citi_venture_explore_zones_metrics(self, driver, citi_map_load_time, citi_zone_page_load_time, citi_zone_compare_time, pass_count,fail_count,status_of_run,reference_key,session_id):

                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                cursor.execute('''INSERT INTO citi_venture_explore_zones_metrics( citi_map_load_time, citi_zone_page_load_time, citi_zone_compare_time, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count,fail_count,session_id) VALUES ( %s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s,%s)''', (citi_map_load_time, citi_zone_page_load_time, citi_zone_compare_time, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(session_id)))

                self.cnx.commit()
                cursor.close()
                self.cnx.close()

        def citi_venture_page_impact_metrics(self, driver, impact_array, pass_count, fail_count, status_of_run,reference_key,session_id):
                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                for impact_dic in impact_array:
                        page_url = impact_dic['page'] 
                        impact = impact_dic['impact']
                        target = impact_dic['target']
                        cursor.execute('''INSERT INTO citi_venture_page_impact_metrics( page_url, impact, target, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count,fail_count,session_id) VALUES ( %s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s,%s)''', (page_url, impact, target, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(session_id)))
                        self.cnx.commit()
                cursor.close()
                self.cnx.close() 

        def eikon_browser_tests(self, driver, eikon_launch_time, eikon_login_time, eikon_search_time, pass_count,fail_count,status_of_run,reference_key,session_id):

                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                cursor.execute('''INSERT INTO eikon_browser_tests( eikon_launch_time,eikon_login_time, eikon_search_time, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count,fail_count,session_id) VALUES ( %s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s,%s)''', (eikon_launch_time, eikon_login_time, eikon_search_time, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(session_id)))

                self.cnx.commit()
                cursor.close()
                self.cnx.close()

        def citi_worthi_grow_metrics(self, driver, citi_home_page_time, citi_salary_compare_time, citi_skill_load_time, citi_resources_time, pass_count, fail_count, status_of_run, reference_key, env, session_id,session_url):
                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                cursor.execute('''INSERT INTO citi_worthi_grow_metrics( citi_home_page_time, citi_salary_compare_time, citi_skill_load_time, citi_resources_time, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count, fail_count, env, session_id,session_url) VALUES ( %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (citi_home_page_time, citi_salary_compare_time, citi_skill_load_time, citi_resources_time, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(env),str(session_id),str(session_url)))

                self.cnx.commit()
                cursor.close()
                self.cnx.close()
        
        def citi_worthi_explore_roles_metrics(self, driver, citi_home_page_time, citi_salary_compare_time, citi_skill_inventory_time, citi_recommended_roles_time, citi_roles_view_time, pass_count, fail_count, status_of_run, reference_key, env, session_id,session_url):
                self.cursor_init(driver)
                print(self.CITY,self.host_name)

                cursor = self.cnx.cursor()
                cursor.execute('''INSERT INTO citi_worthi_explore_roles_metrics( citi_home_page_time, citi_salary_compare_time, citi_skill_inventory_time, citi_recommended_roles_time, citi_roles_view_time, browser, machine, udid, device_model, device_os_version,status_of_run,city,reference,network_type,os_type ,pass_count, fail_count, env, session_id,session_url) VALUES ( %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (citi_home_page_time, citi_salary_compare_time, citi_skill_inventory_time, citi_recommended_roles_time, citi_roles_view_time, self.browser_name, str(self.host_name) , str(self.udid), str(self.device_model), str(self.device_os_version),str(status_of_run),self.CITY,str(reference_key),str(self.device_network),str(self.os),str(pass_count),str(fail_count),str(env),str(session_id),str(session_url)))

                self.cnx.commit()
                cursor.close()
                self.cnx.close()
