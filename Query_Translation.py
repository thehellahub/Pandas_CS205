# Query Translation - take validated input query from user and translate it into sql syntax 

#Author: Matthew Piatt & Nick Hella

import sqlite3 as sq
import pandas as pd
import shlex
from csvtodb import CSV2DB 

# Debug variable for running function stand-alone
standalone = 0
# Debug variable for debug print statements
debug = 0

class Query_Translation:

	def Query_Translation(self, conn=None, user_query=None, debug=debug):

		if standalone:
			print("\n\n ** NOTICE: Query_Translation debug mode ON ** \n\n")
			CSV2DB.go(self)
	
		try:
			#Default to movies Db, pull from other database as needed
			conn = sqlite3.connect("imdb.db")
		except Exception as e:
			print('Failed to connect to the DB')
			print(e)


		#base string for query, going to find all items that match the user query 
		base_query_string = "SELECT " 
		#fake valid query, would need to be assigned after query validation

		if debug:

			if user_query == None:
				user_query = 'title,year,first_name,last_name,rank title "h" year "1952"'
			
			print("\n\n DEBUG: User query is: " + str(user_query) + "\n\n")
		
		# recall: query syntax - see Query_Syntax.txt 
		#Breaking query into an array 
		query_elements = shlex.split(user_query, posix=False) # should get ['title,data' 'title' '10 days...',year,1952]


		# Getting list of return fields 
		return_fields = str(query_elements[0])
		if return_fields == "*":
			return_fields = ["id","title","year","rank"]
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

		for item in return_fields:
			base_query_string += str(item) + ", "
		base_query_string = base_query_string[:-2]

		base_query_string += " FROM movies " + \
				"INNER JOIN movies_genres ON movies.id = movies_genres.id INNER JOIN actors ON " + \
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
			sql_query = base_query_string

			if debug:
				print("\n DEBUG: SQl query created in Query_Translation.py: \n")
				print(sql_query)

			# Execute the created sql string, add that df to the list
			df = pd.read_sql_query(sql_query,conn)
			df = df.drop_duplicates()

			if 'title' in return_fields:
				df = df.drop_duplicates(keep="first", subset='title')

			if debug:
				print("\n DEBUG: Dataframe returning from Query_Translation.py: \n")
				print(df.to_string(index=False) + "\n\n")
				#print("\n\n")
			return df
		else:
			print("Query Syntax Error")
			return

if standalone:
	self = Query_Translation()
	self.Query_Translation()

#EOF