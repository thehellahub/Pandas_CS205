from csvtodb import CSV2DB
from Query_Interpreter import Query_Interpreter
from Query_Translation import Query_Translation
from ErrorHandler import error_handler

import time
import sys
import os
import glob

debug = 0

class IMDB_Query_Engine:


	@error_handler(debug,"IMDB_Query_Engine.run")
	def run(self):

		# Intro line
		intro_string = '''
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$**$$$$$$$$$**$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$"   ^$$$$$$F    *$$$$$$$$$$                        $$
$$$$$$$$$$$$$$$$$$$$$     z$$$$$$L    ^$$$$$$$$$$  Spring 2020 CS 205    $$
$$$$$$$$$$$$$$$$$$$$$    e$$$$$$$$$e  J$$$$$$$$$$  Software Engineering  $$
$$$$$$$$$$$$$$$$$$$'eee$$$$$$$$$$$$$e$$*'$$$$$$$$  Prof Hibbeler         $$
$$$$$$$$$$$$$$$$$$'@$$$$$$$$$$$$$$$$$$$*  $$$$$$$                        $$
$$$$$$$$$$$$$$$$$'$$$$$$$$$$$$$$$$$$$$$*  $$$$$$$  Nick Hella            $$
$$$$$$$$$$$$$$$$$$'*$$$$  $$$$$$$  $$$$$  $$$$$$$  Matthew Piatt         $$
$$$$$$$$$$$$$$$$$$'$*$$$  $$$$$$$  $$$$   ^$**$$$  Rachel Goldman        $$
$$$$$$$$$$$$$$$"     *$$ee$$$$$$$$$$$     $$$**$$  Andrew O'Connor       $$
$$$$$$$$$$$$$$$.      "***$$"*"$$$$        $$$$*$                        $$
$$$$$$$$$$$$$$$b          "$$$$$"          $$$$$*$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$c.         """            $$$$$$*^$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$e..                     $$$$$$$$^$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$eeee..            J$$$$$$$$ "$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$r          z$$$$$$$$$  $$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"         z$$$$$**$$$   $$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$*"          z$$$P"   ^*$   $$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$*"           .d$$$$       $;  $$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$"           .e$$$$$F       3'  $$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$.         .d$$$$$$$         $  $$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$eeeeeeed$*""""**""         $ '$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$                  $ $$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.                 $$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$e.              d$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$   TEAM:                                       88                      $$             		
$$                                               88                      $$      
$$                                               88                      $$             
$$   $$,dPPYba,  ,adPPYYba, 8b,dPPYba,   ,adPPYb,88 ,adPPYYba,           $$  
$$   $$P'    "8a ""     `Y8 88P'   `"8a a8"    `Y88 ""     `Y8           $$  
$$   $$       d8 ,adPPPPP88 88       88 8b       88 ,adPPPPP88           $$  
$$   $$b,   ,a8" 88,    ,88 88       88 "8a,   ,d88 88,    ,88           $$  
$$   $$`YbbdP"'  `"8bbdP"Y8 88       88  `"8bbdP"Y8 `"8bbdP"Y8           $$  
$$   $$                                                                  $$  
$$   $$                                                                  $$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$                                                  
'''		
		print(intro_string)
		print("\n Welcome to the IMDB data set query service brought to you by Team Pandas! \n")

		if debug:
			print("\n\n ** NOTICE: Developer debug mode ON ** \n\n")
			print("Hit enter to continue")
			input()

		extension = '.db'
		result = glob.glob('*.{}'.format(extension))
		if len(result) == 1:
			print("\nDatabase present")
		else:
			print("Would you like to create the database? Enter 'load data' to continue, 'exit' to exit:")
			user_command = input()
			if user_command.lower() == "load data":
				conn = self.load()
			elif user_command.lower() =="exit":
				self.exit()

		# # Load the IMDB database and create connection object to database
		# print("Loading CSVs into Sqlite DB...")
		# conn = CSV2DB.go(self, debug)
		# print("DB creation successful!")

		# Provide example of query structure, taken from Query_Syntax.txt
		query_structure = '''

Query example:

	title,year,genre title "Harry Potter" year "2008"
	                                  ^ Value we're going to look for
	                            ^ Column were going to query on
	                ^ Value we're going to look for
	       ^ Column were going to query on
	^ Desired data field we want to return       


	This would return:
	  Harry Potter and the Half-Blood Prince 

	type 'man' for user manual.
	
	To search all feilds use the keyword '*' at the start of your query
	
	Example: * Harry Potter


Fields you can Query against:

	Queries for movies:

		title - the title of the movie

		year - the year the movie was made

		rank - the rating of the movie out of 10

	Queries for actors:

		first_name - first name of the actor

		last_name - last name of the actor

		gender - the gender of the actor

	Queries for genres:

		genere - the genere/catagory the movie falls into

	Queries for roles:

		role - the role/charater the actor plays

You can Mix & Match any of the fields!!!

'''

		# Print the example query syntax
		print(query_structure)


		# While-True loop for continuous run with designated exit parameter
		while True:

			extension = '.db'
			result = glob.glob('*.{}'.format(extension))
			if len(result) == 0: #database not present
				print("\n 151: Database not detected, enter 'load' to create database:\n\n")



				flag = False
				#Validating correct function has been input

				while flag != True:
					query = input()
					if query.lower() == "load":
						self.load()
						flag = True
					else:
						print("Enter 'load' to continue:")
						pass



			# First, prompt the user to type their query:
			print("\n Please enter your query: \n")

			# Gathering the user's input and defining variable query
			query = input()

			if len(str(query).strip()) != 0:

				# Exit parameter
				if str(query).strip() == 'exit':
					self.exit(conn)
				elif str(query).strip() == 'help':
					self.help()
				elif str(query).strip() == 'man':
					self.help()
				elif str(query).strip()== 'load':
					self.load()
				elif str(query).strip()== 'del':
					self.delete()
				
				else:
					if str(query).strip() == 'show all':
						query = '*'

					query = Query_Interpreter.data_star_check(self,query,conn,debug)

					if debug:
						print("\n\n User query being passed to data comma check is: " + str(query))

					query = Query_Interpreter.data_comma_check(self,query,conn,debug)

					if debug:
						print("\n\n User query being passed to validation checks are: " + str(query))

					if Query_Interpreter.data_field_check(self,query,conn,debug): 	# checking for proper data fields in the query
						# Check to make sure that the query passes data value validation testing 
						# @Exception_Handler
						# Query_Interpreter.data_value_check(query)

						# Run the query through SQLite3 Translation Function
						df = Query_Translation.Query_Translation(self, conn, query, debug)

						if len(df) != 0:
							# Print the result set
							print("\n\n Results: \n\n")
							print(df.to_string(index=False))
							print("\n Length: " + str(len(df)))
						if len(df) == 0:
							print("\n\n No results found! \n\n")

					else:
						print("\n\n Data field validation check failed.")

			else:
				pass
	#Load the database, every time this function is called will load a new database. 
	@error_handler(debug,"IMDB_Query_Engine.load")
	def load(self):
		extension = '.db'
		result = glob.glob('*.{}'.format(extension))
		if len(result) == 1: #There is a database, remove and recreate. 
			for element in result:
				os.remove(element)
		print("Loading CSVs into Sqlite DB...")
		conn = CSV2DB.go(self, debug)
		print("DB creation successful!")
		print(result)
		
		return conn

	# Delete the db
	@error_handler(debug,"IMDB_Query_Engine.delete")
	def delete(self):
		# deleting db file if exists
		extension = '.db'
		result = glob.glob('*.{}'.format(extension))
		for _file in result:
			os.remove(_file)

		# deleting any .csv2 files if exists
		extension = 'csv2'
		result = glob.glob('*.{}'.format(extension))
		for csvfile in result:
			os.remove(csvfile)
		return




	#@error_handler(debug,"IMDB_Query_Engine.exit")
	def exit(self,conn):
		conn.close()
		try:
			os.remove("imdb.db")
		except Exception as e:
			pass
		sys.exit(0)

	@error_handler(debug,"IMDB_Query_Engine.help")
	def help(self): 
		help_str = '''
[Instructions]
Query example:

	title,year,genre title "Harry Potter" year "2008"
	                                  				^ Value we're going to look for
	                            			^ Column were going to query on
	                  			^ Value we're going to look for
	       				^ Column were going to query on
	^ Desired data field(s) we want to return       

	This would return:
	  Harry Potter and the Half-Blood Prince 

Fields you can Query against:

	Queries for movies:

		title - the title of the movie

		year - the year the movie was made

		rank - the rating of the movie out of 10

	Queries for actors:

		first_name - first name of the actor

		last_name - last name of the actor

		gender - the gender of the actor

	Queries for genres:
		genere - the genere/catagory of the movie 

	Queries for roles:

		role - the role/charater the actor plays

You can Mix & Match any of the fields!!!
 
'''
		# Print the help messange
		print(help_str)

		return


for element in list(sys.argv):
	if str(element).strip() == "-debug":
		debug = 1

self = IMDB_Query_Engine()
self.run()