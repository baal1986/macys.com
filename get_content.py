import requests
import os
from bs4 import BeautifulSoup
import re
import time
import ast

from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.proxy import Proxy, ProxyType



def ParsNoKupon(data, proc) :
    soup = BeautifulSoup(data, features="lxml")
    link_list = soup.findAll('li', {'class': ['cell productThumbnailItem']})


    for i in link_list :
        link_ref = i.find('a').get('href')
        
        
        old_price = i.find('div', {'class': 'prices'})
        old_price = str(old_price)
        old_price = re.findall('\$.*\.[0-9][0-9]' , old_price)
        
        try :
            old_price[0] = re.sub( r'(\$)|(,)', '', old_price[0])
        except IndexError :
            continue
        
        try :
            old_price[1] = re.sub( r'(\$)|(,)', '', old_price[1])
        except IndexError :
            continue
        if( old_price[0] == 0 or old_price[1] == 0 ) :
            old_price[0] == 1
            old_price[1] == 1
            
        sale = (1- (float(old_price[1]) / float(old_price[0])))*100
        
        
        if( sale >= proc ) :
            with open('discont_today_macys.txt', 'a+') as output_file:
                print(sale, file=output_file)
                print(link_ref, file=output_file)
                print("\n\n", file=output_file)


def ParsWithKupon(data, proc) :
    #url = 'https://www.macys.com/shop/featured/' + brand + '/Special_offers,Pageindex/Offer%20code%20PRES,'+ str(page)
    
    soup = BeautifulSoup(data, features="lxml")
    link_list = soup.findAll('li', {'class': ['cell productThumbnailItem']})
    

    for i in link_list :
        link_ref = i.find('a').get('href')
        
        
        old_price = i.find('span', {'class': 'regular originalOrRegularPriceOnSale'})
        old_price = str(old_price)
        
        
        old_price = re.findall('\$.*\.[0-9][0-9]' , old_price) 
        
        
        try :
            old_price[0] = re.sub( r'(\$)|(,)', '', old_price[0])
        except IndexError :
            continue
        
        if( old_price[0] == 0 ) :
            old_price[0] == 1
            
            
        
        new_price = i.find('span', {'data-auto': 'final-price'})
        new_price = str(new_price)
        new_price = re.findall('\$.*\.[0-9][0-9] ' , new_price)
        
        try :
            new_price[0] = re.sub( r'(\$)|(,)', '', new_price[0])
        except IndexError :
            continue
        
        if( new_price[0] == 0 ) :
            new_price[0] == 1
    
        sale = (1- (float(new_price[0]) / float(old_price[0])))*100
        
        
        if( sale >= proc ) :
            with open('coupone_today_macys.txt', 'a+') as output_file:
                print(sale, file=output_file)
                print('https://www.macys.com' + link_ref, file=output_file)
                print("\n\n", file=output_file)
        
        
    

def PrintInFile(data) :
    with open('discont_today_macys.txt', 'a+') as output_file:
        print(data, file=output_file)


def GetCountOfPage(data) :
    try :
        soup = BeautifulSoup(data, features="lxml")
        pages = soup.findAll('ul', {'class': ['pagePagination']})
        pages = str(pages)
        page = re.findall(r'Page 1 of [0-9]*', pages)
        page = str(page)
        page_ = re.sub( r'Page 1 of ', '', page)
        if not page_ :
            return 0
        else :
            return int(page_[2:-2])
    except:
        return 0
    


def Pause(sec) :
    time.sleep(sec)


brands_list = [
'adidas',
'asics',
'boss',
'moschino',
'calvin%20klein',
'canali',
'chloe',
'columbia',
'converse',
'diesel',
'dkny',
'dolce%20gabbana',
'dsquared2',
'emporio%20armani',
'g%20star',
'giorgio%20armani',
'gucci',
'guess',
'harley-davidson',
'ivanka%20trump',
'kenzo',
'lacoste',
'ralph%20lauren',
'levis',
'reebok',
'roberto%20cavalli',
'timberland',
'tommy%20hilfiger',
'ugg',
'valentino',
'vans',
'versace',
'victorias%20secret',
'michael%20kors',
'new%20balance',
'nike',
'the%20north%20face',
'ralph%20lauren',
'prada',
'puma'
]

'''
url_1 = 'https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Price_discount_range,Pageindex/70_PERCENT_%20off%20%26%20more'
url_2 = 'https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Price_discount_range,Pageindex/70_PERCENT_%20off%20%26%20more,' + str(j+1)

url_1 = 'https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Special_offers/Offer%20code%20PRES'
url_2 = 'https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Special_offers,Pageindex/Offer%20code%20PRES,'+ str(j+1)
'''

i = 0
while i < len(brands_list) - 1 :
    
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    d = webdriver.Firefox(firefox_options=firefox_options)
    d.get('https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Price_discount_range,Pageindex/70_PERCENT_%20off%20%26%20more')
    #d.get('https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Special_offers/Offer%20code%20PRES')
    t=d.page_source
    pag = GetCountOfPage(t)

    j = 0
    prin_3 = str(i) +"  "+ str(brands_list[i]) + "\n"
    print(prin_3)
    d.close()
    while j <= pag :
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        d = webdriver.Firefox(firefox_options=firefox_options)
        d.get('https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Price_discount_range,Pageindex/70_PERCENT_%20off%20%26%20more,' + str(j+1))
        #d.get('https://www.macys.com/shop/featured/' + str(brands_list[i]) + '/Special_offers,Pageindex/Offer%20code%20PRES,'+ str(j+1))
        
        prin_2 = "\t страница №  "+ str(j+1) + "\n"
        print(prin_2)
        
        j = j + 1
        t=d.page_source
        ParsNoKupon(t, 70)
        ##ParsWithKupon(t, 10)
        d.close()
        Pause(30)
    i = i + 1
    Pause(15)
