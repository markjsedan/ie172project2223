import dbconnect as db
from datetime import datetime

def addfewgenres():
    sqlcode = """ INSERT INTO genres (
        genre_name,
        genre_modified_date,
        genre_delete_ind
    )
    VALUES (%s, %s, %s)"""

    db.modifydatabase(sqlcode, ['Academic', datetime.now(), False])


sql_resetgenres = """
    TRUNCATE TABLE genres RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetgenres, [])
addfewgenres()

sql_query = """ SELECT * FROM genres"""
values = []
columns = ['id', 'name', 'modified', 'is_deleted']
df = db.querydatafromdatabase(sql_query, values, columns) # or print(db.querydatafromdatabase(sql_query, values, columns))
print(df)
