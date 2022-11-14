from ast import Try
from bs4 import BeautifulSoup
import requests
from lxml import etree as et
from csv import writer

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36"}
base_url = "https://www.flipkart.com"
smartWatch_brands = ['APPLE', 'Noise', 'boAt', 'Honor', 'SAMSUNG', 'FITBIT', 'Amazfit', 'GARMIN', 'Huawei', 'FOSSIL']
product_list = []


def get_dom(the_url):
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


def details(dom1):
    try:
        title = dom1.xpath('//span[@class="B_NuCI"]/text()')[0]
    except Exception as e:
        title = 'No title available'
    if title == 'No title available':
        product_brand = 'No brand available'
    else:
        product_brand = title.split()[0]
    try:
        sales_price = dom1.xpath('//div[@class="_30jeq3 _16Jk6d"]/text()')[0].replace(u'\u20B9','')
    except Exception as e:
        sales_price = 'No price available'
    try:
        mrp = dom1.xpath('//div[@class="_3I9_wc _2p6lqe"]/text()')[1]
    except Exception as e:
        mrp = sales_price
    try:
        discount = dom1.xpath('//div[@class="_3Ay6Sb _31Dcoz"]/span/text()')[0].split()[0].replace('%','')
    except Exception as e:
        discount = 0
    try:
        no_of_ratings = dom1.xpath('//div[@class="col-12-12"]/span/text()')[0].split()[0]
    except Exception as e:
        no_of_ratings = 0
    try:
        no_of_reviews = dom1.xpath('//div[@class="col-12-12"]/span/text()')[1].split()[0]
    except Exception as e:
        no_of_reviews = 0
    try:
        overall_rating = dom1.xpath('//div[@class="_2d4LTz"]/text()')[0]
    except Exception as e:
        overall_rating = 0
    try:
        description = dom1.xpath('//div[@class="_1mXcCf RmoJUa"]/text()')
        if description:
            description = description[0]
        else:
            description = 'No description available'
    except Exception as e:
        description = "No description available"
    try:
        features = dom1.xpath('//li[@class="_21lJbe"]/text()')
        for ele in features:
            if 'GB' in ele:
                memory = ele.replace('GB','')
                break
            else:
                memory = 'Memory data not available'
    except Exception as e:
        memory = 'Memory data not available'
    product_record = [title, product_brand, sales_price, mrp, discount, memory, no_of_ratings, no_of_reviews, overall_rating,description]
    return product_record


with open('smartwatch_data.csv','w',newline='', encoding='utf-8') as f:
    theWriter = writer(f)
    heading = ['Product_url','Product_name','Brand','Sale_price','MRP','Discount_percentage','Memory','No_of_ratings','No_of_reviews','Star_rating','Description']
    theWriter.writerow(heading)
    for product in product_list:
        product_url = base_url + product
        product_dom = get_dom(product_url)
        record = [product_url]+details(product_dom)
        theWriter.writerow(record)


