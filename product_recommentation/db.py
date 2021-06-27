def db(articletype:str, color):
    import sqlite3
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    query = f'SELECT * FROM styles WHERE articleType={articletype} AND baseColor={color}'
    result = cur.execute(query)
    con.close()
    return list(result)