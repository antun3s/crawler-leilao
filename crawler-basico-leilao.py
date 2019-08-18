from requests import get
from bs4 import BeautifulSoup
import re


# get product-lot - Ok
# get product-views - Ok
# get product-bid - Ok 
# get product-name - Ok
# get product-actual-price - Ok
# get bid-username - Ok
# get bit-type - Ok

product_url = 'https://www.freitasleiloeiro.com.br/leiloes/lote?leilaoid=3790&lote=36'
response = get(product_url)
product_soup = BeautifulSoup(response.text, 'html.parser')

def get_product_lot():
    lot_soup = product_soup.find(id="num-lote")
    product_lot = lot_soup.h4.text 
    print(product_lot)

def get_product_view():
    view_soup = product_soup.find_all(class_="col-sm-1 text-center")
    product_view = view_soup[0].h4.text
    print(product_view)

def get_bid_number():
    bid_soup = product_soup.find(id="lblTotalLances")
    print(bid_soup.text)

def get_name():
    product_name = ' '.join(product_soup.h2.text.split())
    print(product_name)

def get_bid_soup():
    # busca por scripts do tipo "text/javascript"
    price_soup = product_soup.find_all("script", type="text/javascript")
    # dentro do script ele busca a linha com o link do lance, e converte de lista para string
    bid_url = ''.join(map(str,(re.findall('"([^"]*)"',re.findall('.*lanceslote.*',price_soup[1].text)[0]))))
    bid_url = "https://www.freitasleiloeiro.com.br/" + bid_url
    # print(bid_url)
    bid_response = get(bid_url)
    bid_soup = BeautifulSoup(bid_response.text, 'html.parser')
    return(bid_soup)

def get_bid_price():
    bid_soup = get_bid_soup()
    # remove simbolo monetario e centavos, após isto converte para inteiro
    product_bid_price = int(bid_soup.h2.text[3:-3].replace('.',''))
    print(product_bid_price)

def get_bid_username():
    bid_soup = get_bid_soup()
    product_bid_username = bid_soup.find_all("tr")[0].td.text
    print(product_bid_username)

def get_bid_type():
    bid_soup = get_bid_soup()
    product_bid_type = bid_soup.find_all("tr")[2].td.text
    print(product_bid_type)

def get_bid_date():
    bid_soup = get_bid_soup()
    product_bid_date = bid_soup.find_all("tr")[1].td.text
    print(product_bid_date)

get_product_lot()
get_product_view()
get_bid_number()
get_name()
get_bid_price()
get_bid_username()
get_bid_type()
get_bid_date()
