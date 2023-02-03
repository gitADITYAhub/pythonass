import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    product_listings = soup.find_all("span", class_="a-size-medium a-color-base a-text-normal")
    product_data = []
    for listing in product_listings:
        link = listing.find_parent("a")
        if link:
            product_url = "https://www.amazon.in"+link["href"]
        else:
            product_url = None
        product_name = listing.text.strip()
        product_price = listing.find_next("span", class_="a-price-whole").text.strip()
        rating_tag = listing.find_next("span", class_="a-icon-alt")
        if rating_tag:
            rating = rating_tag.text.strip()
        else:
            rating = None
        num_reviews_tag = listing.find_next("span", class_="a-size-base")
        if num_reviews_tag:
            num_reviews = num_reviews_tag.text.strip()
        else:
            num_reviews = None

        # Hit the product URL to get additional information
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, "lxml")

        # Get product description
        product_description_tag = product_soup.find("div", id="productDescription")
        if product_description_tag:
            product_description = product_description_tag.text.strip()
        else:
            product_description = None

        # Get ASIN
        asin = product_url.split("/")[-1].split("?")[0]

        # Get manufacturer
        manufacturer_tag = product_soup.find("div", id="bylineInfo")
        if manufacturer_tag:
            manufacturer = manufacturer_tag.text.strip()
        else:
            manufacturer = None

        product_data.append({
            "Product URL": product_url,
            "Product Name": product_name,
            "Product Price": product_price,
            "Rating": rating,
            "Number of Reviews": num_reviews,
            "Description": product_description,
            "ASIN": asin,
            "Manufacturer": manufacturer
        })
        
    return product_data

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

product_data = []
product_data.extend(scrape_product_info(url))

for i in range(2, 21):
    url = f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}"
    product_data.extend(scrape_product_info(url))

# Convert the product data to a Pandas dataframe and export to a CSV file
df = pd.DataFrame(product_data)
df.to_csv("product_data.csv", index=False)
print("data sent to product data csv fie")
