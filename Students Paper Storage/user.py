from nameko.rpc import rpc

import dependencies

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def regis(self, a, b, c, d):
        user = self.database.regis(a, b, c, d)
        return user
    
    @rpc
    def login(self, a, b):
        user = self.database.login(a, b)
        return user

    @rpc
    def post_news(self, desc, file):
        news = self.database.post_news(desc, file)
        return news
    
    @rpc
    def uploadfile(self, a, b, c, d):
        user = self.database.uploadfile(a, b, c, d)
        return user
    
    @rpc
    def checkUser(self, a, b):
        user = self.database.checkUser(a, b)
        return user