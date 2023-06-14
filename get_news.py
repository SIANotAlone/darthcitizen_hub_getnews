
from bs4 import BeautifulSoup
import requests
import time
import datetime
from googletrans import Translator
from models import News_item

from database import DbManager
from get_film_news import Get_Film_News

class Get_news:
    def __init__(self) -> None:
        pass
    


    def get_all_news(self):
        playua = self.__get_news_playua()
        pcgamer = self.__get_news_pcgamer()
        #ign = self.__get_news_ign()
        gamespot = self.__get_news_gamespot()
        gameinformer = self.__get_news_gameinformer()
        
        #kotaku = self.__get_news_kotaku()
        unian = self.__get_news_unian()
        #itc = self.__get_news_itc()
        data = []
        data.extend(playua)
        data.extend(pcgamer)
        data.extend(gamespot)
        data.extend(gameinformer)
        data.extend(unian)

        manager = DbManager()
        manager.save_news(data)
        # films = Get_Film_News()
        # films.get()

    def __get_news_playua(self)->list:
        html_doc = requests.get("https://playua.net/novyny/")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        allNews = soup.findAll('article', class_='short-article')
        News_list = []
        
        for n in allNews:
           
            title = n.find("h3").find("a").text
            short = n.text
            url = n.find("a").get("href")
            preview = n.find("img").get("src")
            cur_time = time.time()
            origin = "Playua"

            news_ = News_item(title,short,url,preview,cur_time,origin)
            News_list.append(news_)
        return News_list

    


    def __get_news_pcgamer(self)->list:
        html_doc = requests.get("https://www.pcgamer.com/news/")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        allNews = soup.findAll('a', class_='article-link')
        
        News_list = []

        allNews = soup.find("div",class_="listingResults news")
        
        for article in allNews.find_all("div",class_="listingResult"):
            try:

                title = article.find("a", class_="article-link").get("aria-label")
                title = self.__translate_text(title)
                short = article.find("p", class_="synopsis").get_text()
                short = self.__translate_text(short)
                url = article.find("a", class_="article-link").get("href")
                preview = article.find("figure", class_="article-lead-image-wrap").get("data-original")
                cur_time = time.time()
                origin = "PCGAMER"
                
                news = News_item(title,short,url,preview,cur_time,origin)
                News_list.append(news)


            except Exception as e:
                pass

        return News_list

    #doesn`t worked. Maybe need to use selenium
    def __get_news_ign(self):
        html_doc = requests.get("https://www.ign.com/pc")
        print(html_doc.text)
        soup = BeautifulSoup(html_doc.text, "html.parser")

        allNews = soup.find_all("section", class_="content-feed-grid page-content group-0 even")
        print(all)
        #print(allNews)
        # for article in allNews.findAll("div", class_="content-item"):
        #     title = article.find("a",class_="item-body").get("aria-label")
        #     short = article.find("div",class_="interface")

        #     print(title +  "  " + short)
        return []
    
    def __get_news_gamespot(self)->list:
        
        html_doc = requests.get("https://www.gamespot.com/news/")
      
        soup = BeautifulSoup(html_doc.text, "html.parser")
        News_list = []
        allNews = soup.find_all("div",class_="card-item base-flexbox flexbox-align-center width-100 border-bottom-grayscale--thin")
        for article in allNews:
            title = article.find("h4", class_="card-item__title").text
            title = self.__translate_text(title)
            short = "None"
            url = "https://www.gamespot.com" + article.find("a", class_="card-item__link text-decoration--none").get("href")
            preview = article.find("img", class_="width-100").get("src")
            cur_time = time.time()
            origin = "gamespot"
            news = News_item(title,short,url,preview,cur_time,origin)
            News_list.append(news)
            

        return News_list

    def __get_news_gameinformer(self)->list:
        html_doc = requests.get("https://www.gameinformer.com/news")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        News_list = []
        
        allNews = soup.find("div", class_="views-infinite-scroll-content-wrapper clearfix")
        
        for article in allNews:
            try:
                title = article.find("h2", class_='page-title').find("span").text
                title = self.__translate_text(title)
                short = article.find("div", class_='field field--name-field-promo-summary field--type-string field--label-hidden gi5-field-promo-summary gi5-string field__item').text
                short = self.__translate_text(short)
                url = "https://www.gameinformer.com" + article.find("div", class_="promo-img-thumb").find("a").get("href")
                preview = "https://www.gameinformer.com" + article.find("img").get("src")
                cur_time = time.time()
                origin = "gameinformer"
                news = News_item(title,short,url,preview,cur_time,origin)
                News_list.append(news)
            except Exception as e:
                pass
           
        return News_list



    #doesn`t work. can`t parse
    def __get_news_kotaku(self)->list:
        html_doc = requests.get("https://kotaku.com/culture/news")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        News_list = []
        
        allNews = soup.find("div", class_="sc-17uq8ex-0 fakHlO")
        a = soup.find("div", class_="sc-cw4lnv-13 hHSpAQ")
        for article in a:
            title = article.find("div",class_="sc-cw4lnv-5 dYIPCV")
            print(title)
        
        return []
    

    def __get_news_unian(self)->list:
        html_doc = requests.get("https://www.unian.ua/games")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        News_list = []
        all_News = soup.find("div", class_="games-news")
        for article in all_News:
            title = article.find("a", class_="games-news__title").text
            short = "None"
            url = article.find("a", class_="games-news__title").get("href")
            preview = article.find("a", class_="games-news__image").find("img").get("data-src")
            cur_time = time.time()
            origin = "unian"
            news = News_item(title,short,url,preview,cur_time,origin)
            News_list.append(news)
            
        return News_list
    
    def __get_news_itc(self)->list:
        html_doc = requests.get("https://www.unian.ua/games")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        News_list = []
        all_News = soup.findAll('h2')
        print(all_News)
        
        return []


    def __translate_text(self,text:str):
        try:
            translator = Translator(service_urls=['translate.google.com'])
            result = translator.translate(text, dest='uk')
            return result.text 
        except: 
            return text
    

    