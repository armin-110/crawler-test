from curses import COLOR_BLACK
from rich import print
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
import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
import datetime
import scrapy
meta_list=[]
class Getmeta():
    def __init__ (self,driver,content_link):
        self.driver=driver
        self.content_link=content_link
    def get_meta(self):
        meta_list.clear()
   
        # try:
        try:
            self.driver.get(self.content_link)
            self.driver.refresh()
        except:
            try:
                time.sleep(3)
                self.driver.get(self.content_link)
                self.driver.refresh()
            except:
                time.sleep(3)
                self.driver.get(self.content_link)
                self.driver.refresh()

        converter = bs2json()
        # self.driver.get(self.page_link)

        try:
            fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/section')))
        except:
            fb= WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/section')))
        
        meta_dic = {'categori_name':'','content_name': '','content_link':self.content_link,'rate':'','ratings':'','Size':'','Installs':'','Current Version':'','crawling_date':''}
        html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
        html_soup=b(html,'html.parser')
        converter = bs2json()
        class_find=html_soup.findAll('h1',{'class':'AppName fs-20'})
        json_class_find = converter.convertAll(class_find)
        print(json_class_find[0]['text'])#title
        meta_dic['content_name']=json_class_find[0]['text']
        ############################################
        try:
            class_find=html_soup.findAll('div',{'class':'fs-12 AppSubtitles__item AppSubtitles__item--clickable'})
            json_class_find = converter.convertAll(class_find)
            print(json_class_find)
            print(json_class_find[0]['text'])#version
            meta_dic['Current Version']=json_class_find[0]['text']
        except:
            try:
                class_find=html_soup.findAll('div',{'class':'fs-12 AppSubtitles__item'})
                json_class_find = converter.convertAll(class_find)
                print(json_class_find)
                print(json_class_find[0]['text'])#version
                meta_dic['Current Version']=json_class_find[0]['text']
            except:
                pass

       
        ################################################InfoCube__content fs-14
        class_find=html_soup.findAll('dl',{'class':'InfoCubes'})
        json_class_find = converter.convertAll(class_find)
       
        print(len(json_class_find))
        print(json_class_find[0]['div'][0]['dd']['text'])#install
        meta_dic['Installs']=json_class_find[0]['div'][0]['dd']['text']
        print(json_class_find[0]['div'][1]['dd']['div']['text'])#rate
        meta_dic['rate']=json_class_find[0]['div'][1]['dd']['div']['text']
        pattern = '[،أا-ی]'
        print(re.sub(pattern,'', json_class_find[0]['div'][1]['dt']['text']).strip())#ratings
        meta_dic['ratings']=re.sub(pattern,'', json_class_find[0]['div'][1]['dt']['text']).strip()
        try:
            print(json_class_find[0]['div'][2]['dd']['text'])#size
            meta_dic['Size']=json_class_find[0]['div'][2]['dd']['text']
        except:
            pass    
        #####################################################
        meta_list.append(meta_dic)