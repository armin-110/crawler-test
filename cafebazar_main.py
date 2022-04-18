print('بسمه الله الرحمن الرحیم')
print('salam bar mohammadreza dehghan amiri')
import datetime
from sqlalchemy import create_engine
import schedule
import itertools
import time
from iteration_utilities import unique_everseen
from collections import OrderedDict
import requests
from copy import deepcopy
import copy
import json
import re
from bs2json import bs2json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as b
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from rich import print
from curses import COLOR_BLACK
import cafebazar_get_more_link
import cafebazar_categori_name
import cafebazar_cat_link_extractor
import cafebazar_get_meta
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import scrapy
######################################################################
date_a=datetime.datetime.now()


def get_cat_link_name(page_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    sg = cafebazar_categori_name.GETCATEGORI(page_link, driver)
    sgg = sg.get_cat_link_name()
    driver.close()
    return(cafebazar_categori_name.cat_link_name_list)


def get_total_links(page_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = cafebazar_get_more_link.Getmorelinks(driver, page_link)
    gf.get_link()
    driver.close()
    return (cafebazar_get_more_link.total_link)

def get_categori_links(cat_link):
    gf = cafebazar_cat_link_extractor.Getcatlinks(cat_link)
    gf.get_cat_link()
    return (cafebazar_cat_link_extractor.cat_link_list_out)    


def get_metadata(content_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = cafebazar_get_meta.Getmeta(driver, content_link)
    gf.get_meta()
    driver.close()
    return (cafebazar_get_meta.meta_list)

#######################################################################
engine = create_engine('postgresql://postgres:12344321@10.32.141.17/cafebazar',pool_size=20, max_overflow=100,)
con=engine.connect()


cat_program=get_cat_link_name('https://cafebazaar.ir/pages/list~app-category~app-categories')
cat_link=cat_program[0]
cat_name=cat_program[1]
cat_game=get_cat_link_name('https://cafebazaar.ir/pages/list~app-category~game-categories')
cat_game_link=cat_game[0]
cat_game_name=cat_game[1]
print(cat_game[0])
for j in range(len(cat_link)):
    uniqe_categori_links=get_categori_links(cat_link[j])
    for i in range(len(uniqe_categori_links[0])):
        link_meta=get_metadata(uniqe_categori_links[0][i])
        date_i=datetime.datetime.now()
        link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
        link_meta[0]['categori_name']=cat_name[j]
        data_frame =pd.DataFrame(link_meta[0],index=[0])
        data_frame.to_sql('cafebazar_meta'+str(date_a.date()).replace('-','')+str(date_a.time()).split(':')[0],con,if_exists='append', index=False)
        print(link_meta[0])

for j in range(len(cat_game_link)):
    uniqe_categori_links=get_categori_links(cat_game_link[j])
    for i in range(len(uniqe_categori_links[0])):
        link_meta=get_metadata(uniqe_categori_links[0][i])
        date_i=datetime.datetime.now()
        link_meta[0]['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
        link_meta[0]['categori_name']=cat_game_name[j]
        data_frame =pd.DataFrame(link_meta[0],index=[0])
        data_frame.to_sql('cafebazar_meta'+str(date_a.date()).replace('-','')+str(date_a.time()).split(':')[0],con,if_exists='append', index=False)
        print(link_meta[0])
# print(get_metadata('https://cafebazaar.ir/app/com.pishtaz_ht.salad')) 



