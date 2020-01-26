import pandas as pd

'''
Author: Nick Hella

pandas is a powerful, open source, BSD-licensed library providing high-performance, 
easy-to-use data structures and data analysis tools for the Python programming language.

This file will demonstrate some of the simple queries one can use with our data sets.


More documentation on pandas is available on their website:

	https://pandas.pydata.org/pandas-docs/stable/


More simple pandas examples can also be found here:
	
	https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html

To run this file, (1.) open a terminal	(2.) move into the directory of this file 	(3.) run the command below

	python Pandas_Example.py

Note, you made need to specify python3 instead of python if you have python2.x by default

'''

class Pandas_Example:

	def main(self):

		# Reading in one of our .CSV data sets in as a pandas data frame 

		# Let's try playing around with the movies csv, that one's fun
		movies_df = pd.read_csv('movies.csv', header=0, index_col=False)

		# Let's take a look at how big our data set is
		print("\n The length of the data set: \n")
		print(len(movies_df))

		# Let's try printing the columns, or data headers of our data frame as a list
		print("\n The columns in our data set: \n")
		print(movies_df.columns.tolist())

		# This should return the following
		#	['id', 'name', 'year', 'rank']

		# Let's try printing movies that contain the string "Harry Potter"
		print("\n Harry Potter movies in the movie data set: \n")
		print( movies_df [ movies_df['name'].str.contains('Harry Potter') ] )

		# This should return the following:

		'''
		            id      name   														year  rank
			129731  139650	Harry Potter and the Chamber of Secrets  					2002   7.3
			129732  139651  Harry Potter and the Chamber of Secrets (2002/II)  			2002   NaN
			129733  139652  Harry Potter and the Goblet of Fire  						2005   NaN
			129734  139653  Harry Potter and the Half-Blood Prince  					2008   NaN
			129735  139654  Harry Potter and the Order of the Phoenix  					2007   NaN
			129736  139655  Harry Potter and the Prisoner of Azkaban  					2004   7.7
			129737  139656  Harry Potter and the Prisoner of Azkaban (2004...  			2004   NaN
			129738  139657  Harry Potter and the Sorcerer's Stone  						2001   7.3
			129739  139658  Harry Potter and the Sorcerer's Stone (2001/II)  			2001   NaN
			129740  139659  Harry Potter und die Kammer des Schreckens - D...  			2002   NaN
			129741  139660  Harry Potter: Behind the Magic  							2001   NaN
			129742  139661  Harry Potter: Quidditch World Cup  							2003   NaN
			129743  139662  Harry Potter: Witchcraft Repackaged  						2001   NaN
			152927  164234  J.K. Rowling: Harry Potter and Me  							2002   NaN
			187365  200348  Magical World of Harry Potter: The Unauthorize...  			2000   NaN

			  ^ This first column is just an index column. Not actual part of the data.

		'''

		# Ok, now let's try being a bit more specific...

		# Let's look in our data frame for movies with titles that contain the string "Harry Potter".. 
		# And now  let's also look for the "Harry Potter" movies in this resultset where the year >= 2005

		# Defining harry_potter_movies_df to be the results of our previous print statement
		harry_potter_movies_df = movies_df[ movies_df['name'].str.contains('Harry Potter') ]

		print("\n Harry Potter movis in the dataset that came out on or after 2005: \n")
		print( harry_potter_movies_df [ harry_potter_movies_df['year'] >= 2005 ] )


		# This should return the following:

		'''
		            id      name   														year  rank
			129733  139652  Harry Potter and the Goblet of Fire  						2005   NaN
			129734  139653  Harry Potter and the Half-Blood Prince  					2008   NaN
			129735  139654  Harry Potter and the Order of the Phoenix  					2007   NaN


		'''

		# Ugh, such good movies.. 

		return


self = Pandas_Example()
self.main()

# EOF