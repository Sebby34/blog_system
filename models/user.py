class User: 
    def __init__(self, username, password):
        self.username=username
        self.password=password
        self.role="user"
        self.is_banned=False
    
    def get_username(self):
        return self.username
    
    def check_password(self, password):
        return self.password == password

    def ban(self):
        self.is_banned=True

    def unban(self):
        self.is_banned=False
    
    def __str__(self):
        return f'Username: {self.username} | Role: {self.role} | Banned: {self.is_banned}'

class Admin(User): 
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role="admin"

class Author(User): 
    def __init__(self, username, password): 
        super().__init__(username, password)
        self.role="author"

class Reader(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role="reader"
        


    
              