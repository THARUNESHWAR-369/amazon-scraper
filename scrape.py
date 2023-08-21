import requests
from bs4 import BeautifulSoup
import csv
from product_items import ProductItem
import pandas as pd

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_response(base_url, page_number):
    url = base_url
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response
    else:
        print(f"Status code {response.status_code} for page {page_number}, skipping...")
        return get_response(base_url,page_number)

def scrape_product_listings(base_url, max_pages):
    product_lists = []
    
    page_number = 1
    count = 0

    while page_number < 2:
        
        response = get_response(base_url.format(page_number), page_number)
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
            
            scrape_individual_product(product_url, page_number)
            
            count += 1
            page_number += 1
            break
        print(f"Page={page_number} ==> count = {count}")
        page_number += 1
        
        
    return product_lists

def scrape_individual_product(product_url, page_number):
    
    product_lists = []

    response = get_response(product_url, page_number)
    soup = BeautifulSoup(response.content, "html.parser")
    
    descriptionsUl = soup.find('div', attrs={'id':"productDescription"})
    descriptionsUl = None if descriptionsUl is None else descriptionsUl.text.strip()
    
    #asin_no = product_url.split('/')[6]
    
    manufacturer_tag = soup.find('ul', attrs={'class':"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})
    #manufacturer_value = manufacturer_tag.find("span", {"class": "a-size-base"}).get_text(strip=True)

    #asin_tag = soup.find("li", {"class": "a-list-item"}, text="ASIN")
    #asin_value = asin_tag.find("span", {"class": "a-size-base"}).get_text(strip=True)

    #print("ASIN:", asin_value)

    print("Manufacturer:", manufacturer_tag)

    
    
    

def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"
    max_pages = 20

    products = scrape_product_listings(base_url, max_pages)

    csv_filename = "amazon_products.csv"
    csv_header = ["Product URL", "Product Name", "Product Price", "Rating", "Reviews"]

    individualProducts = []  
    
    #for productData in products:
    #individual_products = scrape_individual_product("https://www.amazon.in/Half-Moon-Backpack-Luggage-Compartment/dp/B09VCLZ3K4/ref=sr_1_5?keywords=bags&sr=8-5&th=1")
    #individualProducts.append(individual_products)
        
    #df = pd.DataFrame(products, columns=csv_header)
    #df.drop_duplicates(inplace=True)
    #df.to_csv(csv_filename, index=False)

    """
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_header)

        for data in product_data:
            csv_writer.writerow(data.toList())
    """
    print("Data extraction and writing to CSV complete.")

if __name__ == "__main__":
    main()
