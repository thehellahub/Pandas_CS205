from csvtodb import CSV2DB
from Query_Interpreter import Query_Interpreter
from Query_Translation import Query_Translation

import time
import sys
import os


class IMDB_Query_Engine:


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


		# Load the IMDB database and create connection object to database
		print("Loading CSVs into Sqlite DB...")
		conn = CSV2DB.go(self, debug)
		print("DB creation successful!")

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

'''

		# Print the example query syntax
		print(query_structure)


		# While-True loop for continuous run with designated exit parameter
		while True:

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
				else:
					# Check to make sure that the query passes data field validation testing
					#@Exception_Handler
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
						if len(df) == 0:
							print("\n\n No results found! \n\n")

			else:
				pass

	def exit(self,conn):
		conn.close()
		try:
			os.remove("imdb.db")
		except Exception as e:
			pass
		sys.exit(0)


	def Exception_Handler():
		print("Exception Handler function called")



debug = 0
for element in list(sys.argv):
	if str(element).strip() == "-debug":
		debug = 1

self = IMDB_Query_Engine()
self.run()