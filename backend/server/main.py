from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import pageData
from ETL import ETLPipeline
from Review import Reviews
import pattern_matching

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.data = None
@app.post("/page")
def create_page(page: pageData.PageData):
    # print(page.pageData)
    app.data = ETLPipeline(page.pageData, page.pageUrl)
    print(app.data.soup.text.strip().replace('\n', ''))
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
    return search.get_reviews(app.data.get_product_name())

@app.get("/pattern")
def find_dark_pattern():
    div_list= app.data.soup.find_all('div')
    # span_list= app.data.soup.find_all('span')
    # iframe_list= app.data.soup.find_all('iframe')
    dark_pattern_div= []
    dark_pattern_span= []
    dark_pattern_iframe= []
    
    for i, div in enumerate(div_list):
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
