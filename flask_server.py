
import querybuilder
import json
import decorator
import jwt
import datetime
import time
import copy
from flask import Flask,request
app = Flask(__name__)



class formresponse():
	@decorator.Authentication
	def returnFunc(self,header, data):		
		return json.dumps(data)

class UserLogin(formresponse):
	def login(self):
		json_dict = request.get_json()
		uesrs = querybuilder.QueryBuilder('raj','users')
		#loaded_r = json.dumps(json_dict)
		params = {'id': json_dict['user'], 'password': json_dict['password']}
		uesrs = querybuilder.QueryBuilder('raj','users')
		select = ["id","password","name","age"];
		results=uesrs.read(select,params);
		output = {'data':[]}
		empty = {"error":"Invalid User namr / Password"}
		 
		try:
			for row in next(results):			 
				mapObj={}			 
				mapObj["id"] = row[0]
				mapObj["password"] = row[1]
				mapObj["name"] = row[2]
				mapObj["age"] = row[3]
				mapObj["message"] ='logged successfully'
				output["data"].append(mapObj)
			jwtObj = copy.deepcopy(mapObj)
			jwtObj['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
			jwt_payload = jwt.encode(jwtObj, 'secret')	
			print(jwt_payload)		 
			headers = {
				'headers':{
					'Token':jwt_payload,
					'Content-Type':'application/json',
					'status_code':200
					}
			}
			return self.returnFunc(headers,output)
		except StopIteration:
			return json.dumps(empty) 

class UserRegisteration(UserLogin,formresponse):
	def create_user(self):
		json_dict = request.get_json()
		uesrs = querybuilder.QueryBuilder('raj','users')
		#loaded_r = json.dumps(json_dict)
		data = {'name': json_dict['name'], 'age': json_dict['age'], 'password': json_dict['password']}
	 	headers = {
				'headers':{					
					'Content-Type':'application/json',
					'status_code':200
					}
			}
		return self.returnFunc(headers,uesrs.create(data))

class Users(formresponse):	
	@decorator.Authentication
	def user_list(self):
		print("user_list")
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
				mapObj["password"] = row[1]
				mapObj["name"] = row[2]
				mapObj["age"] = row[3]
				output["data"].append(mapObj)
			headers = {
				'headers':{					 
					'Content-Type':'application/json',
					'status_code':200
					}
			}
			return formresponse.returnFunc(headers,output)
		except StopIteration:
			return json.dumps(empty)
    
		
	@decorator.Authentication 
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
				mapObj["password"] = row[1]
				mapObj["name"] = row[2]
				mapObj["age"] = row[3]			
				output["data"].append(mapObj)
			headers = {
				'headers':{					 
					'Content-Type':'application/json',
					'status_code':200
					}
			}
			return formresponse.returnFunc(headers,output)
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
	print("test")
	return apiObj.user_list()

@app.route('/create_user',methods=['POST'])
def route_create_user():
	return apiObj.create_user()

@app.route('/login',methods=['POST'])
def route_login():
	return apiObj.login()
    		

app.run()
    