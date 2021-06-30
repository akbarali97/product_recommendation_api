def db(articletype:str, colors):
    import sqlite3
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        result = cur.execute(f"""SELECT DISTINCT *
                                FROM styles 
                                WHERE (articleType LIKE '%{articletype}%' AND (baseColour LIKE '%{colors[0]}%' OR baseColour LIKE '%{colors[1]}%' OR baseColour LIKE '%{colors[2]}%'))
                                OR (articleType LIKE '%{articletype}%')
                                """)
        return list(result)