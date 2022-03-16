from Interface import *
from Interface.Interface import ApplicationInterface

from BackEnd.BackEnd import *

"""
    This class implements functions from the Application Interface. 
    It is the first variant of the prototype.
"""
from BackEnd.BackEnd import *

class BasicControlller(ApplicationInterface):
    def __init__(self):
        ApplicationInterface.__init__(self, BackendImplementation())
    
    def InitalizeBackend(self):
        """
            This function is used as the start up for the backend implementation currently used
            Not always necerssary
        """

    def VerifyLogin(self, user, password):
        """
            This function takes care of the verify login request that is initated by the user via the GUI button. It returns a boolean value
        """
        if self.Backend.VerifyLogin(user, password):
            self.Backend.SetActiveUser(user)
            return True
            
        return False
        

    def request_employees(self):
        """
            This function returns a list of employees, used by the front end in a formatted way.
        """

        return self.Backend.getEmployeesAsList()
        

    def export_payroll(self):
        """
            This function creates an exported CSV file of the employees payroll. Returns boolean for success
        """
        self.Backend.generatePayroll()

    def add_employee(self, emp):
        """
            This function takes as parameters an employee object and adds its to the database in the backend
        """
        self.Backend.AddEmployee(emp)

    def update_employee(self, empID, emp):
        """
            This function takes as parameters the employees ID that needs to be updated, and an employee class that will replace it.
            Returns boolean value if operation was successful
        """
        return self.Backend.UpdateEmployee(empID, emp)
        

    def remove_employee(self, empID):
        """
            This function takes as a parameter the employee ID that needs to be removed from records. 
            Returns a boolean value if operation was successful
        """
        return self.Backend.RemoveEmployee(empID)
    
    def verify_permission(self, action):
        """
            This function calls a black box in the backend to verify whether the user is allowed to do the action that is being requested.
            These actions have a string name and must be used uniformly.
        """
        return self.Backend.VerifyPermission(action)
    

    def is_admin(self):
        """
            This function asks the backend if the current logged in user is an admin, this is used to verify rights and show particular views
        """
        return self.Backend.is_admin()


