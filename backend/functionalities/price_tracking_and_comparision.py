import requests
from collections import namedtuple
from bs4 import BeautifulSoup
# struct for storing name, base website and search website of a ecommerce website
Website_data = namedtuple('Website_data', ['name', 'base_website', 'search_url', 'class1', 'class2', 'name_class'])
Data = [
    Website_data(name = 'amazon', base_website = 'https://www.amazon.in', search_url = 'https://www.amazon.in/s?k=', class1 = 'a-price-whole', class2 = 'a-price-whole', name_class = 'a-size-large product-title-word-break'),
    Website_data(name = 'flipkart', base_website = 'https://www.flipkart.com', search_url = 'https://www.flipkart.com/search?q=', class1 = '_30jeq3 _16Jk6d', class2 = '_30jeq3 _1_WHN1', name_class = 'B_NuCI')
]
def across_platform_search(id1, id2, url, flag): # here id1 and id2 should be names of platforms in small letters !!!
    # print("i worked")
    #declarations skip while reading
    platform1_base_url = ''
    platform2_base_url = ''
    platform2_url = ''
    platform1_class = ''
    platform2_class = ''
    platform1_name_class = ''
    #looping around to assign relevant data to variables
    for Website_data in Data:
        if id1 == Website_data.name:
            platform1_base_url = Website_data.base_website
            platform1_class = Website_data.class1
            platform1_name_class = Website_data.name_class
        elif id2 == Website_data.name:
            platform2_base_url = Website_data.base_website
            platform2_url = Website_data.search_url
            platform2_class = Website_data.class2
    platform1_url = url
    headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Connection' : 'keep-alive',
        'Sec-Fetch-Dest' : 'document',
        'Sec-Fetch-Mode' : 'navigate',
        'Sec-Fetch-Site' : 'none',
        'Sec-Fetch-User' : '?1',
        'Upgrade-Insecure-Requests' : '1'
    }
    # print(f"platform :1  is {id1}, class is {platform1_class}, base url is {platform1_base_url}, url is {platform1_url}, name_class is {platform1_name_class} platform2 is {id2} base url is {platform2_base_url}")
    platform1_base_response = requests.get(platform1_base_url, headers = headers)
    platform1_cookies = platform1_base_response.cookies
    platform1_product_response = requests.get(platform1_url, headers = headers, cookies = platform1_cookies)
    platform1_soup = BeautifulSoup(platform1_product_response.text, parser='html.parser', features = 'lxml')
    platform1_price_lines = platform1_soup.findAll(class_=platform1_class)
    platform1_price = str(platform1_price_lines[0].text.strip())
    platform1_title_x = platform1_soup.findAll(class_=platform1_name_class)
    platform1_title = str(platform1_title_x[0].text.strip())
    x = len(platform1_price)
    # temp = amazon_price[1:(x + 1)//2 - 3]
    tempx = platform1_price.replace(',', "").replace('.', "").replace('₹', "")
    # temp = tempx.replace('.',"")
    # tmp = temp.replace(' ', "")
    price_1 = int(tempx)
    print(f"{id1} price : ")
    print(price_1)
    if flag == 0:
        return
    platform2_url = platform2_url + platform1_title
    platform2_base_response = requests.get(platform2_base_url, headers = headers)
    platform2_cookies = platform2_base_response.cookies
    # print(platform2_url)
    platform2_product_response = requests.get(platform2_url, headers = headers, cookies = platform2_cookies)
    platform2_soup = BeautifulSoup(platform2_product_response.text, parser='html.parser', features = 'lxml')
    price_lines = platform2_soup.findAll(class_=platform2_class)
    price = str(price_lines[0].text.strip())
    x1 = len(price)
    # temp = price[1:x]
    tempx = price.replace(',', "").replace('.', "").replace('₹', "")
    price2 = int(tempx)
    print(f"{id2} price :")
    print(price2)


#calling function 
across_platform_search('amazon', 'flipkart', 'https://www.amazon.in/Adidas-CBLACK-Running-Shoes-9-CL4154_9/dp/B07M8S2BQX/ref=sr_1_1?pf_rd_i=1983518031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=3ad2a80e-dc26-4d41-9d94-10c82be76668&pf_rd_r=TCG19MCPBN2MG50H25XE&pf_rd_s=merchandised-search-6&pf_rd_t=30901&qid=1707487860&refinements=p_89%3AAdidas%2Cp_n_pct-off-with-tax%3A40-60&s=shoes&sr=1-1', 0)
# flag == 0 means only id1 price will be returned flag == 1 means both id1 and id2