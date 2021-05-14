from requests_html import HTMLSession
import re
import pandas as pd
import getpass

from time import sleep
from random import randint

print("*************************BESTBUY_WEB_SCRAPER*************************\n")

def getBaseUrl():
    url = "https://www.bestbuy.com/site/refrigerators/french-door-refrigerators/abcat0901004.c"
    return url

price = []
brand = []
model = []
#color_material = []

session = HTMLSession()

max_pagenum = int(session.get(getBaseUrl()).html.find("ol.paging-list > li:nth-last-child(1)", first=True).text)

def inputPageNum():
    response = int(
        input("Enter number of pages to scrape (default is 1): ") or "1")

    while (response > max_pagenum):
        print("\nERROR: Number of pages entered exceeds the number of pages available " +
              "(" + str(max_pagenum) + ")")
        response = inputPageNum()
    return response

input_pagenum = inputPageNum()
webpages = range(1, input_pagenum + 1)

print("\nLoading...")

for page in webpages:
    r = session.get(getBaseUrl() + "?cp=" + str(page))
    items = r.html.find("#main-results > ol > li.sku-item")

    for item in items:
        item_price = item.find(
            "div.priceView-hero-price.priceView-customer-price", first=True)
        if item_price != None:
            clean_string = re.sub("[Y].+", '', item_price.text)
            price.append(clean_string)
        else:
            price.append("n/a")

    for item in items:
        # Split returned string
        item_desc = item.find("h4 a[href]", first=True)
        split_str = item_desc.text.split(" -", 1)

        brand.append(split_str[0])
        model.append(split_str[1])
        # color_material.append(split_str[-1])

    sleep(randint(2, 5))

dictionary = {"brand": brand, "description": model, "price": price}
df = pd.DataFrame(dictionary)

username = getpass.getuser()
input_filename = input("\nEnter name for the file (no extention required): ")
df.to_csv("/Users/" + username + "/Downloads/" + input_filename + ".csv", index=False, encoding='utf-8-sig')

print("DONE: CSV file is in your downloads folder")
