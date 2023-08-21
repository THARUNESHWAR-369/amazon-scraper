import requests
from bs4 import BeautifulSoup
import csv
from product_items import ProductItem
import pandas as pd

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_response(base_url, page_number, individualProduct=False):
    url = base_url.format(page_number) if not individualProduct else base_url
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response
    else:
        print(f"Status code {response.status_code} for page {page_number}, skipping...")
        return get_response(base_url, page_number)

def scrape_product_listings(base_url, max_pages):
    product_lists = []
    
    page_number = 1
    count = 0

    while page_number < max_pages + 1:
        
        response = get_response(base_url, page_number)
        soup = BeautifulSoup(response.content, "html.parser")
        
        cards = soup.find_all('div', attrs={'class':"s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t3 puis-include-content-margin puis puis-v3b48cl1js792724v4d69zlbwph s-latency-cf-section s-card-border"})
        
        if len(cards) == 0:
            print(f"No product cards found on page {page_number}, retrying...")
            continue
        
        for i in range(len(cards)):
            left_card = cards[i].find('div', attrs={'class': 'a-section a-spacing-small a-spacing-top-small'})
            
            product_name = left_card.find('span', attrs={'class':"a-size-medium a-color-base a-text-normal"})
            product_name = None if product_name is None else product_name.text
            product_price = left_card.find('span', attrs={'class':"a-offscreen"})
            product_price = None if product_price is None else product_price.text
            product_rating = left_card.find('span', attrs={'class':"a-size-base puis-bold-weight-text"})
            product_rating = None if product_rating is None else product_rating.text
            product_review = left_card.find('span', attrs={'class':"a-size-base s-underline-text"})
            product_review = None if product_review is None else product_review.text
            product_url = cards[i].find('a', attrs={'class':'a-link-normal s-no-outline'})
            product_url = None if product_url is None else "https://www.amazon.com"+product_url.get('href')
            product_img = cards[i].find("img", attrs={'class':'s-image'})
            product_img = None if product_img is None else product_img.get('src')
            
            products = ProductItem(product_url, product_name, product_price, product_rating, product_review)
            product_lists.append(products)
            count += 1
        print(f"Page={page_number} ==> count = {count}")
        page_number += 1
        
        
    return product_lists

def scrape_individual_product(product_url):
    
    product_lists = []

    response = get_response(product_url, individualProduct=True)
    soup = BeautifulSoup(response.content, "html.parser")
    
    cards = soup.find_all('div', attrs={'class':"s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t3 puis-include-content-margin puis puis-v3b48cl1js792724v4d69zlbwph s-latency-cf-section s-card-border"})
    
    if len(cards) >= 0:
        print(cards)

    

def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"
    max_pages = 20

    products = scrape_product_listings(base_url, max_pages)

    csv_filename = "amazon_products.csv"
    csv_header = ["Product URL", "Product Name", "Product Price", "Rating", "Reviews"]

    p = []  
    
    for productData in products:
        p.append(productData.toList())
    
    df = pd.DataFrame(p, columns=csv_header)
    df.drop_duplicates(inplace=True)
    df.to_csv(csv_filename, index=False)

    print("Data extraction and writing to CSV complete.")

if __name__ == "__main__":
    main()
