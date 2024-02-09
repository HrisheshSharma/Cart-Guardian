from bs4 import BeautifulSoup
import re
import sites
import requests
import os

class Reviews:
    def __init__(self):
        self.google_api_key = os.environ.get('GOOGLE_SEARCH')
        self.cx = '16bf42430283e4cb5'
        self.extract_review = {
            'tomsguide': {
                'element': 'p',
                'attrs': {'class': 'pretty-verdict'}
            },
            'techradar': {
                'element': 'div',
                'attrs': {'class': 'pretty-verdict'}
            
            },
            'digit': {
                'element': 'article',
            },
            'weartesters': {
                'element': 'div',
                'attrs': {'class': 'entry-content'}
            },
            'skincarevilla': {
                'element': 'article'
            },
            'thebeautyinsideout': {
                'element': 'div',
                'attrs': {'id': 'primary'}
            },
            'digitaltrends': {
                'element': 'article'
            },
            'engadget': {
                'element': 'div',
                'attrs': {'class': 'caas-content'}
            },
            'anandtech': {
                'element': 'div',
                'attrs': {'class': 'articleContent'}
            },
            'tomshardware': {
                'element': 'div',
                'attrs': {'class': 'pretty-verdict'}
            },
            'techspot': {
                'element': 'div',
                'attrs': {'class': 'articleBody'}
            },
            'cnet': {
                'element': 'meta',
                'attrs': {'content': 'article'}
            },
            'theverge': {
                'element': 'aside'
            },
            'soleracks': {
                'element': 'div',
                'attrs': {'class': 'fusion-content-boxes'}
            },
            'shoesguidance': {
                'element': 'div',
                'attrs': {'class': 'entry-content'}
            },
            'laptopmag': {
                'element': 'div',
                'attrs': {'class': 'pretty-verdict'}
            }
        }
    
    def search_google(self, query):
        query = query.lower()
        google_search = f'https://www.googleapis.com/customsearch/v1?key={self.google_api_key}&cx={self.cx}&q={query}&exactTerms=review&excludeTerms=page'
        google_search_response = requests.get(google_search)
        if google_search_response.status_code != 200:
            return None
        return google_search_response.json()

    def get_reviews(self, query):
        google_search_response = self.search_google(query)
        if google_search_response is None:
            return None
        items = google_search_response.get('items')
        if items is None:
            return None
        reviews = []
        for item in items:
            for website, review_tree in self.extract_review.items():
                if website in item['link']:
                    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edg/121.0.0.0', 
                               'referer': item['link']}
                    response = requests.get(item['link'], headers=headers)
                    print(response.status_code)
                    # print(response.text)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    attrs = review_tree.get('attrs')
                    if attrs:
                        review = soup.find_all(review_tree['element'], review_tree['attrs'])
                    else:
                        review = soup.find_all(review_tree['element'])
                    review_text = ''
                    for r in review:
                        review_text += r.text + '\n'
                    reviews.append({'website': website, 'review': review_text, 'link': item['link']})    
                    # print(item['link'], review[0].text)
                    # if review:
                    #     reviews.append({
                    #         'website': website,
                    #         'review': review[0].text
                    #     })
                    # break
        return reviews