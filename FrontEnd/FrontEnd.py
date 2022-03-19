import imp
import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
from BackEnd import empClass
from BackEnd.empClass import Employee, Hourly, Salaried, Commissioned
import Interface.BasicController
import copy
import random
import sys
import os
import platform

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if 'Darwin' in platform.system():
    folder_path = resource_path("FrontEnd/Assets_mac/")
else:
    folder_path = resource_path("FrontEnd\\Assets\\")


logo_large_path = folder_path+"logo_large.PNG"
logo_small_path = folder_path+"logo_small.PNG"
search_icon_path = folder_path+"search_icon.PNG"
login_button_path = folder_path+"login_button.PNG"
payroll_button_path = folder_path+"payroll_button.PNG"
user_guide_button_path = folder_path+"user_guide_button.PNG"
corner_image_path = folder_path+"corner.PNG"
add_button_path = folder_path+"add_button.PNG"
delete_button_path = folder_path+"delete_button.PNG"
bg_color  = "white"
bg_color2 = "#D7D8D9"
skyblue = "#3bc3f1"
title_font = ("Arial Rounded MT Bold", 14)
button_font = ("Arial Rounded MT Bold", 30)
basic_font = ("Arial", 14)


class Window:
    """
    This class handles all the frames, tabs, and popups related to the program, as well as interfacing with the backend
    """
    def __init__(self):
        """
        Initial setup of all the necessary frames for the GUI
        """
        self.colors = [
            skyblue,
            'purple',
            'red',
            'orange',
            'green'
        ]
        self.Controller = Interface.BasicController.BasicControlller()
        # This section creates the basic window with a light gray background
        self.root = tk.Tk() ## Create the root window
        self.root.protocol("WM_DELETE_WINDOW", self.exit)   #Calls self.exit() when the root window is closed
        self.root.bind_all('<F4>', self.change_colors)
        self.root.resizable(width=False, height=False)
        self.width = 1000   ## Define the root window's dimensions
        self.height = 600
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height,
                                                int(self.root.winfo_screenwidth()/2 - self.width/2),
                                                int(self.root.winfo_screenheight()/2 - self.height/2)))
        self.root.configure(bg=bg_color2)   ## Define colors
        self.root.title("EmpDat")           ## This is the title of the window which will show on the top bar
        self.icon_image_large = tk.PhotoImage(file=logo_large_path)     ## Give the window a program icon
        self.icon_image_small = tk.PhotoImage(file=logo_small_path)
        self.root.iconphoto(False, self.icon_image_small)
        self.root.wm_minsize(self.width, self.height)       ## Limit the window so that it cannot be made smaller than its original size
        self.color_index = 0
        self.last_selected = -1
        self.confirm_result = False
        
        # This section creates the white frame that goes on top of the light gray background
        self.main_frame = tk.Frame(self.root, bg=bg_color)  ## Create the main frame on the root
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)    ## Expand to fill the window, leaving a border
        self.main_frame.pack_propagate(0)   ## tell frame not to let its children control its size
        
        # Create the login screen
        self.login_screen = TwoColumnFrame(self.main_frame)     ## Create the login screen from a two column frame class
        self.login_frame = tk.Frame(self.login_screen.left_frame, bg=bg_color)  ## Create the left frame on the login screen frame
        self.login_frame.pack()
        self.login_frame.place(relx=0.5, rely=0.5, anchor='c')  ## Center the login frame on the left column
        self.username = tk.StringVar()
        self.username_label = tk.Label(self.login_frame, text="Username", bg=bg_color, font=title_font, fg='black')     ## Create the username label and button
        self.username_label.pack()
        self.username_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font, textvariable=self.username, fg='black')
        self.username_field.pack()
        self.password = tk.StringVar()
        self.password_label = tk.Label(self.login_frame, text="Password", bg=bg_color, font=title_font, fg='black')     ## Create the password label and button
        self.password_label.pack()
        self.password_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font, show="*", textvariable=self.password, fg='black')
        self.password_field.pack()
        self.password_field.bind("<Return>", self.login)
        self.login_pic = ImageTk.PhotoImage(Image.open(logo_large_path).resize((350, 350)))     ## Load in the logo image
        self.login_pic_container = tk.Label(self.login_screen.right_frame, image=self.login_pic, bd=0, bg=skyblue)     ## Create a logo container on the right frame of the two column frame
        self.login_button_pic = ImageTk.PhotoImage(Image.open(login_button_path).resize((225, 40)))         ## Create the login button from image resource
        self.login_button = tk.Button(self.login_frame, image=self.login_button_pic, bg=skyblue, activebackground=bg_color, bd=0, command=self.login, width=223, height=38)
        self.login_button.pack(pady=10)
        self.login_button.pack_propagate(0)
        self.login_pic_container.pack()
        self.login_pic_container.place(relx=0.5, rely=0.5, anchor='c')  ## Center the logo in the right frame

        ## Add rounded corners to login screen
        if not isMAC():
            self.base_corner_image = Image.open(corner_image_path).resize((35, 35))     ### Load in the base corner image

            self.corner1_image = ImageTk.PhotoImage(self.base_corner_image)
            self.corner1_container = tk.Label(self.login_screen.left_frame, image=self.corner1_image, bg=bg_color, bd=0)    ### Place corner1
            self.corner1_container.pack(side="top", anchor="nw")

            self.corner2_image = ImageTk.PhotoImage(self.base_corner_image.rotate(90))
            self.corner2_container = tk.Label(self.login_screen.left_frame, image=self.corner2_image, bg=bg_color, bd=0)    ### Rotate and place corner2
            self.corner2_container.pack(side="bottom", anchor="sw")

            self.corner3_image = ImageTk.PhotoImage(self.base_corner_image.rotate(270))
            self.corner3_container = tk.Label(self.login_screen.right_frame, image=self.corner3_image, bg=bg_color, bd=0)   ### Rotate and place corner3
            self.corner3_container.pack(side="top", anchor="ne")

            self.corner4_image = ImageTk.PhotoImage(self.base_corner_image.rotate(180))
            self.corner4_container = tk.Label(self.login_screen.right_frame, image=self.corner4_image, bg=bg_color, bd=0)   ### Rotate and place corner4
            self.corner4_container.pack(side="bottom", anchor="se")
        
        # Create the workflow screen
        self.work_screen = TabFrame(self.main_frame, 2) # Create x tabs in the tabs frame

        ## Create elements in tab 1, this will be the open tab upon logging in
        self.work_screen.tabs[0].tab_button.configure(text = "Records")
        self.work_screen.tabs[0].body_frame = tk.Frame(self.work_screen.body_frame, bg=bg_color)    ### Configure the Records tab name and attributes
        self.work_screen.tabs[0].body_frame.pack(expand=True, fill="both")
        self.payroll_button_image = ImageTk.PhotoImage(Image.open(payroll_button_path).resize((740, 185)))
        self.payroll_button = tk.Button(self.work_screen.tabs[0].body_frame, image=self.payroll_button_image,   ### Create a button for payroll from image
                                        bg=skyblue, bd=0, foreground=bg_color, activebackground=bg_color, width=738, height=183,
                                        command=lambda: Notice(self.root, "Under Development.", self.colors[self.color_index]))
        self.payroll_button.pack(padx=100, pady=(50, 10))
        self.payroll_button.pack_propagate(0)
        self.user_guide_button_image = ImageTk.PhotoImage(Image.open(user_guide_button_path).resize((740, 185)))
        self.user_guide_button = tk.Button(self.work_screen.tabs[0].body_frame, image=self.user_guide_button_image, ### Create a button for user guide from image
                                        bg=skyblue, bd=0, foreground=bg_color, activebackground=bg_color, width=738, height=183,
                                        command=lambda: Notice(self.root, "Under Development.", self.colors[self.color_index]))
        self.user_guide_button.pack(padx=100, pady=(10, 55))
        self.user_guide_button.pack_propagate(0)

        if not isMAC():
            self.corner5_image = ImageTk.PhotoImage(self.base_corner_image.rotate(90))
            self.corner5_container = tk.Label(self.work_screen.tabs[0].body_frame, image=self.corner5_image, bg=bg_color, bd=0) ### Add rounded corners to the body frame
            self.corner5_container.pack(side="left")

            self.corner6_image = ImageTk.PhotoImage(self.base_corner_image.rotate(180))
            self.corner6_container = tk.Label(self.work_screen.tabs[0].body_frame, image=self.corner6_image, bg=bg_color, bd=0)
            self.corner6_container.pack(side="right")

        self.work_screen.tabs[0].show_body()    ### Show the tab 1 body
        
        ## Create elements in tab 2
        self.work_screen.tabs[1].tab_button.configure(text = "Employees")                   ### Configure the Employees tab name and attributes
        self.work_screen.tabs[1].body_frame = TwoColumnFrame(self.work_screen.body_frame)   ### Create the employees page out of a two column frame 
        self.work_screen.tabs[1].hide_body()    ### Hide the employees tab because the default tab is the first tab
        
        ### Tab 2 Left
        self.listbox_frame = tk.Frame(self.work_screen.tabs[1].body_frame.left_frame, bg=bg_color2) #### Create a listbox frame on the left frame of the employees tab
        self.listbox_frame.pack(fill="both", expand=True, padx=(25,0), pady=(25,25))
        self.listbox_frame.pack_propagate(0)
        self.emp_search_field = tk.Entry(self.listbox_frame, bd=0, bg=bg_color, font=basic_font, fg='black')    #### Create a search field and attach it to the listbox
        self.emp_search_field.bind("<KeyRelease>", self.search_keyrelease) # Create event listenter for the search field
        self.emp_search_field.pack(side='top', fill='both', padx=10, pady=(10,0))
        self.search_pic = ImageTk.PhotoImage(Image.open(search_icon_path).resize((25, 25)))
        self.search_pic_container = tk.Label(self.emp_search_field, image=self.search_pic, bd=0)    #### Add a search icon to the search field
        self.search_pic_container.pack(side='right', fill='both')
        self.emp_box = tk.Listbox(self.listbox_frame, bd=0, bg=bg_color2, activestyle='none', font=basic_font, fg='black', 
                                    selectbackground=skyblue, highlightcolor=bg_color2, highlightbackground=bg_color2,  #### Create a employee listbox and attach it to the listbox frame
                                    highlightthickness=10, selectforeground='black')
        self.emp_box_scroller = tk.Scrollbar(self.emp_box, command=self.emp_box.yview)      #### Create a scroll bar and attach it to the employee listbox
        self.emp_box.config(yscrollcommand = self.emp_box_scroller.set)     #### Configure the scroll bar settings
        self.emp_box_scroller.pack(side='right', fill='both')
        self.emp_box.bind("<<ListboxSelect>>", self.listbox_select) # Create event listener for when an item in the listbox is selected
        self.emp_box.pack(fill="both", expand=True)
        self.emp_box.pack_propagate(0)
        self.manage_emp_frame = tk.Frame(self.work_screen.tabs[1].body_frame.left_frame, bg=bg_color, height=50)    #### Create a new frame for add, edit, and delete buttons
        self.manage_emp_frame.pack(side='left', expand=True, fill='both', padx=(25,0), pady=(0,25))
        self.manage_emp_frame.pack_propagate(0)
        self.add_button_image = ImageTk.PhotoImage(Image.open(add_button_path).resize((225, 50)))
        self.emp_add_btn = tk.Button(self.manage_emp_frame, bg=skyblue, foreground=bg_color, image=self.add_button_image, width=223, height=48,
                                        font=title_font, bd=0, command=self.add)  #### Create Add button on employee management frame
        self.emp_add_btn.pack(side='left', padx=0)
        self.emp_add_btn.pack_propagate(0)
        self.delete_button_image = ImageTk.PhotoImage(Image.open(delete_button_path).resize((225, 50)))
        self.emp_delete_btn = tk.Button(self.manage_emp_frame, bg=skyblue, foreground=bg_color, image=self.delete_button_image, width=223, height=48,
                                            font=title_font, bd=0, command=self.delete)  #### Create Delete button on employee management frame
        self.emp_delete_btn.pack(side='right')
        self.emp_delete_btn.pack_propagate(0)
        self.full_list = self.request_employees()        #### Populate the listbox with the full list of employee initially
        self.visible_list = self.request_employees()     #### Show the current requested employees
        self.update_search_listbox()        #### Update the search box based on the entered information

        ### Tab 2 Right
        self.indent_amount = 50
        self.entry_length = 35
        self.emp_pic = ImageTk.PhotoImage(Image.open(logo_large_path).resize((100, 100)))       #### This should later call the backend to provide the employee's photo
        self.emp_pic_container = tk.Label(self.work_screen.tabs[1].body_frame.right_frame,      #### Put the employee photo in a container on the right side of the employees tab
                                          image=self.emp_pic, borderwidth=2, relief="groove", bg=skyblue)
        self.emp_pic_container.pack(side="top", pady=25)

        self.work_screen.tabs[1].body_frame.right_frame.configure(bd=self.indent_amount)

        self.emp_name = tk.StringVar()
        self.emp_name_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_name_label_container.pack(pady=5, fill="x")
        self.emp_name_label = tk.Label(self.emp_name_label_container, font=basic_font,    #### Add a field for the employee's name
                                       bg=bg_color2, text="Employee:", fg='black')
        self.emp_name_label.pack(side="left")
        self.emp_name_entry = tk.Entry(self.emp_name_label_container, font=basic_font, bg=bg_color, textvariable=self.emp_name, width=self.entry_length, fg='black')
        self.emp_name_entry.pack(side="left", fill="x")
        self.emp_name_entry.bind("<Return>", self.update_working_employee)

        self.last_selected_emp_info = ""
        self.emp_payment = tk.StringVar()
        self.emp_payment_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_payment_label_container.pack(pady=5, fill="x")
        self.emp_payment_label = tk.Label(self.emp_payment_label_container, font=basic_font,  #### Add a field for the employee's payment type
                                         bg=bg_color2, text="Payment type:", fg='black')
        self.emp_payment_label.pack(side="left")
        self.payment_types = ["Hourly", "Salaried", "Commissioned"]
        self.emp_payment_type_optionlist = tk.OptionMenu(self.emp_payment_label_container, self.emp_payment, *self.payment_types)
        self.emp_payment_type_optionlist.pack(side="left", fill="x")
        self.emp_payment_type_optionlist.bind("<Return>", self.update_working_employee)

        self.emp_salary = tk.StringVar()
        self.emp_salary_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_salary_label_container.pack(pady=5, fill="x")
        self.emp_salary_label = tk.Label(self.emp_salary_label_container, font=basic_font,  #### Add a field for the employee's pay amount
                                         bg=bg_color2, text="Amount:", fg='black')
        self.emp_salary_label.pack(side="left")
        self.emp_salary_entry = tk.Entry(self.emp_salary_label_container, font=basic_font, bg=bg_color, textvariable=self.emp_salary, width=self.entry_length, fg='black')
        self.emp_salary_entry.pack(side="left", fill="x")
        self.emp_salary_entry.bind("<Return>", self.update_working_employee)

        self.emp_address = tk.StringVar()
        self.emp_address_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_address_label_container.pack(pady=5, fill="x")
        self.emp_address_label = tk.Label(self.emp_address_label_container, font=basic_font,  #### Add a field for the employee's address
                                         bg=bg_color2, text="Address:", fg='black')
        self.emp_address_label.pack(side="left")
        self.emp_address_entry = tk.Entry(self.emp_address_label_container, font=basic_font, bg=bg_color, textvariable=self.emp_address, width=self.entry_length, fg='black')
        self.emp_address_entry.pack(side="left", fill="x")
        self.emp_address_entry.bind("<Return>", self.update_working_employee)
        
        #Set the show/hide for each screen for the intial view when the application is launched
        #self.login_screen.hide()
        #self.work_screen.show()
        self.login_screen.show()
        self.work_screen.hide()

        #Hide various widgets based on user permissions
        #if not self.Controller.isAdmin(user):
        #self.manage_emp_frame.pack_forget()

    
    def add(self):
        """
        Add a new employee to the database
        """
        blank = empClass.Employee() # Create a new employee
        id_list = []
        new_id = None
        for employee in self.Controller.request_employees():
            id_list.append(employee.emp_id)
        while (new_id := random.randrange(100000, 999999)) in id_list: pass
        blank.emp_id = new_id   # Assign the blank employee an ID that is not already taken
        self.Controller.add_employee(blank) # Add the employee
        self.full_list = self.request_employees()   # Update the visible list of employees
        self.visible_list = self.request_employees()
        self.emp_search_field.delete(0, tk.END)
        self.update_search_listbox()

    def delete(self):
        """
        Delete the currently selected employee from the database
        """
        self.Controller.remove_employee(self.current_working_employee.emp_id) # Remove the currently selected employee from the database
        self.full_list = self.request_employees()
        self.visible_list = self.request_employees()    # Update the visible list of employees
        self.emp_search_field.delete(0, tk.END)
        self.update_search_listbox() 

    def run(self):
        """
        Begins the program by running the main loop
        """
        self.root.mainloop()    # Run the tk mainloop
        
    def exit(self):
        """
        Ends the program
        """
        self.Controller.on_exit()   # Let the controller know the GUI is about to be closed, save anything necessary
        self.root.destroy()      # When the user closes the program destroy the root window
    
    def login(self, event=None):
        """
        Verifies the user's login credentials. If the credentials are incorrect, show a warning notice. Otherwise, login the user.
        """
        if self.Controller.VerifyLogin(self.username.get(), self.password.get()):  # If the user enters correct credentials
            self.login_screen.hide()    # Hide the login page
            self.work_screen.show()     # Show the work screen
        else:
            popup = Notice(self.root, "Incorrect username or password.", self.colors[self.color_index])     # Otherwise, tell the user they have entered the wrong credentials
    
    def search_keyrelease(self, event):
        """
        Updates the displayed employee list in the employee tab based on the current information entered in the search box.
        """
        search_string = event.widget.get()  # Get the current contents of the search box
        self.visible_list = []      # Create an empty array that will be populated with employees that match the search
        for i in self.full_list:
            if search_string.lower()[:len(search_string)] == i.lower()[:len(search_string)]:
                self.visible_list.append(i)     # If an employee is found that matches the search, add it to the array
        self.update_search_listbox()    # Update the search listbox with the list of found employee matching the search
    
    def listbox_select(self, event):
        """
        Updates the employee information on the right tab when an employee is selected in the left tab
        """
        selection = event.widget.curselection()     # When the user clicks on an employee
        index = selection[0]
        data = event.widget.get(index)
        name = data.split()
        self.current_working_employee = next(employee for employee in self.Controller.request_employees() if ((employee.f_name == name[0]) and (employee.l_name == name[1])))
        if selection:

            if index != self.last_selected:   # If a different employee is being selected

                #if self.Controller.isAdmin(user):
                selected_emp_info = self.get_emp_entry_info()
                if self.last_selected_emp_info != selected_emp_info and self.last_selected != -1:   # If changes were made in the entry fields
                    self.confirm_result = False
                    Confirmation(self.root, self, "Save changes to this employee?", self.colors[self.color_index])   # Confirm changes
                    if self.confirm_result:
                        #self.Controller.update_employee(selected_emp_info)
                        pass

                self.emp_name_entry.delete(0, last="end")
                self.emp_name_entry.insert(0, data)         # Update the employee information on the right tab

                #self.emp_payment_entry.delete(0, tk.END)
                self.emp_classification = self.current_working_employee.classification
                if isinstance(self.emp_classification, Hourly): self.emp_classification = "Hourly"
                elif isinstance(self.emp_classification, Salaried): self.emp_classification = "Salaried"
                elif isinstance(self.emp_classification, Commissioned): self.emp_classification = "Commissioned"
                else: self.emp_classification = "Unknown"
                self.emp_payment.set(self.emp_classification)
                #self.emp_payment_entry.insert(0, self.emp_classification)

                self.emp_salary_entry.delete(0, tk.END)
                self.emp_pay_amount = ""
                if (self.emp_classification == "Hourly"): self.emp_pay_amount = self.current_working_employee.hourly
                elif (self.emp_classification == "Salaried"): self.emp_pay_amount = self.current_working_employee.salary
                elif (self.emp_classification == "Commissioned"): self.emp_pay_amount = self.current_working_employee.commission
                else: self.emp_pay_amount = "Unknown"
                self.emp_salary_entry.insert(0, self.emp_pay_amount)

                self.emp_address_entry.delete(0, tk.END)
                self.emp_address_string = self.current_working_employee.address
                self.emp_address_entry.insert(0, self.emp_address_string)
                self.last_selected_emp_info = self.get_emp_entry_info()
                self.last_selected = self.emp_box.curselection()[0]

        else:
            self.emp_name_label.configure(text="")

    def get_emp_entry_info(self):
        """
        Return all the information in the right side entry fields as a string
        """
        string = ""
        string += self.emp_name_entry.get() + ","
        string += self.emp_payment.get() + ","
        string += self.emp_salary_entry.get() + ","
        string += self.emp_address_entry.get()
        return string
    
    def update_search_listbox(self):
        """
        Updates the listbox to show only employess who are in the visible list
        """
        self.emp_box.delete(0,'end') # Remove all items in the employee listbox
        for i in self.visible_list:  # With the update list of employees that should be available in the listbox,
            self.emp_box.insert(0, i) # Insert employee name into listbox
            self.emp_box.itemconfig(0, {'bg':'white'}) # Edit background color

    def request_employees(self):
        """
        Gets a list of all the names of the employees in the database
        """ 
        emplist = self.Controller.request_employees()   # Request the employee list from the backend
        names = []
        for employee in emplist:
            names.append(employee.f_name+" "+employee.l_name)   # Get all the names from the employee list
        return names

    def update_working_employee(self, event):
        """
        Updates the currently selected employee with new data once the enter key is pressed
        """
        new_name = self.emp_name.get().split()  # Get all the new data from tk entries
        new_payment_type = self.emp_payment.get().lower()
        new_payment_amount = self.emp_salary.get()
        if not (new_payment_amount.isnumeric() or isfloat(new_payment_amount)):
            Notice(self.root, "Payment amount must be a number", self.colors[self.color_index])
            return
        new_address = self.emp_address.get()

        empID = self.current_working_employee.emp_id
        new_employee = copy.copy(self.current_working_employee) # Create a copy of the current working employee
        new_employee.f_name = new_name[0]
        new_employee.l_name = new_name[1]
        new_employee.address = new_address
        if new_payment_type == "hourly": new_payment_type = Hourly(new_payment_amount); new_employee.hourly = new_payment_amount    # Format data and add to copy
        elif new_payment_type == "salaried": new_payment_type = Salaried(new_payment_amount); new_employee.salary = new_payment_amount
        elif new_payment_type == "commisioned": new_payment_type = Commissioned(new_payment_amount, 100); new_employee.commission = new_payment_amount
        else: new_payment_type = None
        new_employee.classification = new_payment_type
        
        self.Controller.update_employee(empID, new_employee)    # Update the employee in the database
        self.full_list = self.request_employees()
        self.visible_list = self.request_employees()    # Update the list of employees on the frontend
        self.emp_search_field.delete(0, tk.END)
        self.update_search_listbox()

    def change_colors(self, event):
        
        colored_image_containers = [
            self.login_pic_container,
            self.login_button,
            self.payroll_button,
            self.user_guide_button,
            self.emp_add_btn,
            self.emp_delete_btn,
            self.emp_pic_container
        ]
        self.color_index = (self.color_index + 1) % len(self.colors)
        for container in colored_image_containers:
            container.configure(bg=self.colors[self.color_index])
        self.emp_box.configure(selectbackground=self.colors[self.color_index])
        

class Widget(ABC):
    """
    This Abstract Class acts as a custom object that can be placed into a tkinter window
    """
    @abstractmethod
    def show(self):
        """
        Enforces a show method on child classes, which will show this window object
        """
        pass
    
    @abstractmethod
    def hide(self):
        """
        Enforces a hide method on child classes, which will hide this window object
        """
        pass


class TwoColumnFrame(Widget):
    """
    This class holds two frames, one on the left, one on the right
    """
    def __init__(self, frame):
        """
        Initialize the left and right frames of the two column frame
        """
        self.left_frame = tk.Frame(frame, bg=bg_color)  # Create the left frame
        self.right_frame = tk.Frame(frame, bg=bg_color) # Create the right frame
        self.show()     # Show the created frames
        
    def show(self):
        """
        Show the two column frame in the window
        """
        self.left_frame.pack(side="left", fill="both", expand=True)     # Left frame fills the left side of the window
        self.left_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="both", expand=True)   # Right frame fills the right side of the window
        self.right_frame.pack_propagate(0)
        
    def hide(self):
        """
        Hide the two column frame in the window
        """
        self.left_frame.pack_forget()   # Disable both frames
        self.right_frame.pack_forget()


class TabFrame(Widget):
    """
    This class holds the frames for the records and employees tabs
    """
    def __init__(self, frame, tab_count):
        """
        Initialize the tab frame
        """
        self.tabs_frame = tk.Frame(frame, bg=bg_color, height=50)   # Create a tab frame
        self.body_frame = tk.Frame(frame, bg=bg_color)  # Create a body frame to go with the tab
        self.tabs = []
        for i in range(tab_count):  # Add enough tabs for all the possible tabs
            self.add_tab()
        self.show()     # Show the created tab
    
    def show(self):
        """
        Shows the tab frame
        """
        self.tabs_frame.pack(side='top', fill='both')   # Enable the tab and the tab body
        self.tabs_frame.pack_propagate(0)
        self.body_frame.pack(side='left', fill='both', expand=True)
        self.body_frame.pack_propagate(0)
        
    def hide(self):
        """
        Hides the tab frame
        """
        self.tabs_frame.pack_forget()   # Disable tab and tab body
        self.body_frame.pack_forget()
            
    def add_tab(self):
        """
        Add an additional tab to the list of available tabs
        """
        tab = Tab(self)         # Create a new tab
        self.tabs.append(tab)   # Add the new tab to the list of tabs
        
    def focus_tab(self, clicked_tab):
        """
        Method for showing only the currently selected tab
        """
        for tab in self.tabs:
            tab.hide_body()         # First, hide all the tabs
        clicked_tab.show_body()     # Then, show only the tab that was clicked


class Tab(Widget):
    """
    This class creates and controls the tab widget
    """
    
    def __init__(self, frame):
        """
        Initialize the tab
        """
        self.body_frame = None # This will later be filled with a reference to a frame object
        self.tab_frame = tk.Frame(frame.tabs_frame, bg=bg_color) # A frame to hold the tab button

        if not isMAC():
            self.corner_left_image = ImageTk.PhotoImage(Image.open(corner_image_path).resize((35, 35)))
            self.corner_left_container = tk.Label(self.tab_frame, image=self.corner_left_image, bg=bg_color, bd=0)
            self.corner_left_container.pack(side="left", anchor="nw")

            self.corner_right_image = ImageTk.PhotoImage(Image.open(corner_image_path).resize((35, 35)).rotate(270))
            self.corner_right_container = tk.Label(self.tab_frame, image=self.corner_right_image, bg=bg_color, bd=0)
            self.corner_right_container.pack(side="right", anchor="ne")

        self.tab_button = tk.Button(self.tab_frame, text="Tab", bg=bg_color2, font=title_font, bd=0, activebackground=bg_color2,
                                    command=lambda: frame.focus_tab(self))
        self.tab_button.pack(fill="both", expand=True)
        self.show()
        
    def show(self):
        """
        Show the tab in the parent tabs frame
        """
        self.tab_frame.pack(side="left", fill="both", expand=True)  # Enable the tab
        self.tab_frame.pack_propagate(0)
    
    def hide(self):
        """
        Hide the tab in the parent tabs frame
        """
        self.tab_frame.pack_forget()    # Disable the tab
        
    def show_body(self):
        """
        Show the body frame that is attached to this tab
        """
        self.tab_button.pack_forget()   # Disable the tab button
        if not isMAC():
            self.corner_left_container.pack(side="left", anchor="nw")   # Add in the rounded corners
            self.corner_right_container.pack(side="right", anchor="ne")
        self.tab_button.pack(fill="both", expand=True)  # Re-enable the tab button
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack(fill="both", expand=True)
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.show()
        self.tab_button.configure(bg=bg_color, activebackground=bg_color)

            
    def hide_body(self):
        """
        Hide the body frame that is attached to this tab
        """
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack_forget()
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.hide()
        self.tab_button.configure(bg=bg_color2) # Hide the tab button
        if not isMAC():
            self.corner_left_container.pack_forget()    # Hide the rounded corners
            self.corner_right_container.pack_forget()
        self.tab_button.configure(bg=bg_color2, activebackground=bg_color2)


class Popup(tk.Toplevel):
    """
    This class creates and controls popup messages in the program
    """
    def __init__(self, master, message):
        """
        Initialize and display the popup
        """
        self.master = master
        tk.Toplevel.__init__(self, master)
        self.transient(master)   # Set the popup to be on top of the main window
        self.grab_set()   # Ignore clicks in the main window while the popup is open
        self.protocol("WM_DELETE_WINDOW", self.close)   # Call self.close when the exit button is clicked
        self.width = 350   # Set popup dimensions and show in the center of the screen
        self.height = 100
        self.geometry("{}x{}+{}+{}".format(self.width, self.height,
                                            int(master.winfo_screenwidth()/2 - self.width/2),
                                            int(master.winfo_screenheight()/2 - self.height/2)))
        self.resizable(width=False, height=False) # Disable resizing
        self.configure(bg=bg_color2) # Set visiual appearance of the popup
        self.title("EmpDat")
        self.icon_image = tk.PhotoImage(file = logo_small_path)
        self.iconphoto(False, self.icon_image)
        
        self.main_frame = tk.Frame(self, bg=bg_color) # A frame where the window context is shown
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.main_frame.pack_propagate(0)
        
        self.message_label = tk.Label(self.main_frame, text=message, bg=bg_color, font=basic_font, fg='black') # Display a message
        self.message_label.pack(side="top", pady=(5, 0))
        self.message_label.pack_propagate(0)
    
    def wait(self):
        """
        Pause main window until the popup is
        """
        self.master.wait_window(self)
    
    def close(self):
        """
        Close the popup
        """
        self.destroy()


class Notice(Popup):
    """
    This class creates a notice popup with a mesage and acknowledgement button
    """
    def __init__(self, master, message, color):
        """
        Initialize and show the notice popup
        """
        super().__init__(master, message)
        self.okay_button = tk.Button(self.main_frame, text="Okay", bg=color, bd=0,
                                    foreground=bg_color, font=basic_font, command=self.close, fg='black') # A button to close the notice
        self.okay_button.pack(side="bottom", pady=5)
        self.wait()


class Confirmation(Popup):
    """
    This class creates a confirmation popup with two option, yes or no
    """
    def __init__(self, master, the_window, message, color):
        """
        Initialize and show the confirmation popup
        """
        super().__init__(master, message)
        self.the_window = the_window
        self.yes_button = tk.Button(self.main_frame, text="Yes", bg=color, bd=0,
                                    foreground=bg_color, font=basic_font, command=self.yes, fg='black') # A button to confirm the action
        self.yes_button.pack(side="left", padx=(90, 5), pady=5)
        self.no_button = tk.Button(self.main_frame, text="No", bg=color, bd=0,
                                    foreground=bg_color, font=basic_font, command=self.no, fg='black') # A button to decline the action
        self.no_button.pack(side="right", padx=(5, 90), pady=5)
        self.wait()

    def yes(self):
        """
        Commands to execute if the confirmation is positive
        """
        self.the_window.confirm_result = True
        self.close()    # Close the popup
    
    def no(self):
        """
        Commands to execute if the confirmation is negative
        """
        self.the_window.confirm_result = False
        self.close()    # Close the popup

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def isMAC():
    if 'Darwin' in platform.system():
        return True
    return False