import shlex
import sys
import sqlite3
import csv
import os
import pandas as pd

class Query_Interpreter:

    def data_field_check(self, user_query):
        
        #Instructions
        '''
        Query example:
            [title,first_name,last_name,gender,rank,year] title "Harry Potter" year "2008"
                                                                                      ^ Value we're going to look for
                                                                                ^ Column were going to query on
                                                                    ^ Value we're going to look for
                                                           ^ Column were going to query on
            ^ Desired data field we want to return
            This would return:
              Harry Potter and the Half-Blood Prince
            type 'man' for user manual.
        '''



        # Creating a connection object to our Sqlite IMDB database
        conn = sqlite3.connect("imdb.db") # Reading in our sqlite3 db

    # Let's get all the data fields in our database
        # First get tables in database...
        sql = "SELECT name as 'Tables' FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

        # Take our tables and load it into a pandas dataframe
        df = pd.read_sql_query(sql, conn)
        tables = df['Tables'].tolist()

        all_our_data_fields = list(())

        # pseudo code meow

        '''
        for each table in our list of tables, we're going to get the columns and then add them to a list

        '''

        for table in tables:

            # now we're referencing an individual table
            # let's get the columns!

            sql = "SELECT * FROM " + str(table) + ";"

            df = pd.read_sql_query(sql, conn)

            columns = df.columns.tolist()

            for column in columns:

                all_our_data_fields.append(column)



    # Now let's switch gears and get all the desired data fields


        # Breaking query into array, ie: ['title,first_name,last_name,gender,rank,year', 'title', '"Harry Potter"', 'date', '2008']
        query = shlex.split(user_query, posix=False)

        desired_data = query[0] # ['title,first_name,last_name,gender,rank,year']

        desired_data = desired_data.split(",")  # ['title','first_name'.....] makes array of data wanted

        for element in desired_data:

            # If an element in the desired_data array is NOT in the all_out_data_fields array, return false!
            if element not in all_our_data_fields: 
                print("Validation failed for data field: " + element)
                return False

    # Check against the data fields the user is querying against.. ie: ['title', 'year']
        # Erasing the desired data from the query list
        del query[0]

        query_data_fields = list(())    # Loading up a list of the fields we're going to query against.             ie: [title,year]


        # recall, query is: [title,first_name,last_name,gender,rank,year] title "Harry Potter" year "2008"
        # then we used "del query[0]" to get rid of what's in the brackets
        # Now our query string looks something like: title "Harry Potter" year "2008"
        
        # Loading up the lists
        count = 1
        for element in query:
            if count % 2 != 0:  # if count is an odd number as we iterate through the query
                query_data_fields.append(element)
            count += 1

        #print(query_data_fields)

        for element in query_data_fields:

            # If an element in the desired_data array is NOT in the all_out_data_fields array, return false!
            if element not in all_our_data_fields: 
                print("Validation failedfor data field: " + element)
                return False

        print("We passed the data field check!")
        return True


# user_query = "title,first_name,last_name,gender,rank,year title 'Yeet' year '2008'"


# self = Query_Interpreter() #instance of object
# self.data_field_check(user_query=user_query)                #call its main | also can be: Query_Interpreter.main(self=Query_Interpreter())


