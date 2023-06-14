from models import News_item

from bs4 import BeautifulSoup
import requests
import time
from database import DbManager




class Get_Film_News():
    def __init__(self) -> None:
        pass
        
    def get(self)->list:
        news = []
        unian = self.__unian()
        _24tv = self.__24tv()
        news.extend(unian)
        news.extend(_24tv)
        print(news)
        return news
    
    def __unian(self)->list:

        html_doc = requests.get("https://www.unian.ua/lite/kino")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        allNews = soup.find_all("div", class_="lite-background__item")
        unian = []
        for n in allNews:
            title = n.find("img").get("alt")
            short = None
            url = n.find("a").get("href")
            preview = n.find("img").get("src")
            cur_time = time.time()
            origin = "Unian"
            news_ = News_item(title,short,url,preview,cur_time,origin)
            unian.append(news_)

        return unian
    
    def __24tv(self)->list:
        html_doc = requests.get("https://kino.24tv.ua/")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        allNews = soup.find_all("article", class_="news-card")
        print(allNews)
        news = []
        for n in allNews:
            title = n.find("div", class_="title").find("a").text
            short = None
            url = n.find("a").get("href")
            preview = "https://kino.24tv.ua/" + str(n.find("span", class_="holder").find("div", class_='background-image').get("url"))
            cur_time = time.time()
            origin = "24tv"
            news_ = News_item(title,short,url,preview,cur_time,origin)
            news.append(news_)

        
        return news

