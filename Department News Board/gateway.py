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
        
    @http('GET', '/all_news')
    def get_all_news(self, request):
        news = self.database.get_all_news()
        return json.dumps(news)
    
    @http('GET', '/all_news/<int:id>')
    def get_news(self, request, id):
        news = self.database.get_news(id)
        return json.dumps(news)
    
    @http('POST', '/post_news')
    def post_news(self, request):
        cookies = request.cookies
        if cookies:
            pcFile = request.files['data']
            data = request.form['desc']
            flags = self.database.post_news(data, pcFile.filename)
            if flags == 0:
                if os.path.exists("upload/"):
                    pcFile.save("upload/" + pcFile.filename);
                else:
                    os.makedirs("upload/")
                    pcFile.save("upload/" + pcFile.filename);
                result = []
                result.append("Upload success")
                return json.dumps(result)
            else:
                result = []
                result.append("Upload failed, the data with the same name already exists")
                return json.dumps(result)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)
        
    @http('POST', '/update_news/<int:id>')
    def edit_news(self, request, id):
        cookies = request.cookies
        if cookies:
            data = format(request.get_data(as_text=True))
            temp = req.utils.unquote(data)
            spt = temp.split("=")
            spt = spt[1]
            news = self.database.edit_news(id, spt)
            return json.dumps(news)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)
        
    @http('DELETE', '/delete_news/<int:id>')
    def delete_news(self, request, id):
        cookies = request.cookies
        if cookies:
            news = self.database.delete_news(id)
            if news != 0:
                os.remove("upload/" + news)
                result = []
                result.append("News deleted")
                return json.dumps(result)
            else:
                result = []
                result.append("Id not found")
                return json.dumps(result)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)
        
    @http('GET', '/download/<int:id>')
    def download(self, request, id):
        result = self.database.download(id)
        if result != 0:
            path = "upload/" + result
            return Response(open(path, "rb").read())
        else:
            result = ("File does not exist")
            return json.dumps(result)