from csvtodb import CSV2DB
from Query_Interpreter import Query_Interpreter
from Query_Translation import Query_Translation
from ErrorHandler import error_handler

import time
import sys
import os
import glob
import sqlite3

debug = 0

class IMDB_Query_Engine:

	conn = None


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

		extension = 'db'
		result = glob.glob('*.{}'.format(extension))
		
		if len(result) == 1:
			print("\nDatabase present")
		else:
			flag = False
			print("Would you like to create the database? Enter 'load' to continue, 'exit' to exit:")
			while flag != True:
				user_command = input()
				if user_command.lower() == "load":
					self.conn = self.load()
					flag = True
				elif user_command.lower() =="exit":
					self.exit(self.conn)
				else:
					print("\nEnter 'load' to continue or 'exit' to exit\n")

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

Type man or help for additonal information

'''

		# Print the example query syntax
		print(query_structure)


		# While-True loop for continuous run with designated exit parameter
		while True:

			extension = 'db'
			result = glob.glob('*.{}'.format(extension))
			if len(result) == 0: #database not present
				print("\nDatabase not detected, enter 'load' to create database:\n\n")
				print("\ninput 'exit' at any time to exit the program")

				flag = False
				#Validating correct function has been input

				while flag != True:
					query = input()
					if query.lower() == "load":
						self.conn.close()
						self.conn = self.load()
						flag = True
					elif query.lower() == "exit":
						self.exit(self.conn)
					else:
						print("Enter 'load' to continue:")
						pass
			else:
				self.conn = sqlite3.connect("imdb.db", check_same_thread=False)


			# First, prompt the user to type their query:
			print("\n Please enter your query: \n")

			# Gathering the user's input and defining variable query
			query = input()

			if len(str(query).strip()) != 0:

				# Exit parameter
				if str(query).strip() == 'exit':
					self.exit()
				elif str(query).strip() == 'help':
					self.help()
				elif str(query).strip() == 'man':
					self.man()
				elif str(query).strip()== 'load':
					self.conn = self.load()
				elif str(query).strip()== 'del':
					self.delete(self.conn)
				elif str(query).strip() == 'show panda':
					self.show_panda()
				else:
					if str(query).strip() == 'show all':
						query = '*'

					if Query_Interpreter.data_value_check(self,query,self.conn,debug):

						query = Query_Interpreter.data_star_check(self,query,self.conn,debug)

						if debug:
							print("\n\n User query being passed to data comma check is: " + str(query))

						query = Query_Interpreter.data_comma_check(self,query,self.conn,debug)

						if debug:
							print("\n\n User query being passed to validation checks are: " + str(query))

						if Query_Interpreter.data_field_check(self,query,self.conn,debug): 	# checking for proper data fields in the query
							# Check to make sure that the query passes data value validation testing 

							# Run the query through SQLite3 Translation Function
							df = Query_Translation.Query_Translation(self, self.conn, query, debug)

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
						print("\n\n Data value validation check failed.")
			else:
				pass
	#Load the database, every time this function is called will load a new database. 
	@error_handler(debug,"IMDB_Query_Engine.load")
	def load(self):

		try:
			self.conn.close()
		except:
			pass
		extension = 'db'
		result = glob.glob('*.{}'.format(extension))
		if len(result) == 1: #There is a database, remove and recreate. 
			for element in result:
				os.remove(element)
		print("Loading CSVs into Sqlite DB...")
		self.conn = CSV2DB.go(self, debug)
		print("DB creation successful!")
		
		return self.conn

	# Delete the db
	@error_handler(debug,"IMDB_Query_Engine.delete")
	def delete(self,conn):
		# deleting db file if exists
		extension = 'db'
		result = glob.glob('*.{}'.format(extension))
		conn.close()
		for _file in result:
			os.remove(_file)

		# deleting any .csv2 files if exists
		extension = 'csv2'
		result = glob.glob('*.{}'.format(extension))
		for csvfile in result:
			os.remove(csvfile)


		return




	#@error_handler(debug,"IMDB_Query_Engine.exit")
	def exit(self,conn=None):
		if self.conn != None:
			self.conn.close()
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

Additonally:

	The query 'show all' will display the full database you 
	are querying against. Alternatively the symbol '*' will 
	also acomplish this. 

	With a specific query, '*' will return all of the possible
	query fields. 

	Example: * title "h"

Technical note:
	Any years given in the query statement are treated as 
	greater than or equal to in the result set


 
'''
		# Print the help messange
		print(help_str)

		return


	@error_handler(debug,"IMDB_Query_Engine.man")
	def man(self): 
		man_str = '''
		[USER MANUAL]

		This database search engine has 7 main functions:

		1) load
			Loads a fresh randomized database pulled from a much larger dataset 

		2) del
			Deletes the randomized database, after performing this function
			the only two functions remaining to the user are load and exit

		3) help
			Demonstrates query syntax and possible fields to query against
			use this function to help formulate possible queries of this database

		4) exit
			exits the program

		5) man
			calls this description of functions

		6) show panda
			if you would like to see the panda ascii art, enter this command =)

		7) query
			This is the default behavior of this program. Enter your query instead of one
			of the previous five functions to perform a query

		For more information about query syntax or structure or query fields please type 'help' to call
		the help function

		'''
		print(man_str)
		return
	def show_panda(self):
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
		return


for element in list(sys.argv):
	if str(element).strip() == "-debug":
		debug = 1

self = IMDB_Query_Engine()
self.run()