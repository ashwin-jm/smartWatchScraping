from ast import Try
from bs4 import BeautifulSoup
import requests
from lxml import etree as et
from csv import writer
import random
import time

header_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"]
base_url = "https://www.flipkart.com"
smartWatch_brands = ['APPLE', 'Noise', 'boAt', 'Honor', 'SAMSUNG', 'FITBIT', 'Amazfit', 'GARMIN', 'Huawei', 'FOSSIL']
product_list = []


def get_dom(the_url):
    user_agent = random.choice(header_list)
    header = {"User-Agent": user_agent}
    response = requests.get(the_url, headers=header, stream=True)
    soup = BeautifulSoup(response.text, 'lxml')
    current_dom = et.HTML(str(soup))
    return current_dom


for brand in smartWatch_brands:
    page_url = "https://www.flipkart.com/wearable-smart-devices/smart-watches/pr?sid=ajy%2Cbuh&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D" + brand
    dom = get_dom(page_url)
    pages = dom.xpath('//div[@class="_2MImiq"]/span/text()')
    page_product_list = dom.xpath('//a[@class="_1fQZEK"]/@href')
    product_list += page_product_list
    if not pages:
        continue
    else:
        no_of_pages = int(pages[0].split()[3])
        for i in range(2, no_of_pages + 1):
            next_page_url = page_url + "&page=" + str(i)
            dom = get_dom(next_page_url)
            page_product_list = dom.xpath('//a[@class="_1fQZEK"]/@href')
            product_list += page_product_list
            time.sleep(random.randint(2,8))


def titleandbrand(dom1):
    try:
        title = dom1.xpath('//span[@class="B_NuCI"]/text()')[0]
    except Exception as e:
        title = 'No title available'
    if title == 'No title available':
        product_brand = 'No brand available'
    else:
        product_brand = title.split()[0]
    return title, product_brand


def salespriceandmrp(dom1):
    try:
        sales_price = dom1.xpath('//div[@class="_30jeq3 _16Jk6d"]/text()')[0].replace(u'\u20B9','')
    except Exception as e:
        sales_price = 'No price available'
    try:
        mrp = dom1.xpath('//div[@class="_3I9_wc _2p6lqe"]/text()')[1]
    except Exception as e:
        mrp = sales_price
    return sales_price, mrp


def discount(dom1):
    try:
        disc = dom1.xpath('//div[@class="_3Ay6Sb _31Dcoz"]/span/text()')[0].split()[0].replace('%','')
    except Exception as e:
        disc = 0
    return disc


def noofratings(dom1):
    try:
        no_of_ratings = dom1.xpath('//div[@class="col-12-12"]/span/text()')[0].split()[0]
    except Exception as e:
        no_of_ratings = 0
    return no_of_ratings


def noofreviews(dom1):
    try:
        no_of_reviews = dom1.xpath('//div[@class="col-12-12"]/span/text()')[1].split()[0]
    except Exception as e:
        no_of_reviews = 0
    return no_of_reviews


def overallrating(dom1):
    try:
        overall_rating = dom1.xpath('//div[@class="_2d4LTz"]/text()')[0]
    except Exception as e:
        overall_rating = 0
    return overall_rating


def description(dom1):
    try:
        desc = dom1.xpath('//div[@class="_1mXcCf RmoJUa"]/text()')
        if desc:
            desc = desc[0]
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


def memory(dom1):
    try:
        features = dom1.xpath('//li[@class="_21lJbe"]/text()')
        for ele in features:
            if 'GB' in ele:
                mem = ele.replace('GB','')
                break
            else:
                mem = 'Memory data not available'
    except Exception as e:
        mem = 'Memory data not available'
    return mem


with open('smartwatch_data2.csv','w',newline='', encoding='utf-8') as f:
    theWriter = writer(f)
    heading = ['Product_url','Product_name','Brand','Sale_price','MRP','Discount_percentage','Memory','No_of_ratings','No_of_reviews','Star_rating','Description']
    theWriter.writerow(heading)
    for product in product_list:
        product_url = base_url + product
        product_dom = get_dom(product_url)
        product_url = product_url.split('&marketplace')[0]
        title, brand = titleandbrand(product_dom)
        sales_price, mrp = salespriceandmrp(product_dom)
        disc = discount(product_dom)
        no_of_ratings = noofratings(product_dom)
        no_of_reviews = noofreviews(product_dom)
        overall_rating = overallrating(product_dom)
        desc = description(product_dom)
        mem = memory(product_dom)
        record = [product_url, title, brand, sales_price, mrp, disc, mem, no_of_ratings, no_of_reviews, overall_rating, desc]
        theWriter.writerow(record)


