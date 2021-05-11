from requests_html import HTMLSession
import re
import pandas as pd
import getpass


from time import sleep
from random import randint

print("*************************BESTBUY_WEB_SCRAPER*************************\n")

price = []
brand = []
model = []
color_material = []

session = HTMLSession()

input_pagenum = int(
    input("Enter number of pages to scrape (default is 1): ") or "1")

print("\nLoading...")

webpages = range(1, input_pagenum + 1)

for page in webpages:
    r = session.get(
        "https://www.bestbuy.com/site/refrigerators/french-door-refrigerators/abcat0901004.c?" + "cp=" + str(page))
    item_desc = r.html.find("h4 a[href]")
    item_price = r.html.find(
        "div.priceView-hero-price.priceView-customer-price")

    for item in item_price:
        clean_string = re.sub("[Y].+", '', item.text)
        price.append(clean_string)

    for item in item_desc:
        # Split returned string
        split_str = item.text.split(" -", 7)

        brand.append(split_str[0])
        model.append(split_str[1])
        color_material.append(split_str[-1])

    sleep(randint(2, 5))

print("\nDONE: CSV file is in your downloads folder")

dictionary = {"brand": brand, "description": model, "price": price}
df = pd.DataFrame(dictionary)

username = getpass.getuser()
df.to_csv("/Users/" + username + "/Downloads/BestBuy_WebScrape.csv",
          index=False, encoding='utf-8-sig')
