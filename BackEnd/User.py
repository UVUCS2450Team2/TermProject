"""
    This class is to hold the data relevant to the user of the application. 
    It contains the Username and password and permissions

    The most important aspect is the permissions, which is a series of strings that act as flags
    which clearly state what the user is allowed to d.

    The Actions so far are :

    ADD 

    EDIT

    DELETE

    The GUI needs to verify that any actions requested by the user is allowed. 
"""


class User:
    def __init__(self, username, password, actions):
        self.username = username
        self.password = password
        self.Permissions = actions
    
    def isActionAllowed(self, action):
        res = [x for x in self.Permissions if action in x]

        return True if len(res) >= 1 else False
    
    def Dump(self):
        print(self.username, self.password)
        print(self.Permissions)
        print()