import re

priceClass = re.compile(r'sc-[a-zA-Z]{6}\s[a-zA-Z]{6}$')
producDetailsClass = re.compile(r'sc-[a-zA-Z]{6}\s[a-zA-Z]{6}\sProductDescription__DetailsCardStyled-sc-1l1jg0i-0\s[a-zA-Z]{6}\sProductDescription__DetailsCardStyled-sc-1l1jg0i-0\s[a-zA-Z]{6}')
imageClassPattern = re.compile(r'sc-[a-zA-Z]{6}\s[a-zA-Z]{6}\sProductCard__StyledCarousel-sc-camkhj-6\siGvXSJ');
class Meesho:
    product_name = {
        'element': 'div',
        'attrs': {
            'class': 'sc-bcXHqe hcOLTO ShippingInfo__DetailCard-sc-frp12n-0 dKuTbW ShippingInfo__DetailCard-sc-frp12n-0 dKuTbW'
            }
        }

    saving = {
        'element': 'span',
        'attrs': {
            'class': 'dOqdSt'
            }
        }

    discounted_price = {
        'element': 'h4',
        'attrs': {
            'class': priceClass
            }
        }

    mrp = {
        'element': 'p',
        'attrs': {
            'class': 'gQDOBc'
            }
        }

    return_policy = None

    free_delivery = {
        'element': 'spand',
        'attrs': {
            'class': 'fkvMlU'
        }
    }

    product_details = {
        'element': 'div',
        'attrs': {
            'class': producDetailsClass
        }
    }

    product_description = None
    
    product_features = None

    stars = {
        'element': 'span',
        'attrs': {
            'class': 'laVOtN'
        }
    }

    total_reviews = {
        'element': 'span',
        'attrs': {
            'class': 'bfIZVF'
        }
    }

    review_summary = None

    review = {
        'element': 'div',
        'attrs': {
            'class': 'eHVGcU'
        }
    }

    product_images = {
        'element': 'div',
        'attrs': {
            'class': imageClassPattern
        }
    }
    
    product_images2 = None