from flask import Flask
from flask import jsonify
import pymysql.cursors


app = Flask(__name__)

@app.route("/")
def hello():
	try:
		cnx = pymysql.connect(user='hardy', password = 'c4S4z5RHZ8VW', database = 'hardy_weinberg', host = 'hardy-weinberg.haib.org',cursorclass=pymysql.cursors.DictCursor)
	except:
		print("connection not established")
	
	try:
		with cnx.cursor() as cursor:
			query = "SELECT chrom, position, ref, alt, neg_log10_Pval FROM gnomad_exome_ref_alt_seq WHERE chrom = %s AND	position = %s"
			param = ("1", "13372")
			cursor.execute(query,param)
			data = cursor.fetchall()
			print(data)
			'''
			query = "SHOW TABLES;"
			cursor.execute(query)
			table = cursor.fetchone()
			tables = cursor.fetchall()
			print(tables)
			'''
	#data = cur.fetchall()
	#print(data)
	#cursor.close()
	finally:
		cnx.close()
	# Load database results
	return jsonify(data)



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(debug=True, host='0.0.0.0')
