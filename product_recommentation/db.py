import sqlite3

def db(articletype:str, colors: tuple = None):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    query = f'SELECT * FROM styles WHERE articleType={articletype} OR baseColor={color}'
    result = cur.execute(query)
    con.close()
    return list(result)