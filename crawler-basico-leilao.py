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
# get pages - Ok 
# get iten - Ok
# estruturar laços - Ok

# look for pages
def get_pages(first_page):    
    item_response = get(first_page)
    item_soup = BeautifulSoup(item_response.text, 'html.parser')
    
    page_list = []
    for li in item_soup.find(class_="pagination"):
        if li.text == "»":
            break
        page_list.append('https://www.freitasleiloeiro.com.br/leiloes/pesquisar?pg=' + li.text + '&categoria=1&subCategoria=3&subCategoriaLabel=Motos&patio=17')

    for i in range(len(page_list)):
        get_products(page_list[i])

def get_products(page_url):
    item_response = get(page_url)
    item_soup = BeautifulSoup(item_response.text, 'html.parser')

    # look for product
    item_list = []
    for item in item_soup.find_all(class_="btn btn-block btn-primary"):
        item_list.append("https://www.freitasleiloeiro.com.br" + item.get("href"))

    # get details of all products, MAKE THE MAGIC!
    for i in range(len(item_list)):
        print('#' + str(i+1) )
        get_details(item_list[i])
    
# look for details
def get_details(product_url):
    response = get(product_url)
    product_soup = BeautifulSoup(response.text, 'html.parser')
    
    def get_product_lot():
        lot_soup = product_soup.find(id="num-lote")
        product_lot = lot_soup.h4.text 
        return(product_lot)
    
    def get_product_view():
        view_soup = product_soup.find_all(class_="col-sm-1 text-center")
        product_view = view_soup[0].h4.text
        return(product_view)

    def get_name():
        product_name = ' '.join(product_soup.h2.text.split())
        return(product_name)

    def get_bid_number():
        bid_soup = product_soup.find(id="lblTotalLances")
        bid_number = bid_soup.text
        return(bid_number)

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
        # tenta pegar o valor na página de lances, senão houver, ele pela o lance inicial
        try:
            # remove simbolo monetario e centavos, após isto converte para inteiro
            product_bid_price = int(bid_soup.h2.text[3:-3].replace('.',''))
        
        except:
            bid_soup2 = product_soup.find(class_="table table-striped")
            # remove espaços vazios, e depois o simbolo monetario e centavos, após isto converte para inteiro
            product_bid_price = int(' '.join(bid_soup2.td.text.split())[3:-3].replace('.',''))
        return(product_bid_price)

    def get_bid_username():
        bid_soup = get_bid_soup()
        product_bid_username = bid_soup.find_all("tr")[0].td.text
        return(product_bid_username)

    def get_bid_type():
        bid_soup = get_bid_soup()
        product_bid_type = bid_soup.find_all("tr")[2].td.text
        return(product_bid_type)

    def get_bid_date():
        bid_soup = get_bid_soup()
        product_bid_date = bid_soup.find_all("tr")[1].td.text
        return(product_bid_date)
    
    #print(get_product_lot())
    #print(get_product_view())
    #print(get_name())
    #print(get_bid_number())
    #print(get_bid_price())
    ## Se não houver lances, não imprime informações do lance
    #if get_bid_number() != '0':
    #    print(get_bid_username())
    #    print(get_bid_type())
    #    print(get_bid_date())
    #print('-' * 5 )

    dataline = [ get_product_lot(), get_name(), get_product_view(), get_bid_number(), get_bid_price() ]
    print(type(dataline))
    print(dataline)


#get_details('https://www.freitasleiloeiro.com.br/leiloes/lote?leilaoid=3805&lote=258')
#get_details('https://www.freitasleiloeiro.com.br/leiloes/lote?leilaoid=3805&lote=253')


#print(type(dataline))
#print(dataline)

get_pages('https://www.freitasleiloeiro.com.br/leiloes/pesquisar?pg=1&categoria=1&subCategoria=3&subCategoriaLabel=Motos&patio=17')
