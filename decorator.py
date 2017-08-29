import querybuilder
import web
import json
import jwt
from flask import request,make_response
options = {
   'verify_signature': True,
   'verify_exp': True,
   'verify_nbf': True,
   'verify_iat': True,
   'verify_aud': True,
   'require_exp': False,
   'require_iat': False,
   'require_nbf': False
}

class Authentication (object):

    def __init__ (self, func):
        self.func = func
    
    def add_response_headers(self,*args):
        
        resp = make_response(self.func(self,*args))
        h = resp.headers
        
        if request.headers.get("Authorization"):
            h['Authorization']=request.headers.get("Authorization")

        for header, value in args[0]['headers'].items():
            h[header] = value
        return resp


    def check_user(self,*args):
        uesrs = querybuilder.QueryBuilder('raj','users')
        params={"id":self.user,"password":self.password}
        select = ["id","password","name","age"]
        results=uesrs.read(select,params)
        if len(list(results)) ==0:
            return False
        else:
             return True

    def check_auth(self,*args):       

        self.auth=request.headers.get("Authorization")
        self.user=request.headers.get("USER")
        self.password=request.headers.get("PASSWORD")

        if self.auth:
            print(self.auth)
            try:
                payload = jwt.decode(self.auth,'secret')
                print(payload)
                return self.func(self,*args)
            except jwt.InvalidTokenError:                
                error = {'error':'Token is invalid'}
                return json.dumps(error)

        elif self.user and self.password:
            res = self.check_user()
            if res==True:
                return self.func (self,*args)
            elif res==False:
                error = {'error':'Invalid logged in User'}
                return error
            else:
                error = {'error':'unable to fecth data'}
                return error

        else:
            result ={
                    "error":"Invalid Authentication"
                } 
            return result
        return result

    def __call__ (self, *args):
        print(args)
        try:
            if len(args)!=0 and args[0]['headers']:
                print("add_response_headers")      
                return self.add_response_headers(*args)
            else:
                print("check_auth")
                return self.check_auth(*args) 
        except:
            print("check_auth")
            return self.check_auth(*args)
            
       

 