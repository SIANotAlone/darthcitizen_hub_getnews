
from get_news import *
# from async_get_news import *



if __name__ == "__main__":
    print("application starting...")
    news = Get_news()
    # news = Get_news()
    news.get_all_news()