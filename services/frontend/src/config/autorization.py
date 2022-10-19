class Credenciales:
    USER = "admin"
    PASSWORD = "admin"

    def __init__(self, username:str = None, password:str = None):
        if username is not None:
            self.USER = username
        if password is not None:
            self.PASSWORD = password


