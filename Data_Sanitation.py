import pandas as pd
import csv
import random

# Debug variable for running function stand-alone
standalone = 0
# Debug variable for debug print statements
debug = 0

class Data_Sanitation:

	def create_movies_table(self,debug=debug):

		movies_df = pd.read_csv("movies.csv", header=0, index_col=False, encoding="ISO-8859-1")

		alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		df_holder = [] # df that holds dataframe of movies that begin with a specified letter (not case sensitive) from movies.csv
		for letter in alphabet_list:
			tmp_df = movies_df[ movies_df['title'].str.startswith(str(letter)) | movies_df['title'].str.startswith(str(letter).upper()) ]
			df_holder.append(tmp_df)

		movies_columns = movies_df.columns.tolist()

		# Choosing 100 random rows from each dataframe in df_holder to create movies2 (df of 100 random movies that begin with each letter of the alphabet)
		sanitized_movies_data = []
		for df in df_holder:
			random_numbers_used = []
			count = 0
			while count < 200:

				random_row = random.randint(0,len(df)-1)

				if random_row not in random_numbers_used:
					random_numbers_used.append(random_row)
					row = df.iloc[random_row].tolist()
					sanitized_movies_data.append(row)
					count += 1
				else:
					pass

		# sanitized_movies_data = zip(sanitized_movies_data)
		movies2 = pd.DataFrame(sanitized_movies_data, columns=movies_columns)
		movies2.to_csv('movies.csv2', index=False)
		return movies2	

	def create_movies_genres_table(self, movies2,debug=debug):
		movies_genres = pd.read_csv("movies_genres.csv", header=0, index_col=False, encoding="ISO-8859-1")
		movies_genres2 = movies_genres[ ( movies_genres['id'].isin(movies2['id']) ) ]
		movies_genres2.to_csv('movies_genres.csv2', index=False)
		return movies_genres2

	def create_actors_table(self, movies2,debug=debug):
		actors = pd.read_csv("actors.csv", header=0, index_col=False, encoding="ISO-8859-1")
		actors2 = actors[ ( actors['id'].isin(movies2['id']) ) ]
		actors2.to_csv('actors.csv2', index=False)
		return actors2
			
	def create_roles_table(self, movies2, actors2,debug=debug):

		roles = pd.read_csv("roles.csv", header=0, index_col=False, encoding="ISO-8859-1")
		roles2 = roles[ ( roles['actor_id'].isin(actors2['id']) ) ]
		roles2.to_csv('roles.csv2', index=False)	
		return roles2

	def sanitize(self,debug=debug):
		movies2 = Data_Sanitation.create_movies_table(self)
		movies_genres2 = Data_Sanitation.create_movies_genres_table(self,movies2)
		actors2 = Data_Sanitation.create_actors_table(self,movies2)
		roles2 = Data_Sanitation.create_roles_table(self,movies2, actors2)
		return


if standalone:
	self = Data_Sanitation()
	self.sanitize()