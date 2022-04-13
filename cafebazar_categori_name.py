from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import pandas as pd
import numpy as np
from bs2json import bs2json
import re
import json
import copy
from copy import deepcopy
import requests
from collections import OrderedDict
from iteration_utilities import unique_everseen
import time
import itertools
cat_link_name_list=[]
class GETCATEGORI():
    def __init__ (self,page_link,driver):
        self.page_link =page_link
        self.driver=driver
        ##################################################################################
    def get_cat_link_name(self):
        cat_link_name_list.clear()
        self.driver.get(self.page_link) 
        

        fb= WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/section/div')))
       
        html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
        page_html_soup=b(html,'html.parser')
        converter = bs2json() 
        # print(page_html_soup)
        class_find_name= page_html_soup.findAll('a',{'class':'CategoryItem padding-h'}) 
        # print(class_find_name)        
        json_class_find_name = converter.convertAll(class_find_name)
        print(len(json_class_find_name))
        print(json_class_find_name[0]['attributes']['href'])#link
        print(json_class_find_name[0]['attributes']['title'])#name
        # time.sleep(1000)
        
        categori_link_list=[]
        categori_name_list=[]

        for i in range(len(json_class_find_name)):
            categori_link_list.append('https://cafebazaar.ir'+json_class_find_name[i]['attributes']['href'])
            categori_name_list.append(json_class_find_name[i]['attributes']['title'])
        
        cat_link_name_list.append(categori_link_list)
        cat_link_name_list.append(categori_name_list)
        # # print(categori_link_list)
        # # print(categori_name_list)