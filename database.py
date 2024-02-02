import psycopg2


class DbManager:
    def __init__(self) -> None:
        pass

    def save_news(self, data:list, origin = "origin"):
        SCHEMA = "allnews"


        conn = psycopg2.connect(
        host="localhost",
        database="news",
        user="postgres",
        password="12345678",
        options=f"-c search_path={SCHEMA}"
    )

        data.reverse()
        cur = conn.cursor()

       
        count = 0
        for news in data:
            sql = f"SELECT url FROM games_news WHERE url = '{news.url}'"
            cur.execute(sql)
            rows = cur.fetchall()
            # if origin=='ITC':
            #
            #     sql = f"SELECT title FROM games_news WHERE origin = 'ITC'"
            #     cur.execute(sql)
            #     rows_itc = cur.fetchall()
            #     # print(rows_itc)
            #     if news.title in rows_itc:
            #         pass
            #     else:
            #         sql = "INSERT INTO games_news (title, short, origin, url, preview, time) VALUES (%s, %s, %s, %s, %s, %s)"
            #         context = (news.title, news.short, news.origin, news.url, news.preview, news.time)
            #         cur.execute(sql, context)
            #
            #         count += 1

            if rows==[]:
                sql = "INSERT INTO games_news (title, short, origin, url, preview, time) VALUES (%s, %s, %s, %s, %s, %s)"
                context = (news.title,news.short, news.origin,news.url,news.preview,news.time)
                cur.execute(sql, context)

                count+=1
        if origin == "origin":
            print(f"[INFO] {count} records added to database")
        else: 
            print(f"[INFO] {count} records added to database from {origin}")
        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()