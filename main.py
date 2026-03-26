from models.user import Admin, Author, Reader
from services.blog_service import BlogService
from sqlalchemy import select
from storage.file_manager import User as DBUser, Post as DBPost, session
import re

def display_menu(user):
    role = user.role.lower()
    if role == "admin":
        print("\nAdmin Menu: ")
        print("1. View All Users")
        print("2. Publish Post")
        print("3. Delete Any Post")
        print("4. Ban User")
        print("5. Unban User")
        print("6. Logout")
    elif role == "author":
        print("\nAuthor Menu: ")
        print("1. Create Post")
        print("2. Edit Post")
        print("3. Publish Post")
        print("4. Delete Post")
        print("5. View My Posts")
        print("6. Logout")
    elif role == "reader": 
        print("\nReader Menu: ")
        print("1. View Published Posts")
        print("2. Search Posts")
        print("3. Logout")

# Ensures valid menu choice is selected
def get_menu_choice(prompt, valid_choices): 
    while True: 
        choice=input(prompt).strip()
        if choice in valid_choices: 
            return choice
        print(f'Invalid choice. Please select from {valid_choices}.')

def handle_author_actions(blog_system):
    action= get_menu_choice("\nChoose an action: ", ["1", "2", "3", "4", "5", "6"])
    current_user = blog_system.current_user

    # Create post
    if action =="1": 
        title= get_nonempty_input("Enter title: ")
        content= get_nonempty_input("Enter content: ")
        blog_system.create_post(title, content)

    # Edit post
    elif action== "2":
        try: 
            post_id=int(input("Enter post ID to edit: "))
            new_title=get_nonempty_input("Enter the new title: ")
            new_content=get_nonempty_input("Enter the new content: ")
            blog_system.edit_post(post_id, new_title, new_content)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")

    # Publish post
    elif action == "3": 
        try: 
            post_id = int(input('Enter post ID to publish: '))
            blog_system.publish_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")

    # Delete post
    elif action== "4":
        try: 
            post_id=int(input("Enter post ID to delete: "))
            blog_system.delete_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")

    # View post
    elif action=="5": 
        all_posts = blog_system.get_all_posts()
        for post in all_posts: 
            if post.author == current_user.get_username(): 
                print(f'{post.id} | {post.title} | Published: {post.is_published} | Date: {post.creation_date}')

    # Logout 
    elif action== "6": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None

    else: 
        print("Invalid action!")

def handle_admin_actions(blog_system): 
    action = get_menu_choice("\nChoose an action: ", ["1", "2", "3", "4", "5", "6"])
    current_user = blog_system.current_user

    # View users
    if action== "1": 
        users = session.execute(select(DBUser)).scalars().all()
        for user in users:
            print(f'Username: {user.username}, Role: {user.role}, Banned: {user.is_banned}')

    # Publish post 
    elif action == "2": 
        try: 
            post_id = int(input('Enter post ID to publish: '))
            blog_system.publish_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")

    # Delete post 
    elif action== "3": 
        try: 
            post_id=int(input("Enter your post ID to delete: "))
            blog_system.delete_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")

    # Ban user
    elif action== "4": 
        username=get_nonempty_input("Enter username to ban: ")
        user = session.execute(select(DBUser).where(DBUser.username == username)).scalar_one_or_none()
        if user: 
            user.is_banned = True
            session.commit()
            print(f'User: {username} has been banned.')
        else: 
            print("User not found.")

    # Unban user
    elif action == "5": 
        username=get_nonempty_input("Enter username to unban: ")
        user = session.execute(select(DBUser).where(DBUser.username == username)).scalar_one_or_none()
        if user: 
            user.is_banned = False 
            session.commit()
            print(f'User: {username} has been unbanned.')
        else: 
            print("User not found.")

    # Logout
    elif action== "6": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None
 
    else: 
        print("Invalid action!")
    
def handle_reader_actions(blog_system): 
    action= get_menu_choice("\nChoose an action: ", ["1", "2", "3"])
    current_user = blog_system.current_user

    # View published post 
    if action=="1": 
        posts = blog_system.get_published_posts()
        for post in posts:  
            print(f'{post.id} | {post.title} | Author: {post.author} | Date: {post.creation_date}')

    # Search posts
    elif action== "2": 
        keywords=get_nonempty_input("Enter keywords separated by spaces: ").split()
        posts = blog_system.search_posts(keywords)
        for post in posts: 
            print(f'{post.id} | {post.title} | Author: {post.author} | Date: {post.creation_date}')

    # Logout 
    elif action== "3": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None
    else: 
        print("Invalid action!")

def get_nonempty_input(prompt): 
    while True: 
        value=input(prompt).strip()
        if value: 
            return value
        print("Input cannot be empty. Please try again.")

def main(): 
    blog_system=BlogService()

    admin1= Admin("AdminSebastian", "Sebby34")
    author1= Author("Stephen", "King123")
    reader1= Reader("Lyla", "Lylab123")
    
    blog_system.register_user(admin1)
    blog_system.register_user(author1)
    blog_system.register_user(reader1)

    username=get_nonempty_input("Enter your username: ")
    password=get_nonempty_input("Enter your password: ")
    
    if blog_system.login_user(username, password): 
        print(f'Welcome {blog_system.current_user.get_username()}!')
        while blog_system.current_user: 
            display_menu(blog_system.current_user)
            role = blog_system.current_user.role.lower()
            if role == "admin": 
                handle_admin_actions(blog_system)
                
            elif role == "author": 
                handle_author_actions(blog_system)
                
            elif role == "reader": 
                handle_reader_actions(blog_system)
                
    else: 
        print("Login failed! Please try again")
    



if __name__ == "__main__": 
        main()