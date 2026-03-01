class User: 
    def __init__(self, username, password):
        self.username=username
        self.password=password
        self.role="user"
        self.is_banned=False
    #^ Above would do the following: 
    #If we created the a user object: user1=User("Sebastian", "Sebby34")
    #Python would automatically create: 
    #user1.username -> "Sebastian"
    #user1.password -> "Sebby34"
    #user1.role -> "user"
    #user1.is_banned -> False
    def get_username(self):
        return self.username
    
    def check_password(self, password):
        return self.password == password
    #^Verifies password

    def ban(self):
        self.is_banned=True
    #^Bans user

    def unban(self):
        self.is_banned=False
    #^Unbans user
    
    def __str__(self):
        return f'Username: {self.username} | Role: {self.role} | Banned: {self.is_banned}'
    #^Outputs the user object as a well formatted string 

class Admin(User): 
    #^Admin class inherits from User class hence the (User), makes us not have to repeat code
    def __init__(self, username, password):
        super().__init__(username, password)
        #^The above calls the __init__ method of the User class so we dont repeat code
        self.role="admin"

class Author(User): 
    def __init__(self, username, password): 
        super().__init__(username, password)
        self.role="author"

class Reader(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role="reader"
        


    
              