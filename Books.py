import pandas as pd

import requests
from bs4 import BeautifulSoup
import re


URL_list=['https://www.libri.hu/fooldal/sikerlistak/cat/',]

for i in range (2,4):
    URL_basic = "https://www.libri.hu/fooldal/sikerlistak/cat/"
    URL_list.append(URL_basic+'?page='+str(i))

titles_df=[]
prices_df=[]
categories_df=[]
years_df=[]

for URL in URL_list:
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, features="lxml")  


    titles=[]
    prices=[]
    links=[]

    #get book title
    for a in soup.findAll('a',href=True, attrs={'class':'book-title gtm-click'}):
        links.append('https://www.libri.hu' + a['href'])  #create links for detailed info
        titel = ""
        text = a.get_text()
        for line in text.splitlines():  # line-wise
            line = line.strip()  # remove whitespace
            titel += line  # add to address string
        titles.append(titel)

    # get price
    for x in soup.findAll('span',{'class':'act-price'}):
        price = ""
        text = x.get_text()
        for line in text.splitlines():  # line-wise
            line = line.strip()  # remove whitespace
            price += line  # add to address string
        price_integers =re.findall(r'\d+',price)
        if len(price_integers) == 2:
            prices.append((int(price_integers[0]) * 1000) + int(price_integers[1]))
        else:
            prices.append(price_integers[0])


    #get category
    categories=[]
    years=[]
    for link in links:
        category = []
        year=''
        x = requests.get(link)
        local_soup = BeautifulSoup(x.content, features="lxml")

        for a in local_soup.findAll('a', href=True, attrs={'itemprop': 'item'}):
            category.append(a.get_text())
        categories.append(category[-1])
        for y in local_soup.findAll('div', class_="book-datas clearfix"):
            year+=y.get_text()
        start = year.find('Kiadás éve') + 12
        years.append(year[start:(start + 4)])
    titles_df+=titles
    prices_df+=prices
    categories_df+=categories
    years_df+=years


df = pd.DataFrame({'Book':titles_df,'Price':prices_df,'Category':categories_df, 'Publish_year':years_df})

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #print(df)

print(df.describe())







