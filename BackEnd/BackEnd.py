"""
    This class is the backend implementation of the project.

    It encompasses the following :

    Read in a CSV file and file in a data structure array
    Manage a data structure array of empData
    Export a CSV file with formatted data from the data structure array



    In regards to the provided employees.csv : 
    Need clarification on what the difference between paymethod and classifications.
    paymethod = cheque or cash??



    Assume that the CSV's records are all formatted correctly. Meaning that no record is missing data.

    Not sure what to do with garbage data.


    Also need clarification on what the value (1,2,3) of the Classification field correlates to.
    Assume for now,

    1 = Hourly
    2 = Salary
    3 = Commissioned

"""

"""
    Details about the userlogin.csv file
    each entry is formatted as such :

    username, password, action, action,..., action

    This is my take on handling permissions.



    In regards to timecards and receipts:

    We will limit the timeframe to calculate the payroll to one month, meaning that timecards and receipts should have enough information
    to income in a given month.
"""

from collections import *

from BackEnd import *

"""PRODUCTION IMPORTS!"""
from BackEnd.empClass import *

from BackEnd.User import *
"""COMMENT OUT WHEN USING DEBUG!"""

"""DEBUG IMPORTS!"""
#from User import *
#from empClass import *
"""COMMENT OUT WHEN USING PRODUCTION!"""



import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class BackendImplementation:
    def __init__(self, empfile = "BackEnd/employees.csv", userfile = "BackEnd/userlogin.csv", timefile = "Backend/timecards.csv", receiptfile = "Backend/receipts.csv", payrollfile = "Backend/Payroll.csv"):
        self.EMP_DATA = []
        self.EMP_DICT = OrderedDict({})
        self.EMPfile = 0
        self.EMPFilename = empfile

        self.USER_DICT = OrderedDict({})
        self.USERfile = 0
        self.USERFilename = userfile

        self.TimeCard_DICT = OrderedDict({})
        self.TimeCardFilename = timefile
        self.TimeCardfile = 0

        self.Reciepts_DICT = OrderedDict({})
        self.RecieptsFilename = receiptfile
        self.Recieptsfile = 0

        self.PayrollFilename = payrollfile
        self.PayrollFile = 0


        self.ActiveUser = None

        safetyNET = True

        try:
            self.EMPfile = open(self.EMPFilename, 'r' )
            
        except:
            print("Error opening file.")
            safetyNET = False

        try:
            self.USERfile = open(self.USERFilename, 'r' )
            
        except:
            try:
                self.USERfile = open(resource_path("userlogin.csv"), 'x')
                self.USERfile.write("admin,password,True,ADD,EDIT,DELETE")
            except:
                print("Login file was not found and could not be created.")
                safetyNET = False
        
        try:
            self.TimeCardfile = open(self.TimeCardFilename, 'r')
        except:
            print("Timecard file was not found!")
            safetyNET = False
        
        try:
            self.Recieptsfile = open(self.RecieptsFilename, 'r')
        except:
            print("Receipts file was not found!")
            safetyNET = False
        
        if not safetyNET:
            #need to throw errors at the user to let them know?
            sys.exit()

     
        self.Read_LoginData()
        self.Read_EmployeeData()
        self.read_Timecards()
        
        

    def Read_LoginData(self):
        """
            Reads the userlogin.csv file and parses the information into User data structure array
        """
        lines = self.USERfile.readlines()

        for line in lines:
            words = line.split(',')

            words[len(words)-1] = words[len(words)-1].split('\n')[0]

            if 'True' in words[2]:
                self.USER_DICT[words[0]] = Admin(words[0], words[1], words[3:])    
            else:
                self.USER_DICT[words[0]] = User(words[0], words[1], words[3:])

    def Login_User(self, user, password):
        if self.VerifyLogin(user,password):
            self.SetActiveUser(user)
            return True
        
        return False

    def Read_EmployeeData(self):
        """
        Reads the employee.csv file and parses the information into the empClass data structure array
        """ 
   
        self.EMPfile = open(self.EMPFilename, 'r' )
        lines = self.EMPfile.readlines()


        for line in lines:

            words = line.split(',')
            words[12] = words[12].split('\n')[0]
            #print(words)

            """
            print(words)
                
            ID = 0
            Name = ""
            Address = ""
            City = ""
            State = ""
            Zip = 0
            Class = None
            Paymethod = 0
            Salary = 0
            Hourly = 0
            Commissioned = 0
            Route = ""
            Account = ""

            """

            empdetais = []

           

            if "ID" in words:
                continue
                
            

            fname = words[1].split(" ")
            lname = ""
            for i in range(1, len(fname)):
                lname += fname[i]
            fname = fname[0]

         

            emp = Employee(int(words[0]), fname, lname, words[2], words[3], words[4], int(words[5]), words[12], words[11], words[9], words[8], words[10], words[7], int(words[6]))

            """
                    if int(words[6]) == 1:
                        emp.make_hourly(float(words[9]))
                    elif int(words[6] == 2):
                        emp.make_salaried(int(words[8]))
                    elif int(words[6] == 3):
                        emp.make_commissioned(float(words[9], float(words[11])))
            """       

            #self.EMP_DICT[int(words[0])] = emp

            self.AddEmployee(emp)

            
        return

    def read_Timecards(self):
        """
            Read timecards.csv, parsing the text by removing the commas and new line character.
            Converting the array of strings into an array of floats and adding it to TimeCard_Dict for easy lookup
        """
        lines = self.TimeCardfile.readlines()

        for line in lines:
            words = line.split(',')
            words[len(words)-1] = words[len(words)-1].split('\n')[0]

            hours = []
            try:
                for el in words:
                    hours.append(float(el))
            except:
                print("Something went wrong parsing the timecards, is the data valid?")
            
            self.TimeCard_DICT[words[0]] = hours[1:]

            if not int(words[0]) in self.EMP_DICT:
                return False

            emp = self.EMP_DICT[int(words[0])]

            try:
                if not "Hourly" in emp.classification.asString():
                    return False
            except:
                return False

            for hour in hours[1:]:
                emp.classification.add_timecard(hour)

            """
                To append hours to an employee:
                employee.classification.add_timecards(float)

                if 'hourly' in employee.classification.AsString():
                     employee.classification.add_timecards(float)

            """
        return True

    
    def read_Receipts(self):
        '''Reads the receipts.csv and parses the file and stores the receipts in
            a dictionary. The key is the employee id the values are the values of 
            the receipts.
        '''
        lines = self.RecieptsFilename.readlines()
        for line in lines:
            words = line.strip().split(",")
            receipts = []
            try:
                for receipt in words:
                    receipts.append(float(receipt))
            except:
                print("Unable to parse receipts. Check if data is valid")
            self.Reciepts_DICT[words[0]] = receipts[1:]
            
    def generatePayroll(self):
        try:

            self.PayrollFile = open(self.PayrollFilename, 'w')
        except:
            print("Failed to open Payroll file")
            return

        """
        emppay = employee.classification.computepay()

        """

        self.PayrollFile.write("ID,Name,Address,Employee Type,Payment\n")

        for empl in self.EMP_DICT:
            empl = self.EMP_DICT[empl]
            #self.PayrollFile.write(key, emp.Name, emp.Address, emp.classification.asString(), emp.classification.computepay())
            self.PayrollFile.write(str(empl.emp_id) + "," +  empl.f_name + " " + empl.l_name + "," + empl.address + "," + empl.classification.asString() + "," + str(empl.classification.compute_pay()) + '\n')
        
        self.PayrollFile.close()
    def IsUserValid(self, username):
        """
            A function to quickly find if a user exists in memory
        """
        if username in self.USER_DICT:
            return True
        return False
        
    
    def VerifyLogin(self, username, password):
        """
            Function that returns true if the username and password credentials match up with 
            what is in the user data structure array
        """
        if not self.IsUserValid(username):
            return False
            
        user = self.USER_DICT[username]
        
        if not password == user.password:
            return False
        
        return True
        

    def SetActiveUser(self, user):
        """
            Set the user as the active user. This if for permissions to function.
        """
        self.ActiveUser = self.USER_DICT[user]


    def AddEmployee(self, emp):
        """
            Add a new employee to the data structure array, verifies the employee information first
        """

        if not self.VerifyEmployeeInformation(emp):
            return False
        self.EMP_DICT[emp.emp_id] = emp
        return True

    
    def UpdateEmployee(self, empID, emp):
        """
            Replace employee data in the data structure array based on ID. Requires that a new emp data be sent to function
        """
        if emp == None:
            return False

        if not self.VerifyEmployeeInformation(emp):
            return False
        
        self.EMP_DICT[empID] = emp
        return True
    
    def getEmployeesAsList(self):
        return self.EMP_DICT.values()
    
    def getUsersAsList(self):
        return self.USER_DICT.values()

    def RemoveEmployee(self, empID):
        """
            Remove the employee from the data structure array based on ID
        """
        emp = self.EMP_DICT.get(empID)

        if emp == None:
            return False
        
        del self.EMP_DICT[empID]
        return True
    
    def VerifyPermission(self, action):
        """
            Verify that the action is in the users permissions.
        """
        if self.ActiveUser == None:
            return False
        
        if action in self.ActiveUser.Permissions:
            return True
        
        return False
    
    def SaveEmployees(self):
        """
            Saves all contents of the employee dictionary to file
        """
        self.EMPfile.close()
        self.EMPfile = open(self.EMPFilename, 'w')

        self.EMPfile.write("ID,Name,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account\n")

        for emp in self.EMP_DICT:
            emp = self.EMP_DICT[emp]

            fullname = emp.f_name + " " + emp.l_name

            self.EMPfile.write(str(emp.emp_id) + "," + fullname + "," +  emp.address + "," + emp.city + "," + emp.state + "," + str(emp.zipcode) + "," + str(emp.Class) + "," + str(emp.paymethod) + "," + str(emp.salary) + "," + str(emp.hourly) + "," + str(emp.commission) + "," + emp.RoutingNumber + "," + emp.AccountNumber +'\n')
        
        self.EMPfile.close()
        
   
    def SaveUsers(self):
        """
            Saves all contents of the users dictionary to file
        """
        self.USERfile.close()
        self.USERfile = open(self.USERFilename, 'w')

        for user in self.USER_DICT:
            user = self.USER_DICT[user]

            self.USERfile.write(user.username + "," + user.password)

            for action in user.Permissions:
                self.USERfile.write("," + action)
            
            self.USERfile.write("\n")

    
    def DumpEmployees(self):
        """
            For debug purposes : prints all employees currently stored
        """
        print("DUMPING EMPLOYEES")
        for emp in self.EMP_DICT:
            self.EMP_DICT[emp].Dump()
    
    def VerifyEmployeeInformation(self, emp):
        if not str(emp.emp_id).isnumeric():
            return False
        if not str(emp.zipcode).isnumeric():
            return False
        try:
            emp.classification.asString()
        except:
            return False
        
        return True

    def DumpUsers(self):
        """
            For debug purposes : prints all user login information stored
        """
        print("DUMPING USERS")
        for user in self.USER_DICT:
            print(user)
            self.USER_DICT[user].Dump()

    def is_admin(self):
        if self.ActiveUser == None:
            return False
        return self.ActiveUser.Admin

def main():
        """
            This function is the Unit Testing for BackEnd. Should only be called when attempting to run BackEnd.py on its own.
            Goes through all the functions of the class and ensures the results are not only predictable, but correct
        """
        
        print()
        print("---------------Backend UnitTesting------------------")
        test = BackendImplementation("BackEnd/UnitTest/empTest.csv", "BackEnd/UnitTest/userTest.csv", "BackEnd/UnitTest/timeTest.csv", "BackEnd/UnitTest/receiptTest.csv", "BackEnd/UnitTest/Payroll.csv")
        print()
        
        try:
            """ Testing User Login Reading Correctness """
            print("--------Testing User Login Reading Correctness-------")
        
            assert len(test.USER_DICT) == 4, "User Dictionary is missing records! Check Read_LoginData!"
            assert "admin" in test.USER_DICT, "User Dictionary is missing records! Check Read_LoginData!"
            admin = test.USER_DICT['admin']
            assert admin.username == "admin", "User 1 was not read correctly!"
            assert admin.password == "password", "User 1 was not read correctly!"
            assert admin.Admin == True, "User 1 was not read correctly!"
            print("Login Reading Testing Passed.")
       

            print()
            """ Testing User Login Functionality"""
            print("--------Testing User Login Functionality--------")
        
            assert test.Login_User("dummy", "no") == False, "User : dummy, Password : no should have failed! Check Login_User" 
            assert test.Login_User("admin", "password") == True, "User : admin, Password : password should have passed! Check Login_User"
            print("Login Testing Passed.")
        
        
            print()
            """ Testing Employee File Reading Correctness"""
            print("---------Testing Employee File Reading Correctness--------")
        
            assert len(test.EMP_DICT) == 3, "Employee Dictionary is missing records! Check Read_EmployeeData!"
            emp = test.EMP_DICT[int(1)]
            assert emp.f_name == "Haley", "Employee 1 First Name was not read correctly! Check Read_EmployeeData!"
            assert emp.l_name == "Dickson", "Employee 1 Last Name was not read correctly! Check Read_EmployeeData!"
            assert emp.address == "652 W 1428 S", "Employee 1 Address was not read correctly! Check Read_EmployeeData!"
            assert emp.city == "Orem", "Employee 1 City was not read correctly! Check Read_EmployeeData!"
            assert emp.state == "UT", "Employee 1 State was not read correctly! Check Read_EmployeeData!"
            assert emp.zipcode == 84058, "Employee 1 State was not read correctly! Check Read_EmployeeData!"
            assert emp.classification.asString() == "Hourly", "Employee 1 Class was not read correctly! Check Read_EmployeeData!"
            assert emp.RoutingNumber == "WELLSFARGO5", "Employee 1 Class was not read correctly! Check Read_EmployeeData!"
            assert emp.AccountNumber == "4567890000", "Employee 1 Class was not read correctly! Check Read_EmployeeData!"
                
            print("Employee Reading Test Passed.")
      

            print()
            """ Testing Permissions and Employee Dictionary Actions """
            print("----------Testing Permissions and Employee Dictionary Actions---------")
       
            assert test.Login_User("admin", "password") == True, "Login failed! Check Login_User!"
            assert test.VerifyPermission("DELETE") == True, "Permission failed when it should have passed! Check VerifyPermission!"
            assert test.VerifyPermission("ADD") == True, "Permission failed when it should have passed! Check VerifyPermission!"
            assert test.VerifyPermission("EDIT") == True, "Permission failed when it should have passed! Check VerifyPermission!"
            assert test.AddEmployee(Employee(99, "Test", "Testingson", "Testing Lane 123", "Exam", "TS", 12345, "TESTROUTE9", "TESTBANK", 50.0, 50000, 5.0, 1, 1)) == True, "Failed to add an employee! Check VerifyPermissions!"
            assert (99 in test.EMP_DICT) == True, "Failed to add employee! Check AddEmployee!"
            assert len(test.EMP_DICT) == 4, "Failed to add employee! Check AddEmployee!"

            assert test.RemoveEmployee(99) == True, "Failed to delete employee! Check RemoveEmployee!"
            assert len(test.EMP_DICT) == 3, "Failed to delete employee! Check RemoveEmployee!"
            assert (not 99 in test.EMP_DICT) == True, "Failed to delete employee! Check RemoveEmployee!"

            assert test.UpdateEmployee(99, Employee()) == False, "Failed to delete employee! Check RemoveEmployee!"
            assert test.UpdateEmployee(1, Employee(99, "Test", "Testingson", "Testing Lane 123", "Exam", "TS", 12345, "TESTROUTE9", "TESTBANK", 50.0, 50000, 5.0, 1, 1)) == True, "Failed to Update an employee! Check UpdateEmployee!"
            emp = test.EMP_DICT[int(1)]
            assert emp.f_name == "Test", "Failed to Update an employee! Check UpdateEmployee!"

            print("Testing Permissions and Employee Actions Passed.")

            print()
            print("---------Testing Employee Change Permanence")
            test.Read_EmployeeData()
            OriginalList = test.getEmployeesAsList()

            test.AddEmployee(Employee(99, "Test", "Testingson", "Testing Lane 123", "Exam", "TS", 12345, "TESTROUTE9", "TESTBANK", 50.0, 50000, 5.0, 1, 1))

            test.SaveEmployees()
            test.Read_EmployeeData()

            assert len(test.EMP_DICT) == 4, "Failed to maintain Employee File changes! Check SaveEmployees!"
            assert (99 in test.EMP_DICT) == True, "Failed to maintain Employee File Changes! Check SaveEmployees!"
            
            test.RemoveEmployee(99)
            test.SaveEmployees()
            test.Read_EmployeeData()

            assert len(test.EMP_DICT) == 3, "Failed to maintain Employee File Changes! Check Save Employees!"
            assert (not 99 in test.EMP_DICT) == True, "Failed to maintain Employee File Changes! Check Save Employees!"

            print("Testing Employee Permanence Passed.")



        except AssertionError as error:
            print(error)
        
        print()
        print("All Testing Passed!")
        print()
        #try:
        #    assert(test.EMP_DICT["1"])
        
        
   
    

if __name__ == "__main__":
    main()