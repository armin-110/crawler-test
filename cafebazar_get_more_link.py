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
total_link=[]
more_link_list=[]
content_link_list=[]
pagination_link_list=[]
class Getmorelinks():
    def __init__ (self,driver,page_link):
        self.driver=driver
        self.page_link=page_link
    def get_link(self):
        
        total_link.clear()
        more_link_list.clear()
        content_link_list.clear()
        pagination_link_list.clear()
        # try:
        try:
            self.driver.get(self.page_link)
            self.driver.refresh()
        except:
            try:
                time.sleep(3)
                self.driver.get(self.page_link)
                self.driver.refresh()
            except:
                time.sleep(3)
                self.driver.get(self.page_link)
                self.driver.refresh()

        converter = bs2json()
        # self.driver.get(self.page_link)

        SCROLL_PAUSE_TIME = 4
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        start1=time.time()
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_time=time.time()-start1
            print(scroll_time)
                # if scroll_time >40:
                #     print('scroll time finshed')
                #     break
        #
        try:
            fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]')))
        except:
            fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]')))

        html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
        html_soup=b(html,'html.parser')
        converter = bs2json()
        #############################################################################################################
        try:
            class_find=html_soup.findAll('a',{'class':'SimpleAppItem SimpleAppItem--carousel'})
            json_class_find = converter.convertAll(class_find)
            
            # print(json_class_find[0]['attributes']['href'])###content link
        except:
            class_find=html_soup.findAll('a',{'class':'SimpleAppItem SimpleAppItem--single'})
            json_class_find = converter.convertAll(class_find)
        if len(json_class_find)==0:
            try:
                class_find=html_soup.findAll('a',{'class':'SimpleAppItem SimpleAppItem--single'})
                json_class_find = converter.convertAll(class_find)
            except:
                pass    

            # print(json_class_find[0]['attributes']['href'])###content link
        for i in range(len(json_class_find)):
        #    print(json_class_find[i]['attributes']['href'])
           content_link_list.append('https://cafebazaar.ir'+json_class_find[i]['attributes']['href'])
        total_link.append(content_link_list)
        ##############################################################################################################
        try:
            class_find=html_soup.findAll('a',{'class':'ExpandInfo fs-14'})
            json_class_find = converter.convertAll(class_find)
            # print(json_class_find[0]['attributes']['href'])####more link
            # print(len(json_class_find))
            for i in range(len(json_class_find)):
            #    print(json_class_find[i]['attributes']['href'])
                more_link_list.append('https://cafebazaar.ir'+json_class_find[i]['attributes']['href'])
        except:
            pass
        
        total_link.append(more_link_list)
        ################################################################################################################
        try:
            class_find=html_soup.findAll('a',{'class':'Pagination__link link-active'})
            json_class_find = converter.convertAll(class_find)
            # print(json_class_find[0]['attributes']['href'])# pagination link
            # print(json_class_find[0]['text'])
            for i in range(len(json_class_find)):
                if json_class_find[i]['text']=='صفحه بعدی':
                    # print('salam bar hossein')
                    # print(json_class_find[0]['attributes']['href'])
                    pagination_link_list.append('https://cafebazaar.ir'+json_class_find[i]['attributes']['href']) 
            total_link.append(pagination_link_list)
        except:
            total_link.append([])

        # print(total_link)
        # except:
        #     print('more link not found')