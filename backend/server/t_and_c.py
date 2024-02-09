from bs4 import BeautifulSoup
import requests

def getTandC(url):
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
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('body').text