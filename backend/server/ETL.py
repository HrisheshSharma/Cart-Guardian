from bs4 import BeautifulSoup
import re
import sites

class ETLPipeline:
    def __init__(self, htmlData, url):
        self.htmlData = htmlData
        self.url = url
        self.soup = BeautifulSoup(htmlData, 'html.parser')
        self.element_map = sites.get_site(url)
    
    def get_product_name(self):
        element = self.element_map.product_name
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_saving(self):
        element = self.element_map.saving
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_discounted_price(self):
        element = self.element_map.discounted_price
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_mrp(self):
        element = self.element_map.mrp
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_return_policy(self):
        element = self.element_map.return_policy
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_free_delivery(self):
        element = self.element_map.free_delivery
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_product_details(self):
        element = self.element_map.product_details
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        element = self.element_map.product_features
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_product_description(self):
        element = self.element_map.product_description
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_stars(self):
        element = self.element_map.stars
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_total_reviews(self):
        element = self.element_map.total_reviews
        if element:
            page_data = self.soup.find(element['element'], element['attrs'])
            if page_data is not None:
                return page_data.text.strip()
        return None
    
    def get_reviews(self):
        element = self.element_map.review
        if element:
            page_data = self.soup.find_all(element['element'], element['attrs'])
            if page_data is not None:
                return [review.text.strip() for review in page_data]
    
    def get_product_images(self):
        element = self.element_map.product_images
        images = []
        if element:
            img_divs = self.soup.find_all(element['element'], element['attrs'])
            for img_div in img_divs:
                imgs = img_div.find_all('img')
                if imgs is not None:
                    images.extend([img.get('src') for img in imgs])
        return images