from models.user import Admin, Author, Reader
from models.post import Post
from storage.file_manager import session, User as DBUser, Post as DBPost
from datetime import datetime
from sqlalchemy import select, or_, and_

class BlogService:
    def __init__(self):
        self.current_user=None
    
    def register_user(self, user):
        stmt = select(DBUser).where(DBUser.username == user.get_username())
        existing = session.execute(stmt).scalar_one_or_none()
        if existing: 
            print(f'Username: {user.get_username()} already exists.')
            return False
        db_user = DBUser(
            username = user.get_username(),
            password = user.password,
            role = user.role,
            is_banned = user.is_banned
        )
        session.add(db_user)
        session.commit()
        print(f'User: {user.get_username()} registered sucessfully')
        return True
    #^ Above checks if username already exists or not
    #The True and False return values are to be used in the main program to determine if registration was successful or not

    def create_post(self, title, content):
        if not self.current_user: 
            print("No user is logged in.")
            return False 
        if self.current_user.role not in ["admin", "author"]:
            print(f'{self.current_user.get_username()} does not have permission to create posts.')
            return False
        
        db_post = DBPost(
            title = title,
            content = content,
            author = self.current_user.get_username(),
            is_published = False
        )
        session.add(db_post)
        session.commit()
        print(f'Post created by {self.current_user.get_username()}')
        return True
    
    def publish_post(self, post_id):
        #^Finds a post by it's postID and calls the publish() method
        stmt = select(DBPost).where(DBPost.id == post_id)
        db_post = session.execute(stmt).scalar_one_or_none()
        if db_post:
            db_post.is_published = True
            db_post.creation_date = datetime.now()
            session.commit()
            print(f'Post: {db_post.title} published successfully')
            return True
            #^Publishes if exists
        print(f'No post found with ID: {post_id}')
        return False
    
    def edit_post(self, post_id, new_title, new_content): 
        #^Finds post by the post id and updates the title and content
        if not self.current_user:
            print("No user is logged in.")
            return False 
        stmt = select(DBPost).where(DBPost.id == post_id)
        db_post = session.execute(stmt).scalar_one_or_none()
        if not db_post: 
            print(f'No post found with ID: {post_id}')
            return False
        if self.current_user.role != "admin" and db_post.author != self.current_user.get_username(): 
            print(f'{self.current_user.get_username()} does not have permission to edit this post.')
            return False 
        
        db_post.title = new_title  
        db_post.content = new_content
        session.commit()
        print(f'Post: {db_post.title} edited successfully')
        return True
    
    def delete_post(self, post_id):
        #^Finds post by post id and unpublishes it
        if not self.current_user:
            print("No user is logged in.")
            return False 
        stmt = select(DBPost).where(DBPost.id == post_id)
        db_post = session.execute(stmt).scalar_one_or_none()
        if not db_post: 
            print(f'No post found with ID: {post_id}')
            return False
        if self.current_user.role != "admin" and db_post.author != self.current_user.get_username(): 
            print(f'{self.current_user.get_username()} does not have permission to delete this post.')
            return False 
        db_post.is_published = False
        session.commit()
        print(f'Post: {db_post.title} has been unpublished successfully')
        return True

    def search_posts(self, keywords, mode = "AND"): 
        #^Search posts by keywords in title or content 
        if not keywords: 
            print("No keywords provided.")
            return []
        conditions = [
            DBPost.title.contains(k) | DBPost.content.contains(k)
            for k in keywords
        ]
        if mode.upper() == "OR": 
            keyword_filter = or_(*conditions)
        else: 
            keyword_filter = and_(*conditions)
        stmt = select(DBPost).where(
            DBPost.is_published == True,
            keyword_filter
        )    
        results = session.execute(stmt).scalars().all()
        if not results: 
            print("No posts found matching keywords.")
        return results

    def login_user(self, username, password): 
        stmt = select(DBUser).where(DBUser.username == username)
        db_user = session.execute (stmt).scalar_one_or_none()
        if not db_user or db_user.password != password: 
            print("Invalid username or password")
            return False
        if db_user.is_banned: 
            print(f'User {username} is banned and cannot log in.')
            return False
        role_lower = db_user.role.lower()
        if role_lower == "admin": 
            self.current_user = Admin(db_user.username, db_user.password)
        elif role_lower == "author": 
            self.current_user = Author(db_user.username, db_user.password)
        else: 
            self.current_user = Reader(db_user.username, db_user.password)
        print(f'{username} logged in successfully!')
        return True
    #^verifies username and password, if correct sets current user
    
    def get_all_posts(self): 
        stmt = select(DBPost)
        return session.execute(stmt).scalars().all()
    #^Returns all posts regardless of published or not
    
    def get_published_posts(self): 
        stmt = select(DBPost).where(DBPost.is_published == True)
        return session.execute(stmt).scalars().all()
    #^Returns only published posts
    
                
