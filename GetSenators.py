#! /usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests as rq

url = "https://www.senate.gov/general/contact_information/senators_cfm.cfm"
r = rq.get(url)
soup = BeautifulSoup(r.text,'xml')

senators = soup.findAll('div')

for senator in senators:
    print(senator)
