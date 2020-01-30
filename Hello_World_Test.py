'''
Author: Nick Hella

A simple "Hello World" Python program to demonstrate some of the symantics of the Python language

To run this file, (1.) open a terminal	(2.) move into the directory of this file 	(3.) run the command below

	python Hello_World_Test.py

Note, you made need to specify python3 instead of python if you have python2.x by default

'''

class Hello_World_Test:

  def main(self):
    print("Hello World!")
    return


# Defining "self", as an instance of the Hello_World_Test class
self = Hello_World_Test()

# Calling the function "main" within the Hello_World_Test class
self.main()


# NOTE: You can also run this program by invoking the following line of code:
# 	Hello_World_Test.main(self=None)


# Defining the "self" variable is just a pythonian thing to do, it's pretty common practice.


# Other basic language semantics:
'''

#'s are used for comments

Note: Triple single tics are used for declaring block-comments or even block-strings!



How to declare that a variable is null in Python

	my_null_variable = None

	# None = null



Declaring a list/array:

	my_list = list(())	or 	my_list = []


Getting the length of a list/array
	
	len(my_list)


Iterating through a list using a for-loop:

	for item in my_list:
		print(item)


Iterating through a list using a while loop:

	count = 0

	while count < len(my_list):
		
		print(my_list[count])

		count = count + 1	# note, you could also say count+=1


Searching for an item in a list:

	Exampel 1:

	# Let's say we want to print the element that contains the string "Test"

		my_list = ["This", "Example", "Is", "To", "Test", "Finding", "An", "Element", "In", "A", "List"]

		for element in my_list:

			if element == "Test":

				print("Found you!")

	Example 2:

	# Let's say we want to find the element that contains the sub-string "Test"

	my_list = ["This", "Example", "Is", "To", "Test Finding", "An", "Element", "In", "A", "List"]

		for element in my_list:

			if "Test" in element:

				print("Found you!")


Determinig if an element is in a list/array:

	# Let's say we want a boolean function to determine if an element is in a list:

	element_were_looking_for = "5"

	my_list = [0,1,2,3,4,5]

	if element_were_looking_for in my_list:
		print("True")

	# Note: Instead of having this if branch, you would simply write: print(element_were_looking_for in my_list)

	# This would return:
	>> True


How to break a String into an array/list.

	For this example, we'll use spaces as our delimeter:

		my_string = "This is an example string"

		my_string = my_string.split() 	

		# Note that priting my_string would now return: ["This", "is", "an", "example", "string"]

		# Instead of spaces, if you wanted to break the string apart by commas or any character for that matter,
		# simply use the "delimeter" argument, ie:

			my_string = my_string.split(delimeter=",")


Adding and deleting items to a list/array:

	# Declaring the list/array
	my_list = list(())

	# Adding an item to the list/array:
	my_list.append("Element1")

	# Note: if you were to print my_list, it would return: ["Element1"]

	# Deleting the element from the list
	del my_list[0]



Note that in Python, you don't need to delcare the data type of a variable. eg:


Delcaring a String:

	my_sting = "foo"


Iterating through characters in a String:

	for char in my_string:
		print(char)

	# Note: you could also follow the while-loop demo above to 
	#		achieve the same results.


Declaring an Int:
	
	my_int = 1


Declaring a Double:

	my_double = 1.5


Opening a txt file and reading line-by-line:

	Mode	Description
	'r'		This is the default mode. It Opens file for reading.
	'w'		This Mode Opens file for writing. 
			If file does not exist, it creates a new file.
			If file exists it truncates the file.
	'w+'	Same as w, but if the file doesn't already exist,
			it will be created automatically.
	'x'		Creates a new file. If file already exists, the operation fails.
	'a'		Open file in append mode. 
			If file does not exist, it creates a new file.
	'a+'	Same as a, but if the file doesn't already exist,
			it will be created automatically.
	't'		This is the default mode. It opens in text mode.
	'b'		This opens in binary mode.

	Example code for reading demo.txt line-by-line:

		f = open("demofile.txt", "r")
		for x in f:
		  print(x)

		# close the file
		f.close()



Lastly, if you don't declare a class in your python program, ie:

	def main():
		print("Hello world!")

You can run this program a couple different ways:

	1.) Natively call the main method,

			def main():
				print("Hello world")

			if __name__=="__main__":
				main()

		This is pretty much synonymous to Java when you say:

			public static void main(String[] args)

	2.) Call the function at the end of the file

			def main():
				print("Hello world")

			main()



'''
# EOF