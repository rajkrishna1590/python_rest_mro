import MySQLdb
import web
from flask import request

db=MySQLdb.connect("localhost","root","","raj")
c=db.cursor()

class Authentication (object):

    def __init__ (self, func):
        self.func = func

    def check_user(self,*args):
        sql = "select * from users where id="+self.user+" and password='"+self.password+"'"
        try:            
            c.execute(sql)
            results = c.fetchall()
            if len(results) ==0:
                return False
            else:
                return True
        except:
            print "Error: unable to fecth data"
            error = {'error':'unable to fecth data'}
            return error

    def check_auth(self,*args):       

        self.auth=request.headers.get("Authorization")
        self.user=request.headers.get("USER")
        self.password=request.headers.get("PASSWORD")

        if self.auth:
            
            return self.func (self,*args)

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
		return self.check_auth(*args)
       

 