import psycopg2


class DbManager:
    def __init__(self) -> None:
        pass

    def save_news(self, data:list):
        SCHEMA = "allnews"


        conn = psycopg2.connect(
        host="localhost",
        database="news",
        user="postgres",
        password="12345678",
        options=f"-c search_path={SCHEMA}"
    )

     
        cur = conn.cursor()

       

        for news in data:
            sql = f"SELECT url FROM news WHERE url = '{news.url}'"
            cur.execute(sql)
            rows = cur.fetchall()
        
            if rows==[]:
                sql = "INSERT INTO news (title, short, origin, url, preview, time) VALUES (%s, %s, %s, %s, %s, %s)"
                context = (news.title,news.short, news.origin,news.url,news.preview,news.time)
                cur.execute(sql, context)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()