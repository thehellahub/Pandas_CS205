import sqlite3 as sq
import pandas as pd

#author: Matthew Piatt, Andrew O'Connor
class myFunction:

    def main(self):
        csv_to_db("movies.csv")
        return

def csv_to_db(csv_file):
    conn = create_connection(csv_file)
    #create a cursor object to execute sql command
    c = conn.cursor()
    # create pandas df table
    movies_df = pd.read_csv(csv_file, header=0, index_col=False)
    c.execute(create_table_sql(movies_df))
    print("I did something... did i do it right tho...\n")
    #TO DO: populate db with data from df

def create_connection(db_file):
    # connect to database in sqlite3, if db not present, it will create one
    conn = None
    try:
        conn = sq.connect("movies")
    except Exception as e:
        print("That wasn't supposed to happen...\n")
        print(e)

    return conn
#Takes in a pandas df - not sure if sql syntax is correct
def create_table_sql(df):
    #can tweak to use column names to be more general for other csv files?
    col_list = df.columns.tolist()
    sql_string = """ CREATE TABLE IF NOT EXISTS movies(
    id int NOT NULL,
    name Text NOT NULL ,
    year Text NOT NULL
    ); """
    return sql_string



self = myFunction
self.main("movies.csv")


