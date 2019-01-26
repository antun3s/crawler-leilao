#!/usr/bin/env python
# coding: utf-8

from requests import get
from bs4 import BeautifulSoup
import re

url = 'https://www.freitasleiloeiro.com.br/leiloes/pesquisar?query=&categoria=2&subCategoria=&subCategoriaLabel=&estado=&cidade=&faixaValor=3&faixaValorLabel=De%20R$%2025.000%20At%C3%A9%20R$%2050.000&condicao=&patio='
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')

lista_item = html_soup.find(id='table_agenda_body')

# find abaixo busca pelo class específica
rows = lista_item.find_all(class_ ='cursor-pointer')

i = 0
for row in rows:
    item = rows[i]

    # data_hora_consulta
    data_hora_consulta = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # captura Lote
    lote=item.h3.text

    # extrai os dados de texto longo e separado em linhas
    # captura todo o texto da div que tem a "class text-justify"
    nome_bruto=item.find("div",{"class":"text-justify;"}).text
    # separa linha do data_hora do leilao
    nome_bruto = re.sub(' - ', '\n',nome_bruto)
    # remove espaços repetidos
    nome_bruto= re.sub(' +', ' ',nome_bruto)
    # separa o nome bruto, cada linha vira um item de lista
    nome_bruto = nome_bruto.splitlines()
    
    # captura data_hora do leilao
    data_hora_leilao = nome_bruto[1]
    
    # captura local do leilao
    local = nome_bruto[2]
    
    # captura nome do item em leilao
    nome = nome_bruto[5]
    
    # Lance
    # Coleta lance com R$ e remove o . do milhar
    lance = item.tr.td.text.replace('.','')
    # prepara a string
    lance = lance[3:].replace(',','.')
     
    #Imprime no log
    with open('consulta.log', 'a') as consulta:
        consulta.write('"{}","{}","{}","{}","{}","{}";\n'.format(data_hora_consulta,lote,data_hora_leilao,local,nome,lance))
    
    i = i + 1    
