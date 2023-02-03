import requests
from bs4 import BeautifulSoup

def scrape_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    product_listings = soup.find_all("span", class_="a-size-medium a-color-base a-text-normal")

    for listing in product_listings:
        link = listing.find_parent("a")
        if link:
            product_url = "https://www.amazon.in"+link["href"]
        else:
            product_url = None
        product_name = listing.text.strip()
        product_price = listing.find_next("span", class_="a-price-whole").text.strip()
        rating = listing.find_next("span", class_="a-icon-alt").text.strip()
        num_reviews = listing.find_next("span", class_="a-size-base").text.strip()

        print("Product URL:", product_url)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Rating:", rating)
        print("Number of Reviews:", num_reviews)
        print()

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

scrape_product_info(url)

for i in range(2, 21):
    url = f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}"
    scrape_product_info(url)
