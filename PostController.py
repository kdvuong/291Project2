from DbConnection import db

class PostController:
    def __init__(self):
        self.collection = db['Posts']
    def get(self):
        return

    def add(self, post):
        return
    
    def addMany(self, posts):
        self.collection.insert_many(posts)
        print("done")

    def delete(self):
        return

    def update(self):
        return