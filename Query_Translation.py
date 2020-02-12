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
		base_query_string = "SELECT * from" 
		#fake valid query, would need to be assigned after query validation
		validated_query = 'title,year title "10 days in a nudist camp" year "1952"'
		# recall: query syntax - see Query_Syntax.txt 
		#Breaking query into an array 
		query_elements = shlex.split(validated_query, posix=False) # should get ['title,data' 'title' '10 days...',year,1952]


		# Getting list of return fields 
		return_fields = query_elements[0]
		return_fields = shlex.split(return_fields, posix=False) #may be useful, may delete or pass to return statement logic

		#Creating list of data fields from csv files: Generalize this??

		#CSV files: actors, movies, movie_genres, roles
		movies_data_fields = pd.from_csv("movies.csv").columns.tolist()
		actors_data_fields = pd.from_csv("actors.csv").columns.tolist()
		movie_genre_data_fields = pd.from_csv("movie_genres.csv").columns.tolist()
		roles_data_fields = pd.from_csv("roles.csv").columns.tolist()

		del query_elements[0] # first element of array are return fields, not needed for sql command


		query_data_fields = list(())    # Loading up a list of the fields we're going to query against.             ie: [title,year]
		query_value_fields = list(())   # loading up a list of the values for fields to query against
		    
		# Loading up the lists
		count = 1
		for element in query_elements:
			if count % 2 != 0:  # odd index is the query field
				query_data_fields.append(element)
			if count % 2 ==0: # even index is the value for a query field
				query_value_fields.append(element)
			count += 1

		count = 0
		while count < len(query_value_fields):
			temp = str(query_value_fields[count])
			temp = temp[1:-1] 
			query_value_fields[count] = temp
			count += 1

		## IDEA: for each item create the sql statement then execute via pandas to make a Df. 
		#Append each dataframe to a list to make a list of DF's. Then concatenate the DF's.
		data_frames = list(())
		# #build sql query string from base wrt each database as necessary, then execute
		count2 = 0 # keep track of index
		for item in query_data_fields:
			#base string for query, going to find all items that match the user query (the one piece of it) 
			base_query_string = "SELECT * from"

			# Determine which database the field is, then create sql command 
			if item in actors_data_fields:
				base_query_string += "actors WHERE " + str(item) + " LIKE '" + str(query_value_fields[count2]) + "';"

			elif item in movie_genre_data_fields:
				base_query_string += "movie_genres WHERE " + str(item) + " LIKE '" + str(query_value_fields[count2]) + "';"

			elif item in roles_data_fields:
				base_query_string += "roles_data_fields WHERE " + str(item) + " LIKE '" + str(query_value_fields[count2])+ "';"

			#item is in movie data fields
			else:
				if item.upper() == "TITLE":
					base_query_string += str(item) + " LIKE '%" + str(query_value_fields[count2]) +"%';"
				elif item.upper() == "YEAR":
					base_query_string += str(item) + " >= '" + str(query_value_fields[count2]) + "';"
				else:
					base_query_string += str(item) + " LIKE '" + str(query_value_fields[count2]) +"';"

			#Execute the created sql string, add that df to the list
			df = pd.read_sql_query(base_query_string,conn)
			data_frames.append(df)

			count2 += 1

		#Now concatenate the list of df to one df
		dfs = [df.set_index(['id','movie_id','actor_id']) for df in data_frames] 
		pd.concat(dfs, axis=1, join='inner')
		#			^				^						^
		#	the df to be concatenated
		#				concatenate by columns, not rows
		#								would prevent duplicates, but taxing and not neccesary.



self = Query_Translation()
self.main()


 











