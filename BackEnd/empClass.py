from abc import abstractmethod
'''This library is added to use inheritance without creating intitial data for the parent class'''
import os, os.path, shutil
'''These libraries are imported to help write information to files the correct way'''
PAY_LOGFILE = "paylog.txt"
employees = []
def load_employee():
    '''This function loads the employees information into a list'''
    with open("employees.csv", "r") as reader:
        reader.readline()
        while reader:
            emp = reader.readline().strip().split(",")
            if emp[0] == "":
                return
            new_emp = Employee(emp[0], emp[1], emp[2], emp[3], emp[4], emp[5], emp[6])
            if emp[7] == "3": #Hourly Employee
                new_emp.make_hourly(emp[10])
            elif emp[7] == "2": #Commissioned
                new_emp.make_commissioned(emp[8], emp[9])
            else: #Salaried Employee
                new_emp.make_salaried(emp[8])
            employees.append(new_emp)
def process_reciepts():
    '''This function processes receipts for employees who are commissioned'''
    with open("receipts.csv", "r") as r:
        while r:
            timeCard = r.readline().strip().split(",")
            emp = find_employee_id(timeCard[0])
            if emp is None:
                return
            if isinstance(emp.classification, Hourly):
                for hours in range(1, len(timeCard) - 1):
                    emp.classification.add_timecard(float(hours))
def process_timecards():
    '''This function processes the timecards of hourly employees'''
    with open("receipts.csv", "r") as r:
        while r:
            timeCard = r.readline().strip().split(",")
            emp = find_employee_id(timeCard[0])
            if emp is None:
                return
            if isinstance(emp.classification, Hourly):
                for hours in range(1, len(timeCard) - 1):
                    emp.classification.add_timecard(float(hours))
def find_employee_id(id):
    '''This function finds an employee using their id'''
    for emp in employees:
        if emp.emp_id == id:
            return emp
def run_payroll():
    '''this function '''
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
    for emp in employees:
        emp.issue_payment()
18
class Employee:
    def __init__(self, emp_id=None, f_name="First,", l_name="Last", address="", city="", state="", zipcode=00000, account=None, route=None, hourly=None, salary=None, commission=None, method=None, Class=None):
        self.emp_id = emp_id
        self.f_name = f_name
        self.l_name = l_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = None
        self.AccountNumber = account
        self.RoutingNumber  = route
        self.hourly = hourly
        self.salary = salary
        self.commission = commission
        self.paymethod = method
        self.Class = Class
    def make_hourly(self, rate):
        '''This function makes an employees classification hourly'''
        self.classification = Hourly(rate)
    def make_salaried(self, salary):
        '''This function makes an employees classification salaried'''
        self.classification = Salaried(salary)
    def make_commissioned(self, salary, percentage):
        '''This function makes an employees classification commissioned'''
        self.classification = Commissioned(salary, percentage)
    def issue_payment(self):
        '''This function writes the out the checks to employees to their address
            and also with the correct amount
        '''
        with open(PAY_LOGFILE, "a") as f:
            name = self.f_name + " " + " " + self.l_name
            addr = self.address
            city = self.city
            state = self.state
            zipcode = self.zipcode
            amount = self.classification.compute_pay()
            print("Mailing", " ", amount, "to", " ", name, "at", addr, city, state, zipcode, file=f)
    def Dump(self):
        '''This function is used to communicate with the front end'''
        print(self.f_name, self.l_name)
        print(self.address)
        print(self.city, self.zipcode)
        print(self.state)
        print(self.classification)
        print(self.AccountNumber)
        print(self.RoutingNumber)
        print()
class Classification:
    '''This class is used to define the way an empoloyee is payed'''
    def __init__(self):
        '''This initializes the classification class as an abstract method'''
        pass
    @abstractmethod
    def compute_pay(self):
        '''This function is passed on to the child class'''
        pass
class Hourly(Classification):
    '''This Classification is for Hourly employees'''
    def __init__(self, hourly_rate):
        '''This initializes the Hourly classification with the necessary 
            attributes.
        '''
        self.hourly_rate = hourly_rate
        self.timecard = []
    def add_timecard(self, card):
        '''This function adds a timecard to a list'''
        self.timecard.append(card)
    def compute_pay(self):
        '''This function computes the pay of an hourly employee'''
        total_hours_worked = 0
        total = 0
        for hours in self.timecard:
            total_hours_worked += hours
        self.timecard = []
        total += round(total_hours_worked * float(self.hourly_rate), 2)
        return total
class Salaried(Classification):
    '''This is the classification of a salaried employee'''
    def __init__(self, salary):
        '''This initializes the Salaried class with it's unique attributes'''
        self.salary = float(salary)
    def compute_pay(self):
        '''This function computes the pay for a salaried employee'''
        total = 0
        total += round(self.salary / 24, 2)
        return total
class Commissioned(Salaried):
    '''This is the Classification of an employee who is Commissioned'''
    def __init__(self, salary, percentage):
        '''This initializes the Commissioned class. It is the child of
            the Salary Class
        '''
        super().__init__(salary)
        self.receipt = []
        self.percentage = percentage
    def compute_pay(self):
        '''This funciton computes the pay of a commissioned employee
            by processing their receipts
        '''
        commissions = 0
        for commission in self.receipt:
            commissions += commission
        self.receipt = []
        total = 0
        total += round(super().compute_pay() * float(self.percentage)/100, 2)
        return total
    def add_receipt(self, receipt):
        '''This function adds a receipt to a list'''
        self.receipt.append(receipt)