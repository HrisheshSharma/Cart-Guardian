from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import pageData
from ETL import ETLPipeline
from Review import Reviews
import requests
import pattern_matching
import t_and_c

llm_server_url = 'https://cde6-35-238-251-29.ngrok-free.app/'
vlm_server_url = 'https://80c1-35-189-1-141.ngrok-free.app/'

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def llm_request(promptType: str, promptText: str):
    request_json = {
        "promptType": promptType,
        "promptText": promptText
    }
    response = requests.post(llm_server_url, json=request_json)
    return response.json()

def vlm_request(promptType: str, promptText: str, promptImageURL: str):
    request_json = {
        "promptType": promptType,
        "promptText": promptText,
        "promptImageURL": promptImageURL
    }
    response = requests.post(vlm_server_url, json=request_json)
    return response.json()

def match_product_image():
    image_description = vlm_request('describe', '', app.data.get_product_images()[0]).get('output')
    image_title = app.data.get_product_name()
    output = llm_request('match', f'image description : {image_description} image_title: {image_title}').get('output')
    return output

def get_TandC(base_url):
    all_links = app.data.soup.find_all('a')
    links = []
    for link in all_links:
        if 'terms' in link.text.lower() or 'conditions' in link.text.lower() or 't&c' in link.text.lower() or 'terms of service' in link.text.lower() or 'privacy policy' in link.text.lower() or 'refund policy' in link.text.lower() or 'return policy' in link.text.lower() or 'shipping policy' in link.text.lower() or 'delivery policy' in link.text.lower() or 'shipping and delivery' in link.text.lower() or 'shipping & delivery' in link.text.lower() or 'delivery and shipping' in link.text.lower() or 'delivery & shipping' in link.text.lower() or 'shipping and returns' in link.text.lower() or 'shipping & returns' in link.text.lower() or 'returns and shipping' in link.text.lower() or 'returns & shipping' in link.text.lower() or 'shipping and refund' in link.text.lower() or 'shipping & refund' in link.text.lower() or 'refund and shipping' in link.text.lower() or 'refund & shipping' in link.text.lower() or 'refund and returns' in link.text.lower() or 'refund & returns' in link.text.lower() or 'returns and refund' in link.text.lower() or 'returns & refund' in link.text.lower() or 'privacy' in link.text.lower() or 'refund' in link.text.lower() or 'return' in link.text.lower() or 'shipping' in link.text.lower() or 'delivery' in link.text.lower():
            links.append({'link': base_url + link.get('href'), 'text': link.text.strip()})
    return links
            
def get_base_url(url):
    if 'http' in url:
        idx = url.find('//')
        idx2 = url.find('/', idx+2)
        return url[:idx2]
    else:
        return url.split('/')[0]
        
@app.get("/")
def read_root():
    return {"Hello": "World"}

app.data = None
app.url = None
@app.post("/page")
def create_page(page: pageData.PageData):
    # print(page.pageData)
    app.data = ETLPipeline(page.pageData, page.pageUrl)
    app.url = page.pageUrl
    # print(app.data.soup.text.strip().replace('\n', ''))
    # print(app.data.get_product_name())
    # print(app.data.get_product_images())
    # tclinks = get_TandC(get_base_url(page.pageUrl))
    # print('Product Name: ', data.get_product_name())
    # print('Saving: ', data.get_saving())
    # print('Discounted Price: ', data.get_discounted_price())
    # print('MRP: ', data.get_mrp())
    # print('Return Policy: ', data.get_return_policy())
    # print('Free Delivery: ', data.get_free_delivery())
    # print('Product Details: ', data.get_product_details())
    # print('Product Description: ', data.get_product_description())
    # print('Stars: ', data.get_stars())
    # print('Total Reviews: ', data.get_total_reviews())
    # print('Image URL: ', data.get_product_images())
    # print('Reviews', data.get_reviews())
    return {"message": "Data received"}

@app.get("/reviews")
def get_reviews():
    search = Reviews()
    print(app.data.get_product_name())
    reviews = search.get_reviews(app.data.get_product_name())
    print(reviews)
    return reviews

@app.get("/match")
def match_product():
    res = match_product_image()
    print(res)
    if res is None:
        return True
    if 'true' in res.lower():
        return True
    elif 'false' in res.lower():
        return False
    else:
        return True
    
@app.get("/pattern")
def find_dark_pattern():
    div_list= app.data.soup.find_all('div')
    # span_list= app.data.soup.find_all('span')
    # iframe_list= app.data.soup.find_all('iframe')
    dark_pattern_div= []
    dark_pattern_span= []
    dark_pattern_iframe= []
    innermost_divs_text = [(i, div) for i, div in enumerate(div_list) if not div.find('div')]
    for i, div in innermost_divs_text:
        if(div.get('id') == 'customerReviews' or div.get('class')=='col JOpGWq'):
            break
        
        dark= pattern_matching.is_dark(div.text)
        if(dark):
            dark_div= {'pos': i, 'pattern': dark}
            dark_pattern_div.append(dark_div)
            
    # for i, span in enumerate(span_list):
    #     dark= pattern_matching.is_dark(span.text)
    #     if(dark):
    #         dark_span= {'pos': i, 'pattern': dark}
    #         dark_pattern_span.append(dark_span)
    
    # for i, iframe in enumerate(iframe_list):
    #     dark= pattern_matching.is_dark(iframe.text)
    #     if(dark):
    #         dark_iframe= {'pos': i, 'pattern': dark}
    #         dark_pattern_iframe.append(dark_iframe)
    
    return {'div': dark_pattern_div, 'span': dark_pattern_span, 'iframe': dark_pattern_iframe}

@app.get("/tandc")
def get_tandc():
    responses = []
    tclinks = get_TandC(get_base_url(app.url))
    for link in tclinks:
        tcText = t_and_c.getTandC(link.get('link'))
        if tcText is not None:
            summaries = ''
            # Get 2000 words from the T&C
            # for i in range(0, len(tcText.split()), 3000):
            for i in range(0, min(2000, len(tcText.split())), 2000):
                tc2000 = ' '.join(tcText.split()[i:i+2000])
                # print(tc2000)
                summary = llm_request('summarization', tc2000).get('output')
                summaries += summary + '\n'
            responses.append({'link': link.get('link'), 'text': link.get('text'), 'summary': summaries})
    return responses
