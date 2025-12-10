import os
import urllib.request as urll
import json
try:
    while True:
        ip = input("what is your target ip?")
        url="http://ip-api.com/json/"
        response=urll.urlopen(url + ip)
        data = response.read()
        values = json.loads (data)
        
        print("Ip :" + values["query"])
        print("City :" + values["city"])
        print("ISP :" + values["isp"])
        print("Country :" + values["country"])
        print("Region :" + values["region"])
        print("TimeZone :" + values["timezone"])
        break
except :
    print("Error")
    print("Please check your internet connection")
    pass