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
"""

from collections import *

from BackEnd import *

from empClass import *

from User import *




class BackendImplementation:
    def __init__(self):
        self.EMP_DATA = []
        self.EMP_DICT = OrderedDict({})
        self.EMPfile = 0
        self.EMPFilename = "employees.csv"

        self.USER_DICT = OrderedDict({})
        self.USERfile = 0
        self.USERFilename = "userlogin.csv"


        ActiveUser = None

        try:
            self.EMPfile = open(self.EMPFilename, 'r' )
            
        except:
            print("Error opening file.")

        try:
            self.USERfile = open(self.USERFilename, 'r' )
            
        except:
            try:
                self.USERfile = open("userlogin.csv", 'x')
                self.USERfile.write("admin,password,ADD,EDIT,DELETE")
            except:
                print("Login file was not found and could not be created.")

     
        self.Read_LoginData()
        self.Read_EmployeeData()
        

    def Read_LoginData(self):
        """
            Reads the userlogin.csv file and parses the information into User data structure array
        """
        lines = self.USERfile.readlines()

        for line in lines:
            words = line.split(',')

            words[len(words)-1] = words[len(words)-1].split('\n')[0]

            self.USER_DICT[words[0]] = User(words[0], words[1], words[2:])


    def Read_EmployeeData(self):
        """
        Reads the employee.csv file and parses the information into the empClass data structure array
        """ 
   

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

         

            emp = Employee(int(words[0]), fname, lname, words[2], words[3], words[4], int(words[5]), words[12], words[11], words[9], words[8], words[10], words[7], words[6])


            if int(words[6]) == 1:
                emp.make_hourly(float(words[9]))
            elif int(words[6] == 2):
                emp.make_salaried(int(words[8]))
            elif int(words[6] == 3):
                emp.make_commissioned(float(words[9], float(words[11])))
              

            self.EMP_DICT[int(words[0])] = emp

            
        return
    
    def IsUserValid(self, username):
        if username in self.USER_DICT:
            return True
        return False
        
    
    def VerifyLogin(self, username, password):
        if not self.IsUserValid(username):
            return False
            
        user = self.USER_DICT[username]
        
        if not password == user.password:
            return False
        
        return True
        

    def SetActiveUser(self, user):
        self.SetActiveUser = self.USER_DICT[user]


    def AddEmployee(self, emp):
        self.EMP_DICT[emp.emp_id] = emp

    
    def UpdateEmployee(self, empID, emp):
        emp = self.EMP_DICT.get(empID)

        if emp == None:
            return False
        
        self.EMP_DICT[empID] = emp
        return True
    
    def RemoveEmployee(self, empID):
        emp = self.EMP_DICT.get(empID)

        if emp == None:
            return False
        
        del self.EMP_DICT[empID]
        return True
    
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

    def DumpUsers(self):
        """
            For debug purposes : prints all user login information stored
        """
        print("DUMPING USERS")
        for user in self.USER_DICT:
            print(user)
            self.USER_DICT[user].Dump()

def main():
    test = BackendImplementation()
    test.DumpEmployees()
    test.DumpUsers()
    test.SaveEmployees()
    test.SaveUsers()
   
    

if __name__ == "__main__":
    main()