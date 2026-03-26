from datetime import datetime 
class Post:
    def __init__(self, post_id, title, content, author):
        self.post_id=post_id
        self.title=title
        self.content=content
        self.author=author
        self.creation_date=None
        self.is_published=False
    
    def publish(self):
        self.is_published=True
        self.creation_date= datetime.now()
    
    def edit(self, new_title, new_content):
        self.title=new_title
        self.content=new_content

    def delete(self):
        self.is_published=False
   
    


