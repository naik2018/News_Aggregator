from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# GEtting news from Times of India

toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

# anchors = toi_soup.find_all('div',attrs={"class":"brief_box"})
toi_headings = toi_headings[0:-13] # removing footers
toi_news = []
toi_news_imgs = []


for th in toi_headings:
    toi_news.append(th.text)
x=toi_soup.find_all('img')
# print(x)
for i in x:
    s=str(i)
    ind=s.find('data-src')
    ind2=s.find('onerror')
    if (ind == -1):
        pass
    else:
        toi_news_imgs.append(s[ind+10:ind2-2])

toi_anchors=[]
toi_anchors2=[]
toi_anchors3=[]
for data in toi_soup.find_all('div', class_='brief_box'):
	for a in data.find_all('a'):
        	if len(a.get('href'))>20:
        		toi_anchors.append(a.get('href'))
 
for i in toi_anchors:
	if i not in toi_anchors2:
		toi_anchors2.append(i)
for i in toi_anchors2:
    i="https://timesofindia.indiatimes.com/india/"+str(i)
    toi_anchors3.append(i)

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
ht_r = requests.get("https://www.hindustantimes.com/india-news/", headers=agent)

ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.find_all("div", {"class": "media-heading headingfour"})
# ht_headings = ht_headings[2:]
ht_titles = []
ht_anchors=[]
for i in ht_headings:
	for a in i.find_all('a'):
		ht_anchors.append(a.get('href'))
		ht_titles.append(a.get('title'))

ht_img = ht_soup.find_all("div", {"class": "media-left"})

ht_imgs=[]
for i in ht_img:
	for a in i.find_all('img'):
		ht_imgs.append(a.get('src'))

zipped_data=zip(toi_news[2:],toi_news_imgs,toi_anchors3)
zipped_data2=zip(ht_anchors,ht_titles,ht_imgs[3:])

ndtv = requests.get("https://www.ndtv.com/latest")
ndtv_soup = BeautifulSoup(ndtv.content, 'html5lib')
ndtv_anchors=[]
ndtv_titles=[]
ndtv_imgs=[]

for data in ndtv_soup.find_all('h2', class_='nstory_header'):
	for a in data.find_all('a'):
		ndtv_anchors.append(a.get('href'))
		ndtv_titles.append(a.get('title'))
		
for data in ndtv_soup.find_all('div', class_='new_storylising_img'):
	for a in data.find_all('img'):
		ndtv_imgs.append(a.get('src'))

zipped_data3=zip(ndtv_titles,ndtv_anchors,ndtv_imgs)


def home(req):
    return render(req, 'news/home.html',{'zip_data':zipped_data,'zip_data2':zipped_data2,'zip_data3':zipped_data3})