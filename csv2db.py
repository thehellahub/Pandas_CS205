import sqlite3
import pandas as pd
import csv
import os

def csvtodb():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    sql_string = ''' CREATE TABLE if NOT EXISTS movies(
    id int,
    title Text,
    year Text,
    rank Text
    ); '''

    cur.execute(sql_string)

    sql = "SELECT * FROM movies;"

    # Now let's fetch our result set and load it into a pandas dataframe
    df = pd.read_sql_query(sql, conn)

    print("My tables columns are: ")
    print(df.columns.tolist())

    count = 0
    with open('movies.csv') as csvfile:
        for row in csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if count > 0:
                id = str(row[0]).strip()
                title = str(row[1]).strip()
                year = str(row[2]).strip()
                rank = str(row[3]).strip()

                if len(id)==0:
                    id= 'NaN'
                if len(title)==0:
                    title='NaN'
                else:
                    print(title)
                    #if title[0] == "'":
                    #    title = title [1:]
                    #if title[len(title)-1] == "'":
                    #    title = title[:-1]
                    title = title.replace("'","''")
                    print(title)
                if len(year)==0:
                    year = 'NaN'
                if len(rank)==0:
                    rank='NaN'

                sql_insert = "INSERT INTO movies ('id', 'title', 'year', 'rank') VALUES ('"+id+"','"+title+"','"+year+"','"+rank+"');"

                try:
                    cur.execute(sql_insert)
                except Exception as e:
                    print(sql_insert)
                    print(e)
                    return
            count+=1

    sql = "SELECT * FROM movies;"

    # Now let's fetch our result set and load it into a pandas dataframe
    df = pd.read_sql_query(sql, conn)

    print("\nMy movies table is: ")
    print(df)

    print("\nLength of movies table is:")
    print(len(df))




    conn.commit()
    conn.close()
    os.remove("database.db")


csvtodb()
