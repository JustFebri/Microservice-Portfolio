from distutils.command.upload import upload
import json
import os
from sys import flags
from unittest import result
from xml.etree.ElementTree import tostring

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from requests import request
import requests
from werkzeug.wrappers import Response
from session import SessionProvider
import requests as req

class GatewayService:
    name = 'gateway'

    database = RpcProxy('user_service')
    session_provider = SessionProvider()
    
    @http('POST', '/regis')
    def regis(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 
        for el in arr:
            node     = el.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        rooms = self.database.regis(username, password)
        return json.dumps(rooms)
    
    @http('GET', '/login')
    def login(self, request):
        cookies = request.cookies
        if cookies:
            response = Response('Logout Required')
            return response
        else:
            data = format(request.get_data(as_text=True))
            arr  =  data.split("&")

            username = "" 
            password = "" 
            for el in arr:
                node     = el.split("=")
                if node[0] == "username":
                    username = node[1]
                if node[0] == "password":
                    password = node[1]
            flags = self.database.login(username, password)
            
            if(flags == 1):
                user_data = {
                    'username': username,
                    'password': password
                }
                session_id = self.session_provider.set_session(user_data)
                response = Response(str(user_data))
                response.set_cookie('SESSID', session_id)
                return response
            else:
                result = []
                result.append("Username/password incorrect")
                return json.dumps(result)
    
    @http('GET', '/check')
    def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            if (confirm):
                response = Response('Logout Successful')
                response.delete_cookie('SESSID')
            else:
                response = Response("Logout Failed")
            return response
        else:
            response = Response('Login Required')
            return response
        
    @http('POST', '/fileupload')
    def fileupload(self, request):
        cookies = request.cookies
        
        
        if cookies:
            confirm = self.session_provider.get_session(cookies['SESSID'])
            temp = json.dumps(confirm)
            temp = json.loads(temp)
            
            pcFile = request.files['data']
            
            flags = self.database.fileupload(temp["username"], pcFile.filename);
            if flags == 0:
                if os.path.exists("upload/" + temp["username"]):
                    pcFile.save("upload/" + temp["username"] + "/" + pcFile.filename);
                else:
                    os.makedirs("upload/" + temp["username"])
                    pcFile.save("upload/" + temp["username"] + "/" + pcFile.filename);
                result = []
                result.append("Upload success")
                return json.dumps(result)
            else:
                result = []
                result.append("Upload failed, the data with the same name already exists")
                return json.dumps(result)
        else:
            response = Response('Login Required')
            return response

    @http('GET', '/filedownload/<string:fileName>')
    def download(self, request, fileName):
        cookies = request.cookies
        if cookies:
            
            confirm = self.session_provider.get_session(cookies['SESSID'])
            temp = json.dumps(confirm)
            temp = json.loads(temp)
            flags = self.database.checkUser(temp["username"], fileName);
            if flags == 1:
                path = "upload/" + temp["username"] + "/" + fileName
                return Response(open(path, "rb").read())
            else:
                result = ("File does not exist")
                return json.dumps(result)
        else:
            response = Response('Login Required')
            return response