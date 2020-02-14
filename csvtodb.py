import sqlite3
import pandas as pd
import csv
import glob
import os
import sys
import ast

# Debug variable for running function stand-alone
standalone = 0
# Debug variable for debug print statements
debug = 0

class CSV2DB:
    '''

    Challenges: single quotes in data, and data encoding.


    '''

    def csvtodb(self, debug=debug):

        if debug:
            print("\n\n ** NOTICE: csvtodb debug mode ON ** \n\n")
        
        # get list of csv files in directory
        extension = 'csv'
        result = glob.glob('*.{}'.format(extension))
        #print(result)

        # remove any previously existing db file

        try:
            os.remove("imdb.db")
        except:
            pass


        # create the db file
        conn = sqlite3.connect("imdb.db")
        cur = conn.cursor()


    # Creating the tables (no inserts yet)

        # iterate through csv list
        for csvfile in result:

            table_name = csvfile[:-4]

            sql_string = "CREATE TABLE IF NOT EXISTS " + str(table_name).strip() + "("


            try:
                df = pd.read_csv(csvfile, header=0, index_col=False, encoding="ISO-8859-1")
            except Exception as e:
                print("error:")
                print(tmp_string)
                print(e)
                sys.exit()
            csv_columns = df.columns.tolist()

            if debug:
                print("\n\n DEBUG: CSV Columns are:")
                print(str(csv_columns) + "\n\n")


            for column in csv_columns:

                sql_string += str(column).strip() + " Text,"

            # getting rid of the last character in the string (the comma)
            sql_string = sql_string[:-1]

            # adding the rest of the string
            sql_string += ");"
            
            #print(sql_string)

            cur.execute(sql_string)

    # Insert into tables
        
        # iterating through the tables
        for csvfile in result:

            # Defining the table name as the CSV file without the .csv extension
            table_name = csvfile[:-4]

            # get the column names of the headers
            df = pd.read_csv(str(csvfile), header=0, index_col=False, encoding="ISO-8859-1")
            csv_columns = df.columns.tolist()

            # print("\n CSV File::")
            # print(csvfile)

            # print("Column headers in CSV file: ")
            # print(csv_columns)


            # let's initialize an empty dictionary
            tmp_dict = dict(())
            for column in csv_columns:
                tmp_dict[column] = None


            #iterate through the csv file row-by-row to insert data
            for index, rows in df.iterrows(): 

                    # creating row value
                    row = rows.tolist()

                    # populating the dictionary
                    counter2 = 0
                    for column in csv_columns:
                        tmp_dict[column] = row[counter2]
                        counter2 += 1

                    # create base insert string
                    base_sql_insert_string = "INSERT INTO " + str(table_name) + "("

                    for column in csv_columns:
                        base_sql_insert_string += "'" + str(column) + "',"

                    # get rid of the last comma

                    base_sql_insert_string = base_sql_insert_string[:-1]

                    base_sql_insert_string += ") VALUES ("

                    for key, value in tmp_dict.items():

                        value = str(value).replace("'", "''")

                        base_sql_insert_string += "'" + str(value) + "',"

                    # remove the last comma

                    base_sql_insert_string = base_sql_insert_string[:-1]

                    base_sql_insert_string += ");"

                    sql_insert_string = base_sql_insert_string

                    try:
                        cur.execute(sql_insert_string)
                    except Exception as e:
                        print(sql_insert_string)
                        print(e)
                        return


        if standalone:


            # Let's see the tables that are available in our database..
            sql = "SELECT name as 'Tables' FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

            # Now let's fetch our result set and load it into a pandas dataframe
            df = pd.read_sql_query(sql, conn)

            # Printing the results... (the tables)
            print("\n\n DEBUG: Names of tables in the db: ")
            print(str(df) + "\n\n")

            tables = df['Tables'].tolist()


            for table in tables:

                sql = "SELECT * FROM " + str(table) + ";"

                # Now let's fetch our result set and load it into a pandas dataframe
                df = pd.read_sql_query(sql, conn)

                print("\n\n DEBUG: Length of table: " + str(table) + " is:")
                print(str(len(df)) + "\n\n")

            # Testing a sample query:
            sql = "SELECT title, year, rank, genre FROM movies INNER JOIN movies_genres ON movies.id = movies_genres.id WHERE title LIKE '%Dalmatians%' GROUP BY title ORDER BY title;"

            # Now let's fetch our result set and load it into a pandas dataframe
            df = pd.read_sql_query(sql, conn)

            print("\n\n DEBUG: Testing sample Query: " + str(sql))
            print("\n\n DEBUG: Returning result set of sample query: ")
            print(df)

        conn.commit()
        conn.close()

if standalone:
    self = CSV2DB()
    self.csvtodb()

#EOF