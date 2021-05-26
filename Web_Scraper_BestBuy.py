try:
    from requests_html import HTMLSession
except ModuleNotFoundError:
    print("Module 'requests-html' is not installed and is required for use of this program")
    print("\nQuitting program")
    quit()

try:
    import pandas as pd
except ModuleNotFoundError:
    print("Module 'pandas' is not installed and is required for use of this program")
    print("\nQuitting program")
    quit()

try:
    import sqlalchemy as sq
    installed = True
except ModuleNotFoundError:
    print("Module 'sqlalchemy' is not installed and may impact the functionality of this program")
    installed = False


import re

from time import sleep
from random import randint

import getpass
import platform
import os

def inputPageNum(max_pagenum):
    response = input("Enter number of pages to scrape (default is 1): ") or 1

    while (int(response) > max_pagenum):
        print("\nERROR: Number of pages entered exceeds the number of pages available " + "(" + str(max_pagenum) + ")")
        response = inputPageNum(max_pagenum)

    return int(response)


def scrapeData(webpages, session, baseUrl):

    for page in webpages:
        r = session.get(baseUrl + "?cp=" + str(page))
        items = r.html.find("#main-results > ol > li.sku-item")

        for item in items:
            item_price = item.find(
                "div.priceView-hero-price.priceView-customer-price", first=True)
            if item_price != None:
                clean_string = re.sub("\$|\,|(Y.+)", '', item_price.text)
                price.append(float(clean_string))
            else:
                price.append(None)

        for item in items:
            item_desc = item.find("h4 a[href]", first=True)
            split_str = item_desc.text.split(" -", 2)

            brand.append(split_str[0])
            model.append(split_str[1])

            if (len(split_str) > 2):
                color_material.append(split_str[-1])
            else:
                color_material.append(None)

        sleep(randint(2, 6))

def previewDataOption(df): 
    response = input("\nWould you like to preview the dataframe? (y/n): ").lower() or "n"  

    if response == "y":
        print(df.head(n=10))  

def toCSV(df):
    username = getpass.getuser()
    input_filename = input(
        "\nEnter name for the file (no extention required): ") or "BestBuy_Web_Scrape"

    plt = platform.system()
    if (plt == "Windows"):
        df.to_csv("C:/Users/" + username + "/Downloads/" +
                  input_filename + ".csv", index=False, encoding='utf-8-sig')

    if (plt == "Darwin"):
        df.to_csv("/Users/" + username + "/Downloads/" +
                  input_filename + ".csv", index=False, encoding='utf-8-sig')


def toMySQL(df):
    mysql_username = os.environ.get("DB_USER")
    mysql_password = os.environ.get("DB_PASS")

    db_name = "BB"
    con = sq.create_engine("mysql+pymysql://" + mysql_username + ":" + mysql_password + "@localhost/" + db_name)

    df.to_sql("BB_Table", con, index=False, if_exists="replace")


def selectExportOption(df):
    optionMenu = '\nExport Options:\n1.) To CSV File\n2.) To MySQL Database\n\nPlease type option number (or "q" to quit program) and hit enter: '
    finished = False
    while not finished:
        selection = input(optionMenu) or "0"
        
        if selection.lower() == "q":
            quit() 

        elif selection == "1":
            toCSV(df)
            print("DONE: CSV file is in your downloads folder")
            break

        elif selection == "2" and installed:
            toMySQL(df)
            print("DONE: Data was sent to MySQL database and stored")
            break

        elif selection == "2" and not installed:
            print(
                "ERROR: Module 'sqlalchemy' is not installed only option CSV is available")

        elif selection != ("1" or "2"):
            print('ERROR: Invalid selection please type either "1" or "2" to complete (or "q" to quit program)')


def main():
    print("*************************BESTBUY_WEB_SCRAPER*************************\n")

    session = HTMLSession()

    baseUrl = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=microwavetypesv_facet%3DMicrowave%20Type~Countertop&sc=Global&st=microwave&type=page&usc=All%20Categories"

    max_pagenum = int(session.get(baseUrl).html.find("ol.paging-list > li:nth-last-child(1)", first=True).text)

    input_pagenum = inputPageNum(max_pagenum)
    webpages = range(1, input_pagenum + 1)

    print("\nLoading...")

    scrapeData(webpages, session, baseUrl)

    df = pd.DataFrame(data_dict)

    previewDataOption(df)

    selectExportOption(df)


price = [] 
brand = []
model = []
color_material = []

data_dict = {"brand": brand, "description": model, "color_material": color_material, "price": price}

main()
