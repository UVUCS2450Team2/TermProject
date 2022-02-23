"""
    This class is an interface that will act as the middleman betweent the front and backend. 
    Details may change in either but what is implemented here is uniform across all iterations.

    Nothing should be removed(?), only expanded upon.

    Other classes will inherit from this based on needs

    These functions must never be implemented.
"""


class ApplicationInterface:
    def __init__(self, backend):
        self.Backend = backend
    
    def InitalizeBackend(self):
        """
            This function is used as the start up for the backend implementation currently used
            Not always necerssary
        """

    def VerifyLogin(self, user, password):
        """
            This function takes care of the verify login request that is initated by the user via the GUI button. It returns a boolean value
        """
        pass

    def request_employees(self):
        """
            This function returns a list of employees, used by the front end in a formatted way.
        """
        pass

    def export_payroll(self):
        """
            This function creates an exported CSV file of the employees payroll. Returns boolean for success
        """
        pass
    
    def add_employee(self, emp):
        """
            This function takes as parameters an employee object and adds its to the database in the backend
        """
        pass
    
    def update_employee(self, empID, emp):
        """
            This function takes as parameters the employees ID that needs to be updated, and an employee class that will replace it.
            Returns boolean value if operation was successful
        """
        pass

    def remove_employee(self, empID):
        """
            This function takes as a parameter the employee ID that needs to be removed from records. 
            Returns a boolean value if operation was successful
        """
    
    def verify_permission(self, action):
        """
            This function calls a black box in the backend to verify whether the user is allowed to do the action that is being requested.
            These actions have a string name and must be used uniformly.
        """