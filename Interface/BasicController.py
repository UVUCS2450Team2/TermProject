from Interface import *
from Interface.Interface import ApplicationInterface

"""
    This class implements functions from the Application Interface. 
    It is the first variant of the prototype.
"""
from TermProject.Backend.Backend import *

class BasicControlller(ApplicationInterface):
    def __init__(self):
        ApplicationInterface.__init__(self, BackendImplementation())
