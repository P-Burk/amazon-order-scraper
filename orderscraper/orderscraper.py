import requests
from bs4 import BeautifulSoup
import selenium

AMAZON_ORDER_URL = 'https://www.amazon.com/dp/B09WMJCQRM?ref=ppx_yo2ov_dt_b_product_details&th=1'
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/111.0.0.0 Safari/537.36'}

response = requests.get(AMAZON_ORDER_URL, headers=HEADER)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)