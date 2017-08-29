
import querybuilder
import json
import auth_fl
from flask import Flask,request
app = Flask(__name__)

 

class UserRegisteration():
	def create_user(self):
		json_dict = request.get_json()
		uesrs = querybuilder.QueryBuilder('raj','users')
		#loaded_r = json.dumps(json_dict)
		data = {'name': json_dict['name'], 'age': json_dict['age'], 'password': json_dict['password']}
	 
		return json.dumps(uesrs.create(data))

class Users():	
	@auth_fl.Authentication
	def user_list(self):
		uesrs = querybuilder.QueryBuilder('raj','users')
		params={}
		select = ["id","password","name","age"]
		results=uesrs.read(select,params)
		output = {'data':[]}
		empty = {"error":"Invalid User"}
		try:
			for row in next(results):
				mapObj={}
				mapObj["id"] = row[0]
				mapObj["password"] = row[0]
				mapObj["name"] = row[2]
				mapObj["age"] = row[3]
				output["data"].append(mapObj)
			return json.dumps(output)
		except StopIteration:
			return json.dumps(empty)
    
		
	@auth_fl.Authentication 
	def get_user(self, user):
		uesrs = querybuilder.QueryBuilder('raj','users')
		params={"id":user}
		select = ["id","password","name","age"];
		results=uesrs.read(select,params);
		output = {'data':[]}
		empty = {"error":"Invalid User"}
		 
		try:
			for row in next(results):			 
				mapObj={}			 
				mapObj["id"] = row[0]
				mapObj["password"] = row[0]
				mapObj["name"] = row[2]
				mapObj["age"] = row[3]			
				output["data"].append(mapObj)
			
			return json.dumps(output)
		except StopIteration:
			return json.dumps(empty)

			
class Api(UserRegisteration,Users):
	def test(self):
		print("test")

apiObj = Api()

@app.route('/users/<user>')
def route_get_user(user):
	return apiObj.get_user(user)

@app.route('/users')
def route_user_list():
	return apiObj.user_list()

@app.route('/create_user',methods=['POST'])
def route_create_user():
	return apiObj.create_user()
    		

app.run()
    