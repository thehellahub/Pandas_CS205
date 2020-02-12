from csvtodb import CSV2DB
from Query_Interpreter import Query_Interpreter

class IMDB_Query_Engine:


	def run(self):


		# Intro line
		print("\n Welcome to the IMDB data set query service brought to you by the Pandas! \n")

		# Load the IMDB database
		print("Loading CSVs into Sqlite DB...")
		CSV2DB.csvtodb(self)
		print("Done!")

		# Provide example of query structure, taken from Query_Syntax.txt
		query_structure = '''

Query example:

	title,date,genre title "Harry Potter" year "2008"
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
				self.exit()
			if str(query).strip() == 'help':
				self.help()
			if str(query).strip() == 'man':
				self.help()
			else:

				# Check to make sure that the query passes data field validation testing
				#@Exception_Handler
				Query_Interpreter.data_field_check(self,query)	# checking for proper data fields in the query

				# Check to make sure that the query passes data value validation testing 
				# @Exception_Handler
				# Query_Interpreter.data_value_check(query)

				# Run the query through SQLite3 Translation Function




				# Print the result set



		#


	def Exception_Handler():

		print("Exception Handler function called")


self = IMDB_Query_Engine()
self.run()