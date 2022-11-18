from ast import Try
from bs4 import BeautifulSoup
import requests
from lxml import etree as et
import csv
import random
import time

url_list = []
with open('smartwatch_data_v2.csv', 'r', encoding='utf-8') as f:
    theReader = csv.reader(f)
    next(theReader, None)
    for row in theReader:
        url_list.append(row[0])

header_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"]

def get_dom(the_url):
    user_agent = random.choice(header_list)
    header = {"User-Agent": user_agent}
    response = requests.get(the_url, headers=header, stream=True)
    soup = BeautifulSoup(response.text, 'lxml')
    current_dom = et.HTML(str(soup))
    return current_dom

def description(dom1):
    try:
        desc = dom1.xpath('//div[@class="_1mXcCf RmoJUa"]/p/text()')
        if desc:
            desc = desc[0]
        else:
            desc1 = dom1.xpath('//div[@class="_1mXcCf RmoJUa"]/p/text()')
            if desc1:
                desc = desc1[0]
            else:
                specs_title = dom1.xpath('//tr[@class="_1s_Smc row"]/td/text()')
                specs_detail = dom1.xpath('//tr[@class="_1s_Smc row"]/td/ul/li/text()')
                specs_dict = {}
                for i in range(len(specs_title)):
                    specs_dict[specs_title[i]] = specs_detail[i]
                desc = str(specs_dict)
    except Exception as e:
        specs_title = dom1.xpath('//tr[@class="_1s_Smc row"]/td/text()')
        specs_detail = dom1.xpath('//tr[@class="_1s_Smc row"]/td/ul/li/text()')
        specs_dict = {}
        for i in range(len(specs_title)):
            specs_dict[specs_title[i]] = specs_detail[i]
        desc = str(specs_dict)
    return desc

for url in url_list:
    url_dom = get_dom(url)
    desc = description(url_dom)
    print(desc)




