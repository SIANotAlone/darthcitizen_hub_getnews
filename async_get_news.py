import asyncio

import aiohttp
from googletrans import Translator
from models import News_item
from bs4 import BeautifulSoup
import time


from database import DbManager

async def translate_text(text:str):
    try:
        translator = Translator(service_urls=['translate.google.com'])
        result = translator.translate(text, dest='uk')
        return result.text 
    except: 
        return text
    


async def ign(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('a', class_='item-body')
    News_list = []
    for item in news:
        
        title = item.get('aria-label')
        short = 'None'
        preview = item.find('div').find('img').get('src')
        url = 'https://www.ign.com' + item.get('href')
        origin = 'IGN'
        now = time.time()
        if title != None:
            news_ = News_item(title,short,url,preview,now,origin)
            News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def kotaku(data, site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('article')

    News_list = []
    for item in news:
        title = item.find('h2')
        try:
            title = item.find('h2').get_text(strip=True)
        except Exception as e:
            continue
        try:
            short = item.find('p').text
        except Exception as e:
            continue
        urls = item.find_all('a')
        origin = 'KOTAKU'
        now = time.time()
        preview = ''
        try:
            preview = item.find('img').get('data-src')
        except:
            pass
        url = ''
        i = 0

        for val in urls:
            try:
                val.get('href')
                i += 1
                if i == 3:
                    url = val.get('href')
                # print(url)
            except:
                pass
        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def nv(data, site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('div', class_='row-result')
    News_list = []
    for item in news:
        title = item.find('div', class_='title').text.strip()
        short = item.find('div', class_='subtitle').text.strip()
        url = item.find('a').get('href')
        preview = 'https://static.nv.ua/images/main/nv_logo_new.svg?q=85&f=png&stamp=4.166'
        origin = 'New Voice(NV)'
        now = time.time()
        news_ = News_item(title, short, url, preview, now, origin)
        News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def engadget(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('article')
    News_list = []
    for item in news:
        title = item.find('h2').text
        url = 'https://www.engadget.com'+ item.find('h2').find('a').get('href')
        preview = item.find('img').get('src')
        short = item.find('div', class_='D(f) Fld(c) Ai(fs)').find('div').text
        origin = 'engadget'
        now = time.time()
        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def stopgame(data, site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find('div', id='w0').find('div').find_all('div', class_='_card_1vlem_1')
    News_list = []
    for item in news:
        title = item.find('a', class_='_title_1vlem_60').text
        short = ''
        origin = 'Stopgame'
        url = 'https://stopgame.ru' + item.find('a', class_='_title_1vlem_60').get('href')
        preview = item.find('picture').find('img').get('src')
        tags = item.find('div', class_='_tags_1vlem_100').find_all('a')
        for index, tag in enumerate(tags):
            if index + 1 < len(tags):
                short += tag.text + ', '
            else:
                short += tag.text + '.'
        now = time.time()
        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def gagadget(data,site):
    
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('div', class_='l-grid_3')
    News_list = []
    for item in news:
        title = item.find('span', class_='cell-title').find('a').text
        preview = 'https://gagadget.com' + item.find('img', class_='b-respon-img').get('src')
        url = 'https://gagadget.com' + item.find('a', class_ = 'b-indexnode__comments b-indexnode__comments_cell').get('href')
        short = "None"
        origin = 'gagadget'
        now = time.time()
        
        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)

    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def gameverse(data, site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('a', class_='post')
    News_list = []
    for item in news:
        title = item.find('p', class_='title').text
        short = item.find('p', class_='description').text
        origin = 'Gameverse'
        url = 'https://gameverse.com.ua' + item.get('href')
        preview = 'https://gameverse.com.ua' + item.find('img').get('src')
        now = time.time()

        news_ = News_item(title, short, url, preview, now, origin)
        News_list.append(news_)
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def tv24(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.findAll('article')
    i=0
    News_list = []
    for item in news:
        i+=1
        title  = item.find('div', class_='news-title').find('a').text
        short = 'None'
        preview = 'https://upload.wikimedia.org/wikipedia/commons/0/04/24_Kanal_logo.svg'
        origin = "24tv.ua"
        url = item.find('div', class_='news-title').find('a').get('href')
        now = time.time()
        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
        if i > 12:
            break
    manager = DbManager()
    manager.save_news(News_list, origin=site)



async def geeknews(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.findAll('div', class_='short-item')
    News_list = []
    for item in news:
        try:
            title = item.find('a',class_='short-title').text
            url = item.find('a',class_='short-title').get('href')
            short = item.find('div', class_='short-text').text
            preview = 'https://geeks.news' + item.find('a', class_='short-img img-fit').find('img').get('data-src')
            origin = 'geek.news'
            now = time.time()
            news_ = News_item(title,short,url,preview,now,origin)
            News_list.append(news_)
        except Exception as e:
            pass
    manager = DbManager()
    manager.save_news(News_list, origin=site)

      

async def uaplay(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('article')
    News_list = []
    for item in news:
        title = item.find('h4', class_='entry-title title').find('a').text
        short = item.find('div',class_='mg-content').find('p').text
        url = item.find('h4', class_='entry-title title').find('a').get('href')
        preview = item.find('div').find('div').get('data-back')
        origin = 'uaplay.com.ua'
        now = time.time()

        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)

    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def itc(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('div', class_='row')
    i=0
    News_list = []
    for item in news:
        
        title = item.find('a').text
        short = item.find('div', class_='entry-excerpt').text
        url = item.find('a').get('href')
        preview = item.find('div', class_='col-img-in').find('a').get('data-bg')
        origin = 'ITC'
        now = time.time()

        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
    
        i+=1
        if i>50:
            break
    # print(site)
    # print(News_list)
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def gameua(data,site):
    
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('article')
    News_list = []
    i=0
    for item in news:
        title = item.find('h2').find('a').text
        short = item.find('div', class_='post-excerpt').find('p').text
        preview = item.find('div',class_='featured-image').find('a').find('span').get('data-src')
        url = item.find('div',class_='featured-image').find('a').get('href')
        origin = 'gameua.com.ua'
        now = time.time()

        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)
    
       
        i+=1
        #only 9 news on the page
        if i>8:
            break
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def root_nation(data,site):
    html = BeautifulSoup(data, 'html.parser')
    news = html.find_all('div', class_='td-module-container td-category-pos-image')
    News_list = []
    for item in news:
        title = item.find('p', class_='entry-title td-module-title').find('a').text
        short = item.find('div', class_='td-excerpt').text
        url = item.find('p', class_='entry-title td-module-title').find('a').get('href')
        preview = 'https://root-nation.com/wp-content/uploads/2022/05/rn-material-logo-web-180p-02.png'
        origin = 'root-nation.com'
        now = time.time()

        news_ = News_item(title,short,url,preview,now,origin)
        News_list.append(news_)

    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def playua(data, site):
    soup = BeautifulSoup(data, "html.parser")
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
    
    #print('playua: '+str(News_list))
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def pcgamer(data,site):
    soup = BeautifulSoup(data, "html.parser")
    allNews = soup.findAll('a', class_='article-link')
    
    News_list = []

    allNews = soup.find("div",class_="listingResults news")
    
    for article in allNews.find_all("div",class_="listingResult"):
        try:

            title = article.find("a", class_="article-link").get("aria-label")
            short = article.find("p", class_="synopsis").get_text()
            url = article.find("a", class_="article-link").get("href")
            preview = article.find("figure", class_="article-lead-image-wrap").get("data-original")
            cur_time = time.time()
            origin = "PCGAMER"
            
            news = News_item(title,short,url,preview,cur_time,origin)
            News_list.append(news)


        except Exception as e:
            pass

        
    #print('pcgamer: ' + str(News_list))
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def gamespot(data, site):
    soup = BeautifulSoup(data, "html.parser")
    News_list = []
    allNews = soup.find_all("div",class_="card-item base-flexbox flexbox-align-center width-100 border-bottom-grayscale--thin")
    for article in allNews:
        title = article.find("h4", class_="card-item__title").text
        short = "None"
        url = "https://www.gamespot.com" + article.find("a", class_="card-item__link text-decoration--none").get("href")
        preview = article.find("img", class_="width-100").get("src")
        cur_time = time.time()
        origin = "gamespot"
        news = News_item(title,short,url,preview,cur_time,origin)
        News_list.append(news)

    #print('pcgamer: '+str(News_list))
    manager = DbManager()
    manager.save_news(News_list, origin=site)


async def gameinformer(data,site):
    soup = BeautifulSoup(data, "html.parser")
    News_list = []
    
    allNews = soup.find("div", class_="views-infinite-scroll-content-wrapper clearfix")
    
    for article in allNews:
        try:
            title = article.find("h2", class_='page-title').find("span").text
            short = article.find("div", class_='field field--name-field-promo-summary field--type-string field--label-hidden gi5-field-promo-summary gi5-string field__item').text
            url = "https://www.gameinformer.com" + article.find("div", class_="promo-img-thumb").find("a").get("href")
            preview = "https://www.gameinformer.com" + article.find("img").get("src")
            cur_time = time.time()
            origin = "gameinformer"
            news = News_item(title,short,url,preview,cur_time,origin)
            News_list.append(news)
        except Exception as e:
            pass
    #print('gameinformer: '+str(News_list))
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def unian(data, site):
    soup = BeautifulSoup(data, "html.parser")
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
    manager = DbManager()
    manager.save_news(News_list, origin=site)

async def get_data(context):
    if context['site'] == 'playua':
        await playua(context["data"],site = context['site'])
    elif context['site'] == 'pcgamer':
        await pcgamer(context["data"],site = context['site'])
    elif context['site'] == 'gamespot':
        await gamespot(context["data"],site = context['site'])
    elif context['site'] == 'gameinformer':
        await gameinformer(context["data"],site = context['site'])
    elif context['site'] == 'unian':
        await unian(context["data"],site = context['site'])
    elif context['site'] == 'gagadget':
        await gagadget(context["data"],site = context['site'])
    elif context['site'] == '24tv':
        await tv24(context["data"],site = context['site'])
    elif context['site'] == 'geek.news':
        await geeknews(context["data"],site = context['site'])
    elif context['site'] == 'uaplay':
        await uaplay(context["data"],site = context['site'])
    elif context['site'] == 'ITC':
        await itc(context["data"],site = context['site'])
    elif context['site'] == 'gameua':
        await gameua(context["data"],site = context['site'])
    elif context['site'] == 'root-nation':
        await root_nation(context["data"],site = context['site'])
    elif context['site'] == 'ign':
        await ign(context["data"],site = context['site'])
    elif context['site'] == 'kotaku':
        await kotaku(context["data"],site = context['site'])
    elif context['site'] == 'engadget':
        await engadget(context["data"],site = context['site'])
    elif context['site'] == 'New Voice(NV)':
        await nv(context["data"],site = context['site'])
    elif context['site'] == 'Gameverse':
        await gameverse(context["data"],site = context['site'])
    elif context['site'] == 'Stopgame':
        await stopgame(context["data"],site = context['site'])
        
    

async def main():
    async with aiohttp.ClientSession() as session:
        start = time.time()
        tasks = [
            {"site":"playua","url":"https://playua.net/novyny/"},
            {"site":"pcgamer","url":"https://www.pcgamer.com/news/"},
            {"site":"gamespot","url":"https://www.gamespot.com/news/"},
            {"site":"gameinformer","url":"https://www.gameinformer.com/news"},
             {"site":"unian","url":"https://www.unian.ua/games"},
             {"site":"gagadget","url":"https://gagadget.com/uk/news/games/"},
             {"site":"24tv","url":"https://games.24tv.ua/"},
             {"site":"geek.news","url":"https://geeks.news/igrovi-novyny/"},
             {"site":"uaplay","url":"https://uaplay.com.ua/"},
             {"site":"ITC","url":"https://itc.ua/ua/igri/"},
             {"site":"gameua","url":"https://gameua.com.ua/news/"},
             {"site":"root-nation","url":"https://root-nation.com/ua/games-ua/"},
             {"site":"ign","url":"https://www.ign.com/?filter=games"},
             {"site":"kotaku","url":"https://kotaku.com/culture/news"},
             {"site":"engadget","url":"https://www.engadget.com/gaming/"},
             {"site": "New Voice(NV)", "url": "https://nv.ua/ukr/tags/videoihry.html"},
             {"site": "Gameverse", "url": "https://gameverse.com.ua/news/"},
            {"site": "Stopgame", "url": "https://stopgame.ru/news"}
            ]
        user_agent = {'User-agent': 'Mozilla/5.0'}
        for task in tasks:
            async with session.get(task['url'], headers=user_agent) as response:
                html = await response.text()
                try:
                    await get_data(context = {"site":task["site"], "data": html})
                except:
                    site = task["site"]
                    print(f"[WARN] Some thing wrong with {site}.")
        end=time.time()
        time_for_scrapping = end - start
        time_spent = '%.2f' % time_for_scrapping
        print(f"[INFO] News was scraped, time: {time_spent} seconds")

# Python 3.7+
asyncio.run(main())
