#!/bin/sh
# 
for n in {1..7}; 
do 
    pytest tests/sam_test.py --html=report.html --self-contained-html --udid RZ8M2334ZAV --appium_input https://dev-in-blr-0.headspin.io:7015/v0/9685e6e54dbb435388e0053412046c0a/wd/hub --os android --use_capture true --video_only false -s -v
    echo $n runs  completed
    sleep 900
done
