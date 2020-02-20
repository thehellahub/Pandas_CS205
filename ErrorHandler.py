import traceback
import os
import glob
import sys

log = None
debug = 0

class ErrorHandlerContext:

	def __init__(self,_debug, function_name):
		self.debug = debug
		self.function_name = function_name

	def __enter__(self):
		self.log = log

	def remove_csv2_files_and_db_file(self):
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

	def __exit__(self,exc_type,exc_value,traceback_):

		exc_lines = traceback.format_exc().split("\n")
		try:
			punchline = exc_lines[-2]
		except:
			punchline = None

		if self.debug:
			print("\n\n EXIT FUNCTION IN ERROR HANDLER PINGED")

		if (exc_type is None and exc_value is None and traceback_ is None):
			return

		if str(exc_type).strip() == "<class 'SystemExit'>":
			print("Exit command detected. Removing .CSV2 files if exists.. \n\n")
			self.remove_csv2_files_and_db_file()
			return
			
		if str(punchline).strip() == "KeyboardInterrupt":
			print("\n\n SIGKILL Detected. Removing .CSV2 files if exists.. \n\n")
			self.remove_csv2_files_and_db_file()
			sys.exit()
			return

		else:

			exc_lines = traceback.format_exc().split("\n")
			try:
				punchline = exc_lines[-2]
			except:
				punchline = None

			if debug:
				print("\n\n ERROR DETECTED: " + \
					" \nFUNCTION: " + str(self.function_name) 	+ \
					" \nEXC TYPE: " + "\n\n" + str(exc_type) 	+ \
					" \nEXC VALUE: " + "\n\n" + str(exc_value) 	+ \
					" \nPUNCHLINE: " + "\n\n" + str(punchline) 	+ \
					" \nERROR TRACEBACK: " + "\n\n" + str(traceback_) )

				print("\n\n Removing .csv2 files if exists")
			self.remove_csv2_files_and_db_file()

		return

def error_handler(debug,function_name):
	# https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
	def actual_decorator(f):
		def wrapper(*args, **kwargs):
			with ErrorHandlerContext(debug, function_name) as context:
				return f(*args, **kwargs)
		return wrapper
	return actual_decorator