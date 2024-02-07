from .amazon import Amazon
from .flipkart import Flipkart
from .meesho import Meesho

def get_site(url):
    if 'amazon' in url:
        return Amazon
    elif 'flipkart' in url:
        return Flipkart
    elif 'meesho' in url:
        return Meesho
    else:
        return None