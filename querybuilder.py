import MySQLdb
class QueryBuilder(object):
	def __init__(self,db,table):
		print("QueryBuilder init")
		db=MySQLdb.connect("localhost","root","",db)
		self.dbc=db.cursor()
		self.table=table
		self.db=db
		
	def read(self,selectFields,conditionFields):
		""" Generates SQL for a SELECT statement matching the conditionFields passed. """
		""" selectFields = ["id","password","name","age"];"""
		""" conditionFields={"id":1}"""
		
		sql = list()
		
		if selectFields:
			sql.append("SELECT " + " , ".join("%s" % (k) for k in selectFields))
		else:
			sql.append("SELECT *")
			
		sql.append(" FROM %s " % self.table)
		if conditionFields:
			sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in conditionFields.iteritems()))
		sql.append(";")
		sql="".join(sql)
		print(sql)		
		self.dbc.execute(sql)
		results = self.dbc.fetchall()
		if len(results) !=0:
			yield list(results)
		if len(results) ==0:			
			return
			
	def create(self,insertData):
		""" create into objects table (update if the row already exists)
			given the key-value pairs in kwargs """
	 
		keys = ["%s" % k for k in insertData]
		 
		values = ["'%s'" % v for v in insertData.values()]
		 
		sql = list()
		sql.append("INSERT INTO %s (" % self.table)
		sql.append(", ".join(keys))
		sql.append(") VALUES (")
		sql.append(", ".join(values))
		sql.append(") ON DUPLICATE KEY UPDATE ")
		sql.append(", ".join("%s = '%s'" % (k, insertData[k]) for k in insertData))
		sql.append(";")
		sql="".join(sql)
		try:
		  self.dbc.execute(sql)
		  self.db.commit()
		  success = {'message':'New record added'}
		  return success
		except:
		  print "Error: unable to insert data"
		  error = {'error':'unable to insert the data'}
		  return error
