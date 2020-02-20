import sqlite3
import pandas as pd
import csv
import glob
import os
import sys
import ast
import time
from multiprocessing import Process
from threading import Thread
from Data_Sanitation import Data_Sanitation
from ErrorHandler import error_handler

# Debug variable for running function stand-alone
standalone = 0
# Debug variable for debug print statements
debug = 0

class CSV2DB:
    '''

    Challenges: single quotes in data, and data encoding.


    '''

    @error_handler(debug,"csvtodb")
    def csvtodb(self, csvfile, conn, cur, debug=debug):

        if debug:
            print("\n\n ** NOTICE: csvtodb debug mode ON ** \n\n")


    # Creating the tables (no inserts yet)

        # iterate through csv list

        table_name = csvfile[:-5]

        sql_string = "CREATE TABLE IF NOT EXISTS " + str(table_name).strip() + "("


        try:
            if debug:
                print("\n\n DEBUG: Reading " + str(csvfile) + " into pandas dataframe")
            df = pd.read_csv(csvfile, header=0, index_col=False, encoding="ISO-8859-1")
            if debug:
                print("\n\n DEBUG: Finished reading " + str(csvfile) + " into pandas dataframe")
        except Exception as e:
            print("error:")
            print(tmp_string)
            print(e)
            sys.exit()

        csv_columns = df.columns.tolist()

        if debug:
            print("\n\n DEBUG: CSV Columns for file : " + str(table_name).strip() + "are:")
            print(str(csv_columns) + "\n\n")


        for column in csv_columns:

            sql_string += str(column).strip() + " Text,"

        # getting rid of the last character in the string (the comma)
        sql_string = sql_string[:-1]

        # adding the rest of the string
        sql_string += ");"
        
        if debug:
            print("\n\n DEBUG: CREATE TABLE SQL string: ")
            print(sql_string)

        cur.execute(sql_string)
        conn.commit()

    # Insert into tables

        # Defining the table name as the CSV file without the .csv2 extension
        table_name = csvfile[:-5]

        # get the column names of the headers
        #df = pd.read_csv(str(csvfile), header=0, index_col=False, encoding="ISO-8859-1")
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
                    print("\n\nError performing INSERT SQL string: ")
                    print(sql_insert_string)
                    print(e)
                    return


        conn.commit()
        #conn.close()

        return

    @error_handler(debug,"show_me_my_csvs")
    def show_me_my_csvs(self, debug=debug):
        
        if debug:
            print("\n\n ** NOTICE: show_me_my_csvs debug mode ON ** \n\n")
        
        # get list of csv files in directory
        extension = 'csv2'
        result = glob.glob('*.{}'.format(extension))

        if debug:
            print("\n\nDEBUG: CSV files in directorty 1.) are: ")
            print(result)

        return result

    @error_handler(debug,"show_me_my_csvs")
    def delete_csv2_files(self,debug=debug):
        # get list of csv files in directory
        extension = 'csv2'
        result = glob.glob('*.{}'.format(extension))

        for csvfile in result:
            os.remove(csvfile)
        return

    @error_handler(debug,"create_database")
    def create_database(debug=debug):

        # remove any previously existing db file

        try:
            os.remove("imdb.db")
        except:
            pass

        # create the db file
        conn = sqlite3.connect("imdb.db", check_same_thread=False)
        cur = conn.cursor()
        return conn,cur


    #THIS IS ONLY USED IF STANDALONE FLAG IS ON
    @error_handler(debug,"delete_database")
    def delete_database(self,debug=debug):
        # remove the imdb.db file created
        extension = 'db'
        result = glob.glob('*.{}'.format(extension))

        for _file in result:
            os.remove(_file)
        return

    @error_handler(debug,"go")
    def go(self, debug=debug):

        Data_Sanitation.sanitize(self,debug)

        result = CSV2DB.show_me_my_csvs(self,debug)

        if debug:
            print("\n\nDEBUG: CSV files in directorty 2.) are: ")
            print(result)

        conn,cur = CSV2DB.create_database(self)


        # NOTE: Turns out, SQLITE doesn't suppurt multithreaded writes. 
        # See: https://softwareengineering.stackexchange.com/questions/340550/why-are-concurrent-writes-not-allowed-on-an-sqlite-database
        
        # Creating the CSVs via multithreading
        #jobs = []

        for csvfile in result:

            if debug:
                print("Adding the following CSV to the DB: ")
                print(csvfile)

            # Used for multiprocessing/threading
            #process = Process(target=CSV2DB.csvtodb, args=(self,csvfile,)) # this is for multiprocessing
            # thread = Thread(target=CSV2DB.csvtodb, args=(self,csvfile,conn,cur))
            # thread.start()
            # jobs.append(thread)
        
            # # Waiting for all the process threads to finish
            # for proc in jobs:
            #     proc.join()

            CSV2DB.csvtodb(self,csvfile,conn,cur)

        CSV2DB.delete_csv2_files(self,debug) # erasing the .csv2 files now that we've put their content in the db

        # END OF FUNCTION
        # DEBUG FOR STANDALONE RUNNING

        if standalone:

            time.sleep(3)

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
            sql = "SELECT title, year, rank, genre FROM movies INNER JOIN movies_genres ON movies.id = movies_genres.id WHERE title LIKE '%D%' GROUP BY title ORDER BY title;"

            # Now let's fetch our result set and load it into a pandas dataframe
            df = pd.read_sql_query(sql, conn)

            print("\n\n DEBUG: Testing sample Query: " + str(sql))
            print("\n\n DEBUG: Returning result set of sample query: ")
            print(df)

            # remove the imdb.db file created
            CSV2DB.delete_database(self,debug)

        return conn


if standalone:
    self = CSV2DB()
    self.go()

#EOF