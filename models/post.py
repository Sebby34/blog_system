from datetime import datetime #Needed to get the current date and time
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
    #^Marks the post as unpublished rather than deleting, keeps it in memeory so it can be republished 
    #or edited later
    


