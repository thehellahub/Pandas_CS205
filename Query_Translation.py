# Query Translation - take validated input query from user and translate it into sql syntax 


#Author: Matthew Piatt

import sqlite3 as sq
import pandas as pd
import shlex
from csvtodb import CSV2DB 

class Query_Translation:

	def main(self):

		CSV2DB.csvtodb(self)
	
		try:
			#Default to movies Db, pull from other database as needed
			conn = sq.connect('imdb.db')
		except Error as e:
			print('failed to connect')
			print(e)



		#base string for query, going to find all items that match the user query 
		base_query_string = "SELECT " 
		#fake valid query, would need to be assigned after query validation
		validated_query = 'title,year,first_name,rank title "h" year "1952"'
		# recall: query syntax - see Query_Syntax.txt 
		#Breaking query into an array 
		query_elements = shlex.split(validated_query, posix=False) # should get ['title,data' 'title' '10 days...',year,1952]


		# Getting list of return fields 
		return_fields = str(query_elements[0])
		return_fields = return_fields.split(",") #may be useful, may delete or pass to return statement logic
		#print(return_fields)
		#Creating list of data fields from csv files: Generalize this??

		#CSV files: actors, movies, movie_genres, roles
		movies_data_fields = pd.read_csv("movies.csv", header=0, index_col=False, encoding="ISO-8859-1").columns.tolist()
		actors_data_fields = pd.read_csv("actors.csv", header=0, index_col=False, encoding="ISO-8859-1").columns.tolist()
		movie_genre_data_fields = pd.read_csv("movies_genres.csv", header=0, index_col=False, encoding="ISO-8859-1").columns.tolist()
		roles_data_fields = pd.read_csv("roles.csv", header=0, index_col=False, encoding="ISO-8859-1").columns.tolist()

		del query_elements[0] # first element of array are return fields, not needed for sql command


		query_data_fields = list(())    # Loading up a list of the fields we're going to query against.             ie: [title,year]
		query_value_fields = list(())   # loading up a list of the values for fields to query against
		    
		# Loading up the lists
		count = 1
		for element in query_elements:
			if count % 2 != 0:  # odd index is the query field
				query_data_fields.append(element)
			if count % 2 ==0: # even index is the value for a query field q
				query_value_fields.append(element)
			count += 1

		count = 0
		while count < len(query_value_fields):
			temp = str(query_value_fields[count])
			temp = temp[1:-1] 
			query_value_fields[count] = temp
			count += 1
		#print(query_data_fields)
		## IDEA: for each item create the sql statement then execute via pandas to make a Df. 
		#Append each dataframe to a list to make a list of DF's. Then concatenate the DF's.
		data_frames = list(())
		# #build sql query string from base wrt each database as necessary, then execute
		count2 = 0 # keep track of index
		tables_pulling_from = list(())#create list of foreign keys to match on
		tables = list(())

		for item in return_fields:
			base_query_string += str(item) + ", "
		base_query_string = base_query_string[:-2]


		base_query_string += " FROM movies "



		base_query_string += "INNER JOIN movies_genres ON movies.id = movies_genres.id INNER JOIN actors ON " + \
			 "roles.actor_id = actors.id INNER JOIN roles ON roles.movie_id = movies.id"

		if (len(query_data_fields) > 0 and len(query_value_fields) > 0 and len(query_data_fields) == len(query_value_fields)) :
			
			base_query_string += " WHERE "
			count = 0
			while count < len(query_value_fields):
				if str(query_data_fields[count]).upper() == "TITLE":
					base_query_string +=   str(query_data_fields[count]) + " LIKE '%" + str(query_value_fields[count]) +"%' AND "
				elif str(query_data_fields[count]).upper() == "YEAR":
					base_query_string +=   str(query_data_fields[count]) + " >= '" + str(query_value_fields[count]) + "' AND "
				else:
					base_query_string +=   str(query_data_fields[count]) + " LIKE '" + str(query_value_fields[count]) +"' AND "
				count += 1


			base_query_string = base_query_string[:-4]
			base_query_string += ";"
			#print(base_query_string) 

			# Execute the created sql string, add that df to the list
			df = pd.read_sql_query(base_query_string,conn)
			print(df.drop_duplicates())
			return
		else:
			print("Query Syntax Error")
			return


self = Query_Translation()
self.main()


 











