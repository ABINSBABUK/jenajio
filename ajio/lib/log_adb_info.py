from __future__ import absolute_import
from __future__ import print_function
import sh
import sys
import os
from time import sleep
import subprocess
import boto3
 
class AdbDdata:


        # adb_comm= sh.Command('adb')
        # cut_comm = sh.Command('cut')
        # grep_comm = sh.Command('grep')
        # head_comm = sh.Command('head')

        
        def before_test(self,device_id):
                #Clear log cat
                self.adb_comm('-s', device_id, 'logcat' , '-c')
                sleep (5)
                
                #Get device temperature
                current_tem= self.get_device_temp(device_id)
                
                return [current_tem]

        def after_test(self, device_id, timestamp, driver, status, *argv):
                path=os.getcwd()+ "/logs/"
                print(path)

                if status == "Pass":
                        screenshot_name = str(timestamp)+'_'+device_id +".png"
                        screenshot_path = path+"/"+screenshot_name

                        log_file_name = str(timestamp)+'_'+device_id + ".log"
                        log_path = path+"/"+ log_file_name
                else:
                        screenshot_name = "{}_{}_error.png".format(str(timestamp), device_id)
                        screenshot_path = path+"/"+screenshot_name

                        log_file_name = "{}_{}_error.log".format(str(timestamp), device_id)
                        log_path = path+"/"+ log_file_name

                try:
                        if driver.desired_capabilities['platformName']== "Android":
                                print("adb -s " + device_id + " logcat -d  > " +  log_path)
                                subprocess.call("adb -s " + device_id + " logcat -d  > " + log_path, shell=True)
                except:
                        pass
                
                #Screenshot
                driver.save_screenshot(screenshot_path) 

                #argv[0] is boolean for AWS push
                if argv[0]:
                        aws_folder= argv[1]
                        #AWS push
                        s3 = boto3.resource('s3')
                        s3.meta.client.upload_file(screenshot_path, 'grafana-images.headspin.io',aws_folder+'/'+screenshot_name)                
                        try:
                                driver.desired_capabilities['udid']
                                s3.meta.client.upload_file(log_path, 'grafana-images.headspin.io',aws_folder+'/'+log_file_name) 
                        except:
                                pass
                        print("Pushed to AWS")

                if status!="Pass":
                        f = open(str(timestamp)+'_'+device_id+'.xml', 'w')
                        f.write(driver.page_source.encode('utf-8'))

                
        def get_device_temp(self,device_id):

                self.batt_temp = str(self.grep_comm(self.adb_comm('-s', device_id, 'shell', 'dumpsys', 'battery'), "temperature"))
                self.batt_temp = self.batt_temp.split(':')[1].strip()
                return self.batt_temp

        def get_dumpsys(self,device_id,reference, step,path):

                file_name= path+"/"+ "dumpsys_"+step+".log"
                subprocess.call("adb -s " + device_id + " shell dumpsys  > " +  file_name , shell=True)         
                sleep (5)

        def get_cpuinfo(self,device_id):
                
                if not os.path.exists('dumpsys.txt'):
                        open("dumpsys.txt", "w+")
                subprocess.call("adb -s " + device_id + " shell dumpsys cpuinfo > dumpsys.txt", shell=True)
                with open("dumpsys.txt", "r+") as f:
                        for line in iter(f.readline, ''):
                                if "TOTAL" in str(line):
                                        cpu_usage= line.strip()
                                        f.truncate(0)
                                        break
                result= cpu_usage.split(" ")[0].split("%")[0].strip()
                return result


        def get_mem_info(self,device_id, package):

                if not os.path.exists('dumpsys.txt'):
                        open("dumpsys.txt", "w+")
                subprocess.call("adb -s " + device_id + " shell dumpsys meminfo "+ " > dumpsys.txt", shell=True)
                with open("dumpsys.txt", "r+") as f:
                        for line in iter(f.readline, ''):
                                if "No process found" in str(line):
                                        print("Application not running. No Memory info available") 
                                        return None     
                                
                                if "Used RAM: " in str(line):
                                        mem_usage= line.strip()
                                        f.truncate(0)
                                        break
                result= mem_usage.split("Used RAM: ")[1].split('K')[0].strip().replace(',', "") 
                return result

        def get_rsrp(self,device_id):
                
                print("RF Details")
                rf = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'telephony.registry'), "mSignalStrength"), '-n1'))
                self.rsrp = rf.split("mSignalStrength=SignalStrength: ")[1].split()[8]
                
                print("RSRP")
                print(self.rsrp)
                return self.rsrp 

        def get_rsrq(self,device_id):

                rf = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'telephony.registry'), "mSignalStrength"), '-n1'))
                self.rsrq = rf.split("mSignalStrength=SignalStrength: ")[1].split()[9]
                print("RSRQ")
                print(self.rsrq)
                return self.rsrq
        
        def get_ssnr(self,device_id):
        
                rf = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'telephony.registry'), "mSignalStrength"), '-n1'))
                self.ssnr = rf.split("mSignalStrength=SignalStrength: ")[1].split()[7]
                print("SSNR")
                print(self.ssnr)
                return self.ssnr

        def get_cqi(self,device_id):

                rf = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'telephony.registry'), "mSignalStrength"), '-n1'))
                self.cqi = rf.split("mSignalStrength=SignalStrength: ")[1].split()[10]
                print("CQI")
                print(self.cqi)
                return self.cqi

        def get_lat(self,device_id):
        
                print("GPS DATA")
                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        for data in gps_data:
                                if  "," in data and "." in data:
        
                                        self.lat = data.split(",")[0]
                                        print("Lat: ")
                                        print(self.lat)
                                        break
                except:
                        self.lat= None
                return self.lat

        def get_lon(self,device_id):
                
                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        for data in gps_data:
                                if  "," in data and "." in data:
                                        self.lon = data.split(",")[1]
                                        print("Lon: ")
                                        print(self.lon)
                                        break
                except:
                        self.lon= None
                return self.lon
        
        def get_et(self,device_id):
        
                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        self.et ="0"
                        for data in gps_data:
                                if "et=" in data:
                                        print("ET: ")
                                        self.et = data.split("=")[1]
                                        print(self.et)
                                        break
                except:
                        self.et= None
                return self.et

        def get_vel(self,device_id):
                
                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        self.velocity ="0"
                        for data in gps_data:
                                if "vel" in data:
                                        print("Velocity: ")
                                        self.velocity = data.split("=")[1]
                                        print(self.velocity)
                                        break
                except:
                        self.velocity= None
                return self.velocity
        
        def get_alt(self,device_id):

                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        self.altitude = "0"
                        for data in gps_data:
                                if "alt" in data:
                                        print("Alt: ")
                                        self.altitude = data.split("=")[1]
                                        print(self.altitude)
                                        break
                except:
                        self.altitude= None
                return self.altitude

        def get_acc(self,device_id):
                
                try:
                        device_lat = str(self.head_comm(self.grep_comm(self.adb_comm('-s',device_id,'shell', 'dumpsys', 'location'), "network: Location"), '-n1'))
                        gps_data = device_lat.split(" ")
                        self.accuracy = "0"
                        for data in gps_data:
                                if "acc" in data:
                                        print("Acc: ")
                                        self.accuracy = data.split("=")[1]
                                        print(self.accuracy)
                                        break
                except:
                        self.accuracy= None
                return self.accuracy
                





