import json
import os
import string
from sys import flags
import requests as req
from unittest import result
from xml.etree.ElementTree import tostring

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from session import SessionProvider

class GatewayService:
    name = 'gateway'

    database = RpcProxy('user_service')
    session_provider = SessionProvider()
    
    @http('POST', '/regis')
    def regis(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        nrp = ""
        nama = "" 
        email = ""
        password = "" 
        for el in arr:
            node     = el.split("=")
            if node[0] == "nrp":
                nrp = node[1]
            if node[0] == "nama":
                nama = node[1]
            if node[0] == "email":
                email = node[1]
            if node[0] == "password":
                password = node[1]
        rooms = self.database.regis(nrp, nama, email, password)
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

            nrp = ""
            password = "" 
            for el in arr:
                node     = el.split("=")
                if node[0] == "nrp":
                    nrp = node[1]
                if node[0] == "password":
                    password = node[1]
            flags = self.database.login(nrp, password)
            
            if(flags == 1):
                user_data = {
                    'nrp': nrp,
                    'password': password
                }
                session_id = self.session_provider.set_session(user_data)
                response = Response(str(user_data))
                response.set_cookie('SESSID', session_id)
                return response
            else:
                result = []
                result.append("NRP/password incorrect")
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
        
    @http('POST', '/uploadfile')
    def uploadfile(self, request):
        cookies = request.cookies
        
        
        if cookies:
            judul = request.form['judul']
            abstract = request.form['abstract']
            confirm = self.session_provider.get_session(cookies['SESSID'])
            temp = json.dumps(confirm)
            temp = json.loads(temp)
            
            pcFile = request.files['data']
            
            flags = self.database.uploadfile(temp["nrp"], pcFile.filename, judul, abstract);
            if flags == 0:
                if os.path.exists("upload/"):
                    pcFile.save("upload/"  + pcFile.filename);
                else:
                    os.makedirs("upload/")
                    pcFile.save("upload/" + pcFile.filename);
                result = []
                result.append("Upload success")
                return json.dumps(result)
            else:
                result = []
                result.append("Upload failed, the data with the same filename and abstract already exists")
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
            flags = self.database.checkUser(temp["nrp"], fileName);
            if flags == 1:
                path = "upload/" + fileName
                return Response(open(path, "rb").read())
            else:
                result = ("File does not exist")
                return json.dumps(result)
        else:
            response = Response('Login Required')
            return response