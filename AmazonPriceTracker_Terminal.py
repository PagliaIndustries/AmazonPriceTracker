import requests
from bs4 import BeautifulSoup
import sqlite3
from BX_Constants import (MainDatabase)
from rich import print

#Initializing Currency Symbols to substract it from our string
currency_symbols = ['€', '	£', '$', "¥", "HK$", "₹", "¥", "," ] 

headers = {
'authority': 'www.amazon.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

#------------------------------------------
#            Get Price of Products
#------------------------------------------
#Get the price of each product
def get_price(URL):
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    #Finding the elements
    product_title = soup.find('span', class_ = "a-size-large product-title-word-break").getText()
    product_price = soup.find('span', class_ = "a-offscreen").getText()

    # using replace() to remove currency symbols
    for i in currency_symbols : 
        product_price = product_price.replace(i,'')

    ProductTitleStrip = product_title.strip()
    ProductPriceStrip = product_price.strip()
    print("[bright_yellow]"+ProductTitleStrip)
    print("[bright_cyan]$" + ProductPriceStrip)

    #Converting the string to integer
    product_price = int(float(product_price))
    return(product_price)
#------------------------------------------


#------------------------------------------
#            Get Products to Track
#------------------------------------------
#Connect to the database
connection = sqlite3.connect(MainDatabase)
cursor = connection.cursor()

for Product_Name, URL, my_price in cursor.execute("SELECT Product, URL, Alert_Price FROM AmazonPriceTracker"):
    current_price = get_price(URL)
    if current_price < float(my_price):
        print("[green]You Can Buy This Now!\n")
    else:
        print("[red]The Price Is Too High\n")

connection.close() #Close the connection
#------------------------------------------


