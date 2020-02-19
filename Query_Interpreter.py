import shlex
import sys
import sqlite3
import csv
import os
import pandas as pd

# Debug variable for running function stand-alone
standalone = 0
# Debug variable for debug print statements
debug = 0

class Query_Interpreter:

    def data_field_check(self, user_query, conn=None,debug=debug):

        if debug:
            print("\n\n ** NOTICE: Query Query_Interpreter debug mode ON ** \n\n")
        
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
        if standalone:
            conn = sqlite3.connect("imdb.db") # Reading in our sqlite3 db

    # Let's get all the data fields in our database
        # First get tables in database...
        sql = "SELECT name as 'Tables' FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

        # Take our tables and load it into a pandas dataframe
        df = pd.read_sql_query(sql, conn)
        tables = df['Tables'].tolist()

        all_our_data_fields = list(())

        # for each table in our list of tables, we're going to get the columns and then add them to a list
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


        if debug:
            print("\n\n DEBUG: Desired data fields are: " + str(desired_data) + "\n\n")

        for element in desired_data:

            # If an element in the desired_data array is NOT in the all_out_data_fields array, return false!
            if element not in all_our_data_fields: 
                print("\n\n Validation failed for data field: " + element)
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

        if debug:
            print("\n\n DEBUG: Data fields being queried against are: " + str(query_data_fields) + "\n\n")


        for element in query_data_fields:
            # If an element in the desired_data array is NOT in the all_out_data_fields array, return false!
            if element not in all_our_data_fields: 
                print("\n\n Validation failed for data field in: " + element)
                return False

        return True

    def data_value_check(self, user_query, conn=None,debug=debug):

        if debug:
            print("\n\n ** NOTICE: Query Query_Interpreter debug mode ON ** \n\n")
        
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
        if standalone:
            conn = sqlite3.connect("imdb.db") # Reading in our sqlite3 db

    # Let's get all the data fields in our database
        # First get tables in database...
        sql = "SELECT name as 'Tables' FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

        # Take our tables and load it into a pandas dataframe
        df = pd.read_sql_query(sql, conn)
        tables = df['Tables'].tolist()

        all_our_data_fields = list(())

        # for each table in our list of tables, we're going to get the columns and then add them to a list
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

        # Erasing the desired data from the query list
        del query[0]

        query_data_values = list(())    # Loading up a list of the fields we're going to query against.             ie: [title,year]


        # recall, query is: [title,first_name,last_name,gender,rank,year] title "Harry Potter" year "2008"
        # then we used "del query[0]" to get rid of what's in the brackets
        # Now our query string looks something like: title "Harry Potter" year "2008"
        
        # Loading up the lists
        count = 1
        for element in query:
            if count % 2 == 0:  # if count is an odd number as we iterate through the query
                query_data_values.append(element)
            count += 1

        if debug:
            print("\n\n DEBUG: Data fields being queried against are: " + str(query_data_values) + "\n\n")


        for element in query_data_values:

            if element[0] != "\"": # gets first char in string https://guide.freecodecamp.org/python/is-there-a-way-to-substring-a-string-in-python/
                print("\n\n QUERY ERROR: No beginning quotes around " + element)
                return False
            if element[-1] != "\"": # gets last char in string https://www.pythoncentral.io/how-to-get-a-substring-from-a-string-in-python-slicing-strings/
                print("\n\n QUERY ERROR: No ending quotes around " + element)
                return False

        return True

    def data_comma_check(self, user_query, conn=None, debug=debug):

        if debug:
            print("\n\n ** NOTICE: Query Query_Interpreter debug mode ON ** \n\n")

        # Breaking query into array, ie: ['title,first_name,last_name,gender,rank,year', 'title', '"Harry Potter"', 'date', '2008']
        query = shlex.split(user_query, posix=False)

        desired_data = str(query[0]).strip()  # ['title,first_name,last_name,gender,rank,year']

        if debug:
            print("\n\nDEBUG: desired data in data comma check before any correction: " + str(desired_data))

        del query[0]

        if desired_data[len(desired_data)-1] == ",":
            print("\n\nDEBUG: Comma detected at the end of desired data!")
            desired_data = desired_data[:-1]

            if debug:
                print("\n\nDEBUG: corrected desired data string without comma should be: " + str(desired_data))
                print(len(desired_data))

        user_query = desired_data + " "

        for element in query:
            user_query += str(element) + " "

        user_query = user_query.strip()

        return user_query

    def data_star_check(self, user_query, conn=None, debug=debug):

        if debug:
            print("\n\n ** NOTICE: Query Query_Interpreter debug mode ON ** \n\n")

        # Instructions
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
        if standalone:
            conn = sqlite3.connect("imdb.db")  # Reading in our sqlite3 db

        # Let's get all the data fields in our database
        # First get tables in database...
        sql = "SELECT name as 'Tables' FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

        # Take our tables and load it into a pandas dataframe
        df = pd.read_sql_query(sql, conn)
        tables = df['Tables'].tolist()

        all_our_data_fields = list(())

        # for each table in our list of tables, we're going to get the columns and then add them to a list
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

        desired_data = query[0]  # ['title,first_name,last_name,gender,rank,year']

        desired_data = desired_data.split(",")  # ['title','first_name'.....] makes array of data wanted

        if (desired_data[0] == '*') and (len(desired_data) == 1):

            print("\n\n DEBUG: STAR NOTATION DETECTED!")
            desired_data = "title,year,rank,genre,role,first_name,last_name,gender"
            query[0] = desired_data
            tmp = user_query[2:]
            tmp = desired_data + " " + tmp
            print("\n\n DEBUG: User query being passed back from data_star_check function: " + str(tmp))
            return tmp
        else:
            return user_query




if standalone:

    user_query = "title,first_name,last_name,gender,rank,year title 'Yeet' year '2008'"
    self = Query_Interpreter() #instance of object
    #call its main | also can be: Query_Interpreter.main(self=Query_Interpreter())
    self.data_field_check(user_query=user_query)



