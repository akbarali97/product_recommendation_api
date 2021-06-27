def db(articletype:str, color):
    import sqlite3
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        result = cur.execute(f"""SELECT * 
                                FROM styles 
                                WHERE (articleType LIKE '%{articletype}%' AND baseColour='{color}') OR
                                articleType LIKE '%{articletype}%'
                                """)
        return list(result)