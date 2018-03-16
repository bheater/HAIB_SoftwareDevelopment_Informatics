# This Python file uses the following encoding: utf-8
import os, sys
import mysql.connector
from mysql.connector import errorcode
from flask import Flask
from flask import jsonify

# create an instance of this class. 
app = Flask(__name__,)
# The first argument is the name of the application’s module or package.
# If you are using a single module (as in this example), you should use __name__ 
# because depending on if it’s started as application or imported as module 
# the name will be different ('__main__' versus the actual import name).
# This is needed so that Flask knows where to look for templates, static files, and so on. 


try:
	 #cnx = mysql.connector.connect(user='scott',database='testt')
	# Establish a connection to the database.
	cnx = mysql.connector.connect(user='hardy', password = 'c4S4z5RHZ8VW', database = 'hardy_weinberg', host = 'hardy-weinberg.haib.org')
	#cnx = mysql.connector.connect(user='bheater', password = 'S4EuaUXh', database = 'hardy_weinberg', host = 'hardy-weinberg.haib.org')
	print('connected!')
	
	# Create a cursor to execute changes within the database.
	try:
		cursor = cnx.cursor(buffered=True)
	except:
		print('error connecting cursor')
		
	
	DB_NAME = 'hardy_weinberg'
	#drop_database(cnx,DB_NAME)
	
	
	# use the route() decorator to tell Flask what URL should trigger our function.
	@app.route('/')
	def get_hw_data():
		"""
		views = ['gnomad_genome_ref_alt_seq','gnomad_exome_ref_alt_seq']
		for view in views:
			query = '''SELECT e.chrom,e.position,e.ref,e.alt,e.neg_log10_Pval
				FROM {} AS e 
				WHERE e.expected0>5 AND e.expected1>5 AND e.expected2>5 
				ORDER BY e.chrom, e.position
				'''.format(view)
			cursor.execute(query)
		"""
		query = 'SHOW TABLES'
		print(query)
		cursor.execute(query)
		'''
		for item in cursor.fetchall():
			print item
		#print (cursor.cursor)
		'''
		
		rows = []
		for row in cursor:
			rows.append(str(row))
			print(row)
			#= cursor.fetchall()
		
		cursor.close()
	
		return items
	

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
#else:
#	cnx.close()

print('it works!')



'''
To run the application you can either use the flask command or python’s -m switch with Flask.
Before you can do that you need to tell your terminal the application to work with
by exporting the FLASK_APP environment variable:

$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
If you are on Windows you need to use set instead of export.

Alternatively you can use python -m flask:

$ export FLASK_APP=hello.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
This launches a very simple builtin server, which is good enough for testing
but probably not what you want to use in production. For deployment options see Deployment Options.
'''
if __name__ == "__main__":
    # '0.0.0.0' run flash at IP address to broadcast instead of running it locally.
    app.run('0.0.0.0')
    