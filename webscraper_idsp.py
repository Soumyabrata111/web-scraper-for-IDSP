# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:59:48 2019

@author: soumy
"""
import ssl; ssl._create_default_https_context = ssl._create_unverified_context
import wget

from urllib import request

from bs4 import BeautifulSoup

import re
import os


# connect to website and get list of all pdfs
url="https://idsp.nic.in/index4.php?lang=1&level=0&linkid=406&lid=3689"
response = request.urlopen(url).read()
soup= BeautifulSoup(response, "html.parser")     
links = soup.find_all('a', href=re.compile(r'(.pdf)'))


# clean the pdf link names
url_list = []
for el in links:
    url_list.append(el['href'])
    

print(url_list)


# download the pdfs to a specified location
for url in url_list[0:37]: #Change the range as per your wish
    print(url)
    folder_location = r'D:\webscraping_idsp_2019'
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    fullfilename = os.path.join('D:\webscraping_idsp_2019', url.replace("https://idsp.nic.in/index4.php?lang=1&level=0&linkid=406&lid=3689", ""))
    wget.download(url, 'D:\webscraping_idsp_2019')
    
