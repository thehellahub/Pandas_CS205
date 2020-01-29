import shlex
import sys
import sqlite3
import csv


class Example_Program:

	def main(self):

		# Creating a connection object to our Sqlite IMDB database
		conn = sqlite3.connect("imdb.db") # Reading in our sqlite3 db

		# Intro line
		print("\n Welcome to the IMDB data set query service brought to you by the Pandas! \n")

		# Provide example of query structure, taken from Query_Syntax.txt
		query_structure = '''

Query example:

	title title "Harry Potter" year "2008"
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

			# Exit parameter
			if str(query).strip() == 'exit':
				sys.exit()
			if str(query).strip() == 'help':
				self.help()
			if str(query).strip() == 'man':
				self.help()
			else:

				# Breaking query into array, ie: ['title,date,genre', 'title', '"Harry Potter"', 'date', '2008']
				query = shlex.split(query, posix=False)

				desired_data = query[0]

				# Erasing the desired data from the query list
				del query[0]

				query_data_fields = list(())	# Loading up a list of the fields we're going to query against. 			ie: [title,year]
				query_data_values = list(())	# Loading up a list of the values we're going to query the fields against. 	ie: ["Harry Potter", "2008"]

				# Loading up the lists
				count = 1
				for element in query:

					if count % 2 == 0:
						query_data_values.append(element)
					else:
						query_data_fields.append(element)

					count += 1

				print(query_data_fields)
				print(query_data_values)



		return

	def help(self):

		print("Help!")

		return

	def man(self):

		manual_string = 
'''

Enter "help" for help

Enter "man" for the program manual

Query Example (Sytax Explanation):

	title title "Harry Potter" year "2008"
	                                  ^ Value we're going to look for
	                            ^ Column were going to query on
	                ^ Value we're going to look for
	       ^ Column were going to query on
	^ Desired data field we want to return       


	This would return:
	  Harry Potter and the Half-Blood Prince 

'''	
	print(manual_string)

	return

self = Example_Program()
self.main()

# EOF