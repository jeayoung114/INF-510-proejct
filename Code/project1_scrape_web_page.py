### scraping Famous burger restaurant name and famous burger from https://www.timeout.com/los-angeles/restaurants/the-best-burgers-in-los-angeles
from bs4 import BeautifulSoup
import urllib
import requests
print("#################name scraping################")
url = 'https://www.timeout.com/los-angeles/restaurants/the-best-burgers-in-los-angeles'
res = requests.get(url)
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('a')
key = []
name = []
famous = []
count = 0
for tag in tags:

    # tag=tag.get_text()
    tag = str(tag)
    start = tag.find("prop60")
    end = tag.find("eVar60")
    if start != -1:
        title = tag[start + 9:end - 3]
        title = str(title)
        title = title.replace("\\u2019", '\'')
        title = title.replace("\\u2018", '\'')
        title = title.replace("\\u00f1", 'n')
        if title not in key:
            count += 1
            key.append(title)
            at = title.find("at ")
            famous.append(title[:at])
            name.append(title[at + 3:])

key = key[:-2]
famous = famous[:-2]
name = name[:-2]
for i in key:
    print(i)
print("#####################################")
for i in famous:
    print(i)
print("#####################################")
for i in name:
    print(i)

    #     print(start)
print("#################url scraping####################")
url = 'https://www.timeout.com/los-angeles/restaurants/the-best-burgers-in-los-angeles'
res = requests.get(url)
soup = BeautifulSoup(html, 'html.parser')
tags = soup('a')
link = []
count = 0
for tag in tags:

    get_link = tag.get('href')
    get_link = str(get_link)
    #     print(get_link)
    if get_link.startswith('/los-angeles/restaurants/') or get_link.startswith(
            '/los-angeles/bars/') or get_link.startswith('/los-angeles/shopping/'):
        if get_link not in link:
            link.append(get_link)

for i in range(len(link)):
    link[i]='https://www.timeout.com'+link[i]
###the last one was not about restaurants
link=link[:-1]

for i in link:
    print(i)


print("#################rating scraping####################")
star_in_site=[]
for i in link:
    star_rating='no rating'
#     print(i)
#     url='https://www.timeout.com/los-angeles/bars/everson-royce-bar'
#     res=requests.get(i)
    html =  urllib.request.urlopen(i).read()
    soup=BeautifulSoup(html, 'html.parser')
    tags = soup.findAll("span",{"class":"sr-only"})
    for tag in tags:
        tag=str(tag)
        star=tag.find("stars")
        if star!=-1:
    #         print(tag)
    #         print(star)
            star_rating=(tag[star-11:star-10])
    star_in_site.append(star_rating)

print("##############review scraping###############")

review=[]
for url in link:
# url='https://www.timeout.com/los-angeles/bars/everson-royce-bar'
    res=requests.get(url)
    html =  urllib.request.urlopen(url).read()
    soup=BeautifulSoup(html, 'html.parser')
    tags = soup.findAll("div",{"itemprop":"reviewBody"})
    review_page=''
    for tag in tags:
        tag=tag.get_text()
        tag.strip()
        review_page+=tag
    review.append(review_page)



print("####################address scraping##############")

address=[]
for url in link:
# url='https://www.timeout.com/los-angeles/bars/everson-royce-bar'
    res=requests.get(url)
    html =  urllib.request.urlopen(url).read()
    soup=BeautifulSoup(html, 'html.parser')
    tags = soup.findAll("td",{"class":"xs-px0 sm-full-width"})
    # review_page=''
    for tag in tags:
        tag=tag.get_text()
        tag=str(tag)
        tag=tag.strip()
        print(tag)
        tag=repr(tag).replace('\\n','').replace('  ','')
        break
    address.append(tag)



print("####################web address scraping###############")

web_address=[]
for url in link:
#     url='https://www.timeout.com/los-angeles/bars/everson-royce-bar'
    res=requests.get(url)
    html =  urllib.request.urlopen(url).read()
    soup=BeautifulSoup(html, 'html.parser')
    tags = soup.findAll("tr",{"data-order":'6'})

    for tag in tags:
        tag=str(tag)
        hr=tag.find('href')
        hre=tag.find('rel')
        if hr==-1 or hre==-1:
            web_address.append("no_website")
        else:
            web_address.append(tag[hr+6:hre-2])
print(web_address)



print("############merging data#############")
num=[]
for i in range(len(name)):
    num.append(i)


data=[]
data.append(num)
data.append(key)
data.append(name)
data.append(famous)
data.append(link)
data.append(star_in_site)
data.append(web_address)
data.append(address)
data.append(review)

print("#################to csv###############")

import pandas as pd

df = pd.DataFrame.from_records(data)
df=df.rename(index={0: "num", 1: "keyword",2:"name",3:"famous_for",4:"link",5:"rating_in_site",6:"website",7:"address",8:"review"})
df=df.transpose()
df.to_csv("../Dataset/1_crawled_data.csv",index=0,index_label='num')