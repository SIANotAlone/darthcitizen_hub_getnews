import asyncpg


class DbManager:
    def __init__(self) -> None:
        pass

    async def save_news(self, data: list, origin="origin"):
        SCHEMA = "allnews"

        # Установка соединения с базой данных
        conn = await asyncpg.connect(
            host="localhost",
            database="news",
            user="postgres",
            password="12345678",
            options=f"-c search_path={SCHEMA}"
        )

        data.reverse()

        count = 0
        async with conn.transaction():
            for news in data:
                sql = f"SELECT url FROM games_news WHERE url = '{news.url}'"
                rows = await conn.fetch(sql)

                if not rows:
                    sql = "INSERT INTO games_news (title, short, origin, url, preview, time) VALUES ($1, $2, $3, $4, $5, $6)"
                    context = (news.title, news.short, news.origin, news.url, news.preview, news.time)
                    await conn.execute(sql, *context)
                    count += 1

        if origin == "origin":
            print(f"[INFO] {count} records added to database")
        else:
            print(f"[INFO] {count} records added to database from {origin}")

        # Закрытие соединения
        await conn.close()



