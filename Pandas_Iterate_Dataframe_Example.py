import pandas as pd
import ast

'''
How to iterate through a pandas dataframe

Author: Nick Hella

Here's a representation of our dataframe

	 col1  col2  col3  col4  col5
	    0     5    10    15    20
	    1     6    11    16    21
	    2     7    12    17    22
	    3     8    13    18    23
	    4     9    14    19    24


Objective: 

Iterate through the dataframe 
and print the following:


		0     5    10    15    20
		1     6    11    16    21
		2     7    12    17    22
		3     8    13    18    23
		4     9    14    19    24

'''

def create_dataframe():
	# Setting up the dataframe (unimportant.. no need to spend time understandig)
	the_dict = dict(())
	the_dict['col1'] = []
	the_dict['col2'] = []
	the_dict['col3'] = []
	the_dict['col4'] = []
	the_dict['col5'] = []

	count = 1
	count2 = 0
	while count<=5:
		count3 = count2+5
		while count2<count3:
			the_dict['col'+str(count)].append(count2)
			count2+=1
			if count2 == 25:
				break
		if count2 == 25:
			break
		count += 1

	df = pd.DataFrame.from_dict(the_dict)

	return df


def main():

	# Here's the dataframe ---- START READING CODE HERE:
	df = create_dataframe() 

	print("\nDataframe is:")
	print(df.to_string(index=False))
	print("\n")

	# Let's get the columns
	columns = df.columns.tolist()

	# Let's get the number of rows
	number_rows = len(df)

	# Iterating the df row-by-row and printing
	print("\nOutput:")
	index = 0
	while index < len(columns):

		count = 0
		tmp_str = ""
		while count < len(columns):

			df_cell = str(df[columns[count]].iloc[index]) # The cell in the dataframe we've hit as we iterate

			tmp_str += df_cell + "\t"
			count +=1

		print(tmp_str)

		index+=1

main()

#EOF