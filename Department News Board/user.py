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
    def get_all_news(self):
        news = self.database.get_all_news()
        return news

    @rpc
    def get_news(self, newsid):
        news = self.database.get_news(newsid)
        return news
    
    @rpc
    def post_news(self, desc, file):
        news = self.database.post_news(desc, file)
        return news
    
    @rpc
    def edit_news(self, id, desc):
        news = self.database.edit_news(id, desc)
        return news
    
    @rpc
    def delete_news(self, id):
        news = self.database.delete_news(id)
        return news
    
    @rpc
    def download(self, id):
        news = self.database.download(id)
        return news