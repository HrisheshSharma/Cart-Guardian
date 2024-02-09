from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import pageData
from ETL import ETLPipeline
from Review import Reviews

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