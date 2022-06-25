from nameko.rpc import rpc

import dependencies

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def regis(self, a, b):
        user = self.database.regis(a, b)
        return user
    
    @rpc
    def login(self, a, b):
        user = self.database.login(a, b)
        return user
    
    @rpc
    def fileupload(self, a, b):
        user = self.database.fileupload(a, b)
        return user
    
    @rpc
    def checkUser(self, a, b):
        user = self.database.checkUser(a, b)
        return user