from ctypes import WinDLL
import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

folder_path = "FrontEnd\\Assets\\"
logo_large_path = folder_path+"logo_large.PNG"
logo_small_path = folder_path+"logo_small.PNG"
search_icon_path = folder_path+"search_icon.PNG"
login_button_path = folder_path+"login_button.PNG"
payroll_button_path = folder_path+"payroll_button.PNG"
user_guide_button_path = folder_path+"user_guide_button.PNG"
corner_image_path = folder_path+"corner.PNG"
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
        # This section creates the basic window with a light gray background
        self.root = tk.Tk() ## Create the root window
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
        
        # This section creates the white frame that goes on top of the light gray background
        self.main_frame = tk.Frame(self.root, bg=bg_color)  ## Create the main frame on the root
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)    ## Expand to fill the window, leaving a border
        self.main_frame.pack_propagate(0)   ## Enable showing the frame
        
        # Create the login screen
        self.login_screen = TwoColumnFrame(self.main_frame)     ## Create the login screen from a two column frame class
        self.login_frame = tk.Frame(self.login_screen.left_frame, bg=bg_color)  ## Create the left frame on the login screen frame
        self.login_frame.pack()
        self.login_frame.place(relx=0.5, rely=0.5, anchor='c')  ## Center the login frame on the left column
        self.username_label = tk.Label(self.login_frame, text="Username", bg=bg_color, font=title_font)     ## Create the username label and button
        self.username_label.pack()
        self.username_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font)
        self.username_field.pack()
        self.password_label = tk.Label(self.login_frame, text="Password", bg=bg_color, font=title_font)     ## Create the password label and button
        self.password_label.pack()
        self.password_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font, show="*")
        self.password_field.pack()
        self.login_pic = ImageTk.PhotoImage(Image.open(logo_large_path).resize((350, 350)))     ## Load in the logo image
        self.login_pic_container = tk.Label(self.login_screen.right_frame, image=self.login_pic, bd=0, bg=bg_color)     ## Create a logo container on the right frame of the two column frame
        self.login_button_pic = ImageTk.PhotoImage(Image.open(login_button_path).resize((225, 40)))         ## Create the login button from image resource
        self.login_button = tk.Button(self.login_frame, image=self.login_button_pic, bg=bg_color, activebackground=bg_color, bd=0, command=self.login)
        self.login_button.pack(pady=10, expand=True, fill="both")
        self.login_pic_container.pack()
        self.login_pic_container.place(relx=0.5, rely=0.5, anchor='c')  ## Center the logo in the right frame

        ## Add rounded corners to login screen
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

        self.login_screen.show()    ## show the login screen frame
        
        # Create the workflow screen
        self.work_screen = TabFrame(self.main_frame, 2)
        
        ## Create elements in tab 1, this will be the open tab upon logging in
        self.work_screen.tabs[0].tab_button.configure(text = "Records")
        self.work_screen.tabs[0].body_frame = tk.Frame(self.work_screen.body_frame, bg=bg_color)    ### Configure the Records tab name and attributes
        self.work_screen.tabs[0].body_frame.pack(expand=True, fill="both")
        self.payroll_button_image = ImageTk.PhotoImage(Image.open(payroll_button_path).resize((740, 185)))
        self.payroll_button = tk.Button(self.work_screen.tabs[0].body_frame, image=self.payroll_button_image,   ### Create a button for payroll from image
                                        bg=bg_color, bd=0, foreground=bg_color, activebackground=bg_color,
                                        command=lambda: Notice(self, "Under Development."))
        self.payroll_button.pack(padx=100, pady=(50, 10), expand=True, fill="both")
        self.user_guide_button_image = ImageTk.PhotoImage(Image.open(user_guide_button_path).resize((740, 185)))
        self.user_guide_button = tk.Button(self.work_screen.tabs[0].body_frame, image=self.user_guide_button_image, ### Create a button for user guide from image
                                        bg=bg_color, bd=0, foreground=bg_color, activebackground=bg_color, 
                                        command=lambda: Notice(self, "Under Development."))
        self.user_guide_button.pack(padx=100, pady=(10, 50), expand=True, fill="both")

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
        self.listbox_frame.pack(fill="both", expand=True, padx=(25,0), pady=(25,10))
        self.listbox_frame.pack_propagate(0)
        self.emp_search_field = tk.Entry(self.listbox_frame, bd=0, bg=bg_color, font=basic_font)    #### Create a search feild and attach it to the listbox
        self.emp_search_field.bind("<KeyRelease>", self.search_keyrelease)
        self.emp_search_field.pack(side='top', fill='both', padx=10, pady=(10,0))
        self.search_pic = ImageTk.PhotoImage(Image.open(search_icon_path).resize((25, 25)))
        self.search_pic_container = tk.Label(self.emp_search_field, image=self.search_pic, bd=0)    #### Add a search icon to the search field
        self.search_pic_container.pack(side='right', fill='both')
        self.emp_box = tk.Listbox(self.listbox_frame, bd=0, bg=bg_color2, activestyle='none', font=basic_font, 
                                    selectbackground=skyblue, highlightcolor=bg_color2, highlightbackground=bg_color2,  #### Create a employee listbox and attach it to the listbox frame
                                    highlightthickness=10, selectforeground='black')
        self.emp_box_scroller = tk.Scrollbar(self.emp_box, command=self.emp_box.yview)      #### Create a scroll bar and attach it to the employee listbox
        self.emp_box.config(yscrollcommand = self.emp_box_scroller.set)     #### Configure the scroll bar settings
        self.emp_box_scroller.pack(side='right', fill='both')
        self.emp_box.bind("<<ListboxSelect>>", self.listbox_select)
        self.emp_box.pack(fill="both", expand=True)
        self.emp_box.pack_propagate(0)
        self.manage_emp_frame = tk.Frame(self.work_screen.tabs[1].body_frame.left_frame, bg=bg_color, height=50)    #### Create a new frame for add, edit, and delete buttons
        self.manage_emp_frame.pack(side='left', expand=True, fill='both', padx=(25,0), pady=(0,25))
        self.manage_emp_frame.pack_propagate(0)
        self.emp_add_btn = tk.Button(self.manage_emp_frame, bg=skyblue, foreground=bg_color, text="  Add ",
                                        font=title_font, bd=0, command=lambda: Notice(self, "Under Development."))  #### Create Add button on employee management frame
        self.emp_add_btn.pack(side='left', expand=True, fill='both')
        self.emp_edit_btn = tk.Button(self.manage_emp_frame, bg=skyblue, foreground=bg_color, text=" Edit ",
                                        font=title_font, bd=0, command=lambda: Notice(self, "Under Development."))  #### Create Edit button on employee management frame
        self.emp_edit_btn.pack(side='left', expand=True, fill='both', padx=10)
        self.emp_delete_btn = tk.Button(self.manage_emp_frame, bg=skyblue, foreground=bg_color, text="Delete",
                                            font=title_font, bd=0, command=lambda: Notice(self, "Under Development."))  #### Create Delete button on employee management frame
        self.emp_delete_btn.pack(side='left', expand=True, fill='both')
        self.full_list = request_employees()        #### Populate the listbox with the full list of employee initially
        self.visible_list = request_employees()     #### Show the current requested employees
        self.update_search_listbox()        #### Update the search box based on the entered information

        ### Tab 2 Right
        self.indent_amount = 50
        self.entry_length = 35
        self.emp_pic = ImageTk.PhotoImage(Image.open(logo_large_path).resize((100, 100)))       #### This should later call the backend to provide the employee's photo
        self.emp_pic_container = tk.Label(self.work_screen.tabs[1].body_frame.right_frame,      #### Put the employee photo in a container on the right side of the employees tab
                                          image=self.emp_pic, borderwidth=2, relief="groove")
        self.emp_pic_container.pack(side="top", pady=25)

        self.work_screen.tabs[1].body_frame.right_frame.configure(bd=self.indent_amount)

        self.emp_name = ""
        self.emp_name_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_name_label_container.pack(pady=5, fill="x")
        self.emp_name_label = tk.Label(self.emp_name_label_container, font=basic_font,    #### Add a feild for the employee's name
                                       bg=bg_color2, text="Employee:")
        self.emp_name_label.pack(side="left")
        self.emp_name_entry = tk.Entry(self.emp_name_label_container, font=basic_font, bg=bg_color, textvariable=self.emp_name, width=self.entry_length)
        self.emp_name_entry.pack(side="left", fill="x")

        self.emp_salary_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_salary_label_container.pack(pady=5, fill="x")
        self.emp_salary_label = tk.Label(self.emp_salary_label_container, font=basic_font,  #### Add a feild for the employee's payment type
                                         bg=bg_color2, text="Payment type:")
        self.emp_salary_label.pack(side="left")

        self.emp_payment_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_payment_label_container.pack(pady=5, fill="x")
        self.emp_payment_label = tk.Label(self.emp_payment_label_container, font=basic_font,  #### Add a feild for the employee's pay amount
                                         bg=bg_color2, text="Amount: $0")
        self.emp_payment_label.pack(side="left")

        self.emp_address_label_container = tk.Frame(self.work_screen.tabs[1].body_frame.right_frame, bg=bg_color2)
        self.emp_address_label_container.pack(pady=5, fill="x")
        self.emp_address_label = tk.Label(self.emp_address_label_container, font=basic_font,  #### Add a feild for the employee's address
                                         bg=bg_color2, text="Address:")
        self.emp_address_label.pack(side="left")
        
        self.work_screen.hide()     #### Hide the tab since it is not the first tab
        
    def run(self):
        """
        Begins the program by running the main loop
        """
        self.root.mainloop()    # Run the tk mainloop
        
    def exit(self):
        """
        Ends the program
        """
        self.destroy()      # When the user closes the program destroy the root window
    
    def login(self):
        """
        Verifies the user's login credentials. If the credentials are incorrect, show a warning notice. Otherwise, login the user.
        """
        if verify_login(self.username_field.get(), self.password_field.get()):  # If the user enters correct credentials
            self.login_screen.hide()    # Hide the login page
            self.work_screen.show()     # Show the work screen
        else:
            popup = Notice(self, "Incorrect username or password.")     # Otherwise, tell the user they have entered the wrong credentials
    
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
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.emp_name_entry.delete(0, last="end")
            self.emp_name_entry.insert(0, data)         # Update the employee information on the right tab   
        else:
            self.emp_name_label.configure(text="")

    def update_search_listbox(self):
        """
        Unknown
        """
        self.emp_box.delete(0,'end')
        for i in self.visible_list:
            self.emp_box.insert(0, i)
            self.emp_box.itemconfig(0, {'bg':'white'})


class Widget(ABC):
    """
    Uknown
    """
    @abstractmethod
    def show(self):
        """
        Unknown
        """
        pass
    
    @abstractmethod
    def hide(self):
        """
        Unknown
        """
        pass


class TwoColumnFrame(Widget):
    """
    This class holds the frames for the records and employees tabs
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
        self.left_frame.pack_propagate(0)                               # Enable the left frame
        self.right_frame.pack(side="right", fill="both", expand=True)   # Right frame fills the right side of the window
        self.right_frame.pack_propagate(0)                              # Enable the right frame
        
    def hide(self):
        """
        Hide the two column frame in the window
        """
        self.left_frame.pack_forget()   # Disable both frames
        self.right_frame.pack_forget()


class TabFrame(Widget):
    
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
        self.parent = frame
        self.body_frame = None
        self.tab_frame = tk.Frame(frame.tabs_frame, bg=bg_color)

        self.corner_left_image = ImageTk.PhotoImage(Image.open(corner_image_path).resize((35, 35)))
        self.corner_left_container = tk.Label(self.tab_frame, image=self.corner_left_image, bg=bg_color, bd=0)
        self.corner_left_container.pack(side="left", anchor="nw")

        self.corner_right_image = ImageTk.PhotoImage(Image.open(corner_image_path).resize((35, 35)).rotate(270))
        self.corner_right_container = tk.Label(self.tab_frame, image=self.corner_right_image, bg=bg_color, bd=0)
        self.corner_right_container.pack(side="right", anchor="ne")

        self.tab_button = tk.Button(self.tab_frame, text="Tab", bg=bg_color2, font=title_font, bd=0, activebackground=bg_color2,
                                    command=lambda: self.parent.focus_tab(self))
        self.tab_button.pack(fill="both", expand=True)
        self.show()
        
    def show(self):
        """
        Show the tab
        """
        self.tab_frame.pack(side="left", fill="both", expand=True)
        self.tab_frame.pack_propagate(0)
    
    def hide(self):
        """
        Hide the tab
        """
        self.tab_frame.pack_forget()
        
    def show_body(self):
        """
        A better way to show the tab that puts everything back where it was
        """
        self.tab_button.pack_forget()
        self.corner_left_container.pack(side="left", anchor="nw")
        self.corner_right_container.pack(side="right", anchor="ne")
        self.tab_button.pack(fill="both", expand=True)
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack(fill="both", expand=True)
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.show()
        self.tab_button.configure(bg=bg_color, activebackground=bg_color)

            
    def hide_body(self):
        """
        A better way to hide the tab
        """
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack_forget()
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.hide()
        self.tab_button.configure(bg=bg_color2)
        self.corner_left_container.pack_forget()
        self.corner_right_container.pack_forget()
        self.tab_button.configure(bg=bg_color2, activebackground=bg_color2)


class Popup:
    """
    This class creates and controls popup messages in the program
    """
    def __init__(self, master, message):
        """
        Initialize and display the popup
        """
        self.master = master
        self.popup = tk.Toplevel(master.root)
        self.popup.width = 350
        self.popup.height = 100
        self.popup.geometry("{}x{}+{}+{}".format(self.popup.width, self.popup.height,
                                                int(self.master.root.winfo_screenwidth()/2 - self.popup.width/2),
                                                int(self.master.root.winfo_screenheight()/2 - self.popup.height/2)))
        self.popup.resizable(width=False, height=False)
        self.popup.configure(bg=bg_color2)
        self.popup.title("EmpDat")
        self.popup.icon_image = tk.PhotoImage(file = logo_small_path)
        self.popup.iconphoto(False, self.popup.icon_image)
        
        self.popup.main_frame = tk.Frame(self.popup, bg=bg_color)
        self.popup.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.popup.main_frame.pack_propagate(0)
        
        self.popup.message_label = tk.Label(self.popup.main_frame, text=message, bg=bg_color, font=basic_font)
        self.popup.message_label.pack(side="top", pady=(5, 0))
        self.popup.message_label.pack_propagate(0)
        
    def close(self):
        """
        Close the popup
        """
        self.popup.destroy()


class Notice(Popup):
    """
    This class creates a notice popup with a mesage and acknowledgement button
    """
    def __init__(self, master, message):
        """
        Initialize and show the notice popup
        """
        super().__init__(master, message)
        self.popup.okay_button = tk.Button(self.popup.main_frame, text="Okay", bg=skyblue, bd=0,
                                      foreground=bg_color, font=basic_font, command=self.close)
        self.popup.okay_button.pack(side="bottom", pady=5)


class Confirmation(Popup):
    """
    This class creates a confirmation popup with two option, yes or no
    """
    def __init__(self, master, message):
        """
        Initialize and show the confirmation popup
        """
        super().__init__(master, message)
        self.popup.yes_button = tk.Button(self.popup.main_frame, text="Yes",
                                          bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.popup.yes_button.pack(side="left", padx=(90, 5), pady=5)
        self.popup.no_button = tk.Button(self.popup.main_frame, text="No",
                                         bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.popup.no_button.pack(side="right", padx=(5, 90), pady=5)

    def yes(self):
        """
        Commands to execute if the confirmation is positive
        """
        self.close()
    
    def no(self):
        """
        Commands to execute if the confirmation is negative
        """
        self.close()

#####CONTROLLER#####
# This section should be imported from the interface.py
def verify_login(username, password):
    return True

def request_employees() : 
    return sorted(["Alex", "Elliot", "Shayne", "Michael", "Kaleb", "Sam"] *5, reverse=True)

def get_employee(ID) :
    return 100

def export_payroll() :
    return

def update_employee(ID, data) : 
    return True

def remove_employee(ID) :
    return True

def verify_permission(user, action) :
    return True