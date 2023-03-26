
from bs4 import BeautifulSoup
import requests
import time
import datetime
from googletrans import Translator
import psycopg2
from models import News_item


class Get_news:
    def __init__(self) -> None:
        pass
    


    def get_all_news(self):
        playua = self.__get_news_playua()
        pcgamer = self.__get_news_pcgamer()
        

        data = []
        data.extend(playua)
        data.extend(pcgamer)


        self.__write_to_db(data)


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
            #print(n)
        #print(News_list[0].title)
        return News_list

        # allNews = soup.findAll('article', class_='short-article')
        # print(allNews)


    def __get_news_pcgamer(self)->list:
        html_doc = requests.get("https://www.pcgamer.com/news/")
        soup = BeautifulSoup(html_doc.text, "html.parser")
        allNews = soup.findAll('a', class_='article-link')
        
        News_list = []

        allNews = soup.find("div",class_="listingResults news")
        
        for article in allNews.find_all("div",class_="listingResult"):
            ##title = article.find("a", class_='article-link').get("aria-label")
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




    def __translate_text(self,text:str):
        translator = Translator(service_urls=['translate.google.com'])
        result = translator.translate(text, dest='uk')
        return result.text    
    

    def __write_to_db(self, data:list):
        schema = "allnews"


        conn = psycopg2.connect(
        host="localhost",
        database="news",
        user="postgres",
        password="12345678",
        options=f"-c search_path={schema}"
    )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a query
        cur.execute("SELECT * FROM news")

        # Fetch the query results
        rows = cur.fetchall()

        # Print the results
        #print(rows)

        todb = []
        for news in data:
            context = (news.title,news.short, news.origin,news.url,news.preview,news.time)
            todb.append(context)

        sql = "INSERT INTO news (title, short, origin, url, preview, time) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.executemany(sql, todb)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()