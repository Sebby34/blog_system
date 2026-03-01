from models.user import Admin, Author, Reader
from services.blog_service import BlogService

import re

def display_menu(user):
    if isinstance(user, Admin):
        print("\nAdmin Menu: ")
        print("1. View All Users")
        print("2. Delete Any Post")
        print("3. Ban User")
        print("4. Logout")
    elif isinstance(user, Author):
        print("\nAuthor Menu: ")
        print("1. Create Post")
        print("2. Edit Post")
        print("3. Delete Post")
        print("4. View My Posts")
        print("5. Logout")
    elif isinstance(user, Reader): 
        print("\nReader Menu: ")
        print("1. View Published Posts")
        print("2. Search Posts")
        print("3. Logout")

def get_menu_choice(prompt, valid_choices): 
    while True: 
        choice=input(prompt).strip()
        if choice in valid_choices: 
            return choice
        print(f'Invalid choice. Please select from {valid_choices}.')
        #^Ensures the user selects a valid menu option, loops until done

def handle_author_actions(blog_system):
    action= get_menu_choice("\nChoose an action: ", ["1", "2", "3", "4", "5"])

    if action =="1": 
        title= get_nonempty_input("Enter title: ")
        content= get_nonempty_input("Enter content: ")
        blog_system.create_post(title, content, blog_system.current_user)
    #^Creating post
    elif action== "2":
        try: 
            post_id=int(input("Enter post ID to edit: "))
            new_title=get_nonempty_input("Enter the new title: ")
            new_content=get_nonempty_input("Enter the new content: ")
            blog_system.edit_post(post_id, new_title, new_content)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")
            #^Error handling for invalid post ID
    #^Editing post
    elif action== "3":
        try: 
            post_id=int(input("Enter post ID to delete: "))
            blog_system.delete_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")
            #^Error handling for invalid post ID
    #^Deleting post
    elif action=="4": 
        for post in blog_system.posts:
            if post.author== blog_system.current_user.get_username():
                print(f'{post.title} | Published: {post.is_published} | Date: {post.creation_date}')
    #^Viewing posts
    elif action== "5": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None
    #^Logout
    else: 
        print("Invalid action!")

def handle_admin_actions(blog_system): 
    action = get_menu_choice("\nChoose an action: ", ["1", "2", "3", "4"])
    if action== "1": 
        for user in blog_system.users: 
            print(f'Username: {user.username}, Role: {user.role}, Banned: {user.is_banned}')
    #^View all users
    elif action== "2": 
        try: 
            post_id=int(input("Enter your post ID to delete: "))
            blog_system.delete_post(post_id)
        except ValueError: 
            print("Invalid post ID. Please enter a valid integer.")
            #^Error handling for invalid post ID
    #Delete any post
    elif action== "3": 
        username=get_nonempty_input("Enter username to ban: ")
        for user in blog_system.users: 
            if user.username.lower()== username.lower(): 
                user.ban()
                print(f'{username} has been banned')
                break
        else: 
            print("User not found")
    #^Ban user
    elif action== "4": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None
    #^Logout 
    else: 
        print("Invalid action!")
    
def handle_reader_actions(blog_system): 
    action= get_menu_choice("\nChoose an action: ", ["1", "2", "3"])
    if action=="1": 
        for post in blog_system.posts: 
            if post.is_published: 
                print(f'{post.title} | Published: {post.is_published} | Date: {post.creation_date}')
            #^View published posts
    elif action== "2": 
        keywords=get_nonempty_input("Enter keywords separated by spaces: ").split()
        patterns= [re.compile(re.escape(key), re.IGNORECASE) for key in keywords]
        #^Treats user input as literal (symbols and all), case insensitive
        found=False
        for post in blog_system.posts:
            if any(pattern.search(post.title) or pattern.search(post.content) for pattern in patterns):
                print(f'Found: {post.title} | Published: {post.is_published} | Date: {post.creation_date}')
                found=True
        if not found:
            print("No posts matched your search.")
            #Searches multiple keywords in both title and content
    elif action== "3": 
        print("Logging out. Goodbye!")
        blog_system.current_user= None
            #^Logout
    else: 
        print("Invalid action!")

def get_nonempty_input(prompt): 
    while True: 
        value=input(prompt).strip()
        if value: 
            return value
        print("Input cannot be empty. Please try again.")
        #^Ensures the input is not empty, keeps asking until valid input is given 

def main(): 
    blog_system=BlogService()

    admin1= Admin("AdminSebastian", "Sebby34")
    author1= Author("Stephen", "King123")
    reader1= Reader("Lyla", "Lylab123")
    
    blog_system.register_user(admin1)
    blog_system.register_user(author1)
    blog_system.register_user(reader1)
    #^Register Users

    username=get_nonempty_input("Enter your username: ")
    password=get_nonempty_input("Enter your password: ")
    
    if blog_system.login_user(username, password): 
        print(f'Welcome {blog_system.current_user.get_username()}!')
        while blog_system.current_user: 
            display_menu(blog_system.current_user)

            if isinstance(blog_system.current_user, Admin): 
                handle_admin_actions(blog_system)
                #^If user is admin call admin actions
            elif isinstance(blog_system.current_user, Author): 
                handle_author_actions(blog_system)
                #^if user is author call author actions
            elif isinstance(blog_system.current_user, Reader): 
                handle_reader_actions(blog_system)
                #^if user is reader call reader actions 
    else: 
        print("Login failed! Please try again")
    



if __name__ == "__main__": 
        main()