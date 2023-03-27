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