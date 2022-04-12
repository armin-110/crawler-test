import cafebazar_get_more_link
import cafebazar_categori_name
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

def get_total_links(page_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = cafebazar_get_more_link.Getmorelinks(driver, page_link)
    gf.get_link()
    driver.close()
    return (cafebazar_get_more_link.total_link)
        
import psycopg2
import pandas.io.sql as psql
cat_link_list_out=[]
def uniq_function():
    cat_link_list_out.clear()
    connection = psycopg2.connect(user="postgres",
                                    password="12344321",
                                    host="10.32.141.17",
                                    port="5432",
                                    database="cafebazar")
    cursor = connection.cursor()

    df= psql.read_sql("SELECT * FROM public.cafebazar_content_link", connection)
# Execute the drop table command
    cursor.execute("DELETE FROM public.cafebazar_content_link")
    connection.commit()
    if connection:
        cursor.close()
        connection.close()
    df.drop_duplicates(subset =["content_link"],
                        keep = 'last', inplace = True)
    cat_link_list = list(itertools.chain(*df.iloc[:, [0]].values.tolist()))
    cat_link_list_out.append(cat_link_list)

class Getcatlinks():
    def __init__ (self,cat_link):
        self.cat_link=cat_link
    def get_cat_link(self): 
        engine = create_engine('postgresql://postgres:12344321@10.32.141.17/cafebazar', pool_size=20, max_overflow=100,)
        con = engine.connect()

        connection1 = psycopg2.connect(user="postgres",
                                    password="12344321",
                                    host="10.32.141.17",
                                    port="5432",
                                    database="cafebazar")
        cursor1 = connection1.cursor()
        pagination_link0=[self.cat_link]
        # pagination_link0=['https://cafebazaar.ir/cat/tools?o=25']
        while True:
            total_link_list0 = get_total_links(pagination_link0[0])
            content_link0 = total_link_list0[0]
            availble_more_link0 = total_link_list0[1]
            pagination_link0 = total_link_list0[2]
            # print(pagination_link0)
            # print(len(pagination_link0))
            df = pd.DataFrame(content_link0, columns=['content_link'])
            df.to_sql('cafebazar_content_link', con, if_exists='append', index=False)
            df = pd.DataFrame(availble_more_link0, columns=['availble_more_link'])
            df.to_sql('cafebazar_availble_more_link', con,
                    if_exists='replace', index=False)
            df = pd.DataFrame(pagination_link0, columns=['pagination_link0'])
            df.to_sql('cafebazar_pagination_link0', con,
                    if_exists='replace', index=False)
            connection1 = psycopg2.connect(user="postgres",
                                    password="12344321",
                                    host="10.32.141.17",
                                    port="5432",
                                    database="cafebazar")
            cursor1 = connection1.cursor()
            df = psql.read_sql("SELECT * FROM public.cafebazar_availble_more_link", connection1)

            availble_more_link0 = list(itertools.chain(*df.iloc[:, [0]].values.tolist()))
            # print(availble_more_link0)
            df1 = psql.read_sql("SELECT * FROM public.cafebazar_pagination_link0", connection1)
            pagination_link0= list(itertools.chain(*df1.iloc[:, [0]].values.tolist()))
            # print(pagination_link0)
            if connection1:
                cursor1.close()
                connection1.close()

            if len(availble_more_link0) > 0:
                for i in range(len(availble_more_link0)):
                    # print(availble_more_link0[i])
                    total_link_list1 = get_total_links(availble_more_link0[i])
                    # print(total_link_list1)
                    content_link1 = total_link_list1[0]
                    # print(content_link1)
                    # availble_more_link0=total_link_list[1]
                    pagination_link_list1 = total_link_list1[2]
                    df = pd.DataFrame(content_link1, columns=['content_link'])
                    df.to_sql('cafebazar_content_link', con,
                            if_exists='append', index=False)
                    if len(pagination_link_list1) > 0:
                        while True:
                            total_link_list2 = get_total_links(pagination_link_list1[0])
                            content_link2 = total_link_list2[0]
                            availble_more_link2 = total_link_list2[1]
                            pagination_link_list2 = total_link_list2[2]
                            df = pd.DataFrame(content_link2, columns=['content_link'])
                            df.to_sql('cafebazar_content_link', con,
                                    if_exists='append', index=False)
                            if len(pagination_link_list2) == 0:
                                break
            # print(pagination_link0)
            # print(len(pagination_link0))
            if len(pagination_link0)==0:
                break   
        uniq_function()