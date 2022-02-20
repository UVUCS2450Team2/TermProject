import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

logo_path = "FrontEnd\logo.PNG"
bg_color  = "white"
bg_color2 = "lightgray"
skyblue = "#3bc3f1"
title_font = ("Arial", 14, "bold")
basic_font = ("Arial", 14)


class Window:
    
    def __init__(self):
        self.root = tk.Tk()
        self.width = 1000
        self.height = 600
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height,
                                                int(self.root.winfo_screenwidth()/2 - self.width/2),
                                                int(self.root.winfo_screenheight()/2 - self.height/2)))
        self.root.configure(bg=bg_color2)
        self.root.title("EmpDat")
        self.icon_image = tk.PhotoImage(file = logo_path)
        self.root.iconphoto(False, self.icon_image)
        
        self.main_frame = tk.Frame(self.root, bg=bg_color)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.main_frame.pack_propagate(0)
        
        #Create the login screen
        self.login_screen = TwoColumnFrame(self.main_frame)
        self.login_frame = tk.Frame(self.login_screen.left_frame, bg=bg_color)
        self.login_frame.pack()
        self.login_frame.place(relx=0.5, rely=0.5, anchor='c')
        self.username_label = tk.Label(self.login_frame, text="Username", bg=bg_color, font=title_font)
        self.username_label.pack()
        self.username_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font)
        self.username_field.pack()
        self.password_label = tk.Label(self.login_frame, text="Password", bg=bg_color, font=title_font)
        self.password_label.pack()
        self.password_field = tk.Entry(self.login_frame, bd=0, bg=bg_color2, font=basic_font, show="*")
        self.password_field.pack()
        self.login_pic = ImageTk.PhotoImage(Image.open(logo_path).resize((350, 350)))
        self.login_pic_container = tk.Label(self.login_screen.right_frame, image=self.login_pic, bd=0)
        self.login_button = tk.Button(self.login_frame, text="Login", bg=skyblue, bd=0,
                                      foreground=bg_color, font=title_font, command=self.login)
        self.login_button.pack(pady=10, expand=True, fill="both")
        self.login_pic_container.pack()
        self.login_pic_container.place(relx=0.5, rely=0.5, anchor='c')
        self.login_screen.show()
        
        #Create the workflow screen
        self.work_screen = TabFrame(self.main_frame, 2)
        
        ##Create elements in tab 1
        self.work_screen.tabs[0].tab_button.configure(text = "Records")
        self.work_screen.tabs[0].body_frame = tk.Frame(self.work_screen.body_frame, bg=bg_color)
        self.work_screen.tabs[0].body_frame.pack(expand=True, fill="both")
        self.payroll_button = tk.Button(self.work_screen.tabs[0].body_frame, text="View My Payroll",
                                        bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.payroll_button.pack(padx=100, pady=(50, 10), expand=True, fill="both")
        self.user_guide_button = tk.Button(self.work_screen.tabs[0].body_frame, text="User Guide",
                                        bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.user_guide_button.pack(padx=100, pady=(10, 50), expand=True, fill="both")
        
        ##Create elements in tab 2
        self.work_screen.tabs[1].tab_button.configure(text = "Employees")
        self.work_screen.tabs[1].body_frame = TwoColumnFrame(self.work_screen.body_frame)
        self.work_screen.tabs[1].hide_body()
        
        ###Left
        self.emp_box = tk.Listbox(self.work_screen.tabs[1].body_frame.left_frame, bd=0, bg=bg_color2)
        self.emp_box.pack(fill="both", expand=True)
        self.emp_box.pack_propagate(0)
        self.emp_search_field = tk.Entry(self.emp_box, bd=0, bg=bg_color, font=basic_font)
        self.emp_search_field.pack(side='top', fill='both', padx=10, pady=10)

        ###Right
        self.emp_pic = ImageTk.PhotoImage(Image.open(logo_path).resize((100, 100)))
        self.emp_pic_container = tk.Label(self.work_screen.tabs[1].body_frame.right_frame,
                                          image=self.emp_pic, borderwidth=2, relief="groove")
        self.emp_pic_container.pack(side="top", pady=25)
        self.emp_name_label = tk.Label(self.work_screen.tabs[1].body_frame.right_frame, font=basic_font,
                                       bg=bg_color, text="Employee: Alex")
        self.emp_name_label.pack(pady=5)
        self.emp_salary_label = tk.Label(self.work_screen.tabs[1].body_frame.right_frame, font=basic_font,
                                         bg=bg_color, text="Salary: $0")
        self.emp_salary_label.pack(pady=5)
        
        self.work_screen.hide()
        
    def run(self):
        self.root.mainloop()
        
    def exit(self):
        self.destroy()
        
    def create_popup(self, message):
        popup = Notice(self, message)
        
    def login(self):
        self.login_screen.hide()
        self.work_screen.show()


class Widget(ABC):
    
    @abstractmethod
    def show(self):
        pass
    
    @abstractmethod
    def hide(self):
        pass


class TwoColumnFrame(Widget):
    
    def __init__(self, frame):
        self.left_frame = tk.Frame(frame, bg=bg_color)
        self.right_frame = tk.Frame(frame, bg=bg_color)
        self.show()
        
    def show(self):
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(0)
        
    def hide(self):
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()


class TabFrame(Widget):
    
    def __init__(self, frame, tab_count):
        self.tabs_frame = tk.Frame(frame, bg=bg_color, height=50)
        self.body_frame = tk.Frame(frame, bg=bg_color)
        self.tabs = []
        for i in range(tab_count):
            self.add_tab()
        self.show()
    
    def show(self):
        self.tabs_frame.pack(side='top', fill='both')
        self.tabs_frame.pack_propagate(0)
        self.body_frame.pack(side='left', fill='both', expand=True)
        self.body_frame.pack_propagate(0)
        
    def hide(self):
        self.tabs_frame.pack_forget()
        self.body_frame.pack_forget()
            
    def add_tab(self):
        tab = Tab(self)
        self.tabs.append(tab)
        
    def focus_tab(self, clicked_tab):
        for tab in self.tabs:
            tab.hide_body()
        clicked_tab.show_body()


class Tab(Widget):
    
    def __init__(self, frame):
        self.parent = frame
        self.body_frame = None
        self.tab_frame = tk.Frame(frame.tabs_frame, bg=bg_color)
        self.tab_button = tk.Button(self.tab_frame, text="Tab", bg=bg_color, font=title_font, bd=0,
                                    command=lambda: self.parent.focus_tab(self))
        self.tab_button.pack(fill="both", expand=True)
        self.show()
        
    def show(self):
        self.tab_frame.pack(side="left", fill="both", expand=True)
        self.tab_frame.pack_propagate(0)
    
    def hide(self):
        self.tab_frame.pack_forget()
        
    def show_body(self):
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack(fill="both", expand=True)
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.show()
            
    def hide_body(self):
        if isinstance(self.body_frame, tk.Frame):
            self.body_frame.pack_forget()
        elif isinstance(self.body_frame, TwoColumnFrame):
            self.body_frame.hide()


class Popup:
    
    def __init__(self, master, message):
        self.master = master
        self.popup = tk.Toplevel(master.root)
        self.popup.width = 300
        self.popup.height = 100
        self.popup.geometry("{}x{}+{}+{}".format(self.popup.width, self.popup.height,
                                                int(self.master.root.winfo_screenwidth()/2 - self.popup.width/2),
                                                int(self.master.root.winfo_screenheight()/2 - self.popup.height/2)))
        self.popup.configure(bg=bg_color2)
        self.popup.title("EmpDat")
        self.popup.icon_image = tk.PhotoImage(file = logo_path)
        self.popup.iconphoto(False, self.popup.icon_image)
        
        self.popup.main_frame = tk.Frame(self.popup, bg=bg_color)
        self.popup.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.popup.main_frame.pack_propagate(0)
        
        self.popup.message_label = tk.Label(self.popup.main_frame, text=message, bg=bg_color, font=basic_font)
        self.popup.message_label.pack(side="top", pady=(5, 0))
        
    def close(self):
        self.popup.destroy()


class Notice(Popup):
    
    def __init__(self, master, message):
        super().__init__(master, message)
        self.popup.okay_button = tk.Button(self.popup.main_frame, text="Okay", bg=skyblue, bd=0,
                                      foreground=bg_color, font=basic_font, command=self.close)
        self.popup.okay_button.pack(side="bottom", pady=5)


class Confirmation(Popup):
    
    def __init__(self, master, message):
        super().__init__(master, message)
        self.popup.yes_button = tk.Button(self.popup.main_frame, text="Yes",
                                          bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.popup.yes_button.pack(side="left", padx=(90, 5), pady=5)
        self.popup.no_button = tk.Button(self.popup.main_frame, text="No",
                                         bg=skyblue, bd=0, foreground=bg_color, font=basic_font)
        self.popup.no_button.pack(side="right", padx=(5, 90), pady=5)

    def yes(self):
        self.close()
    
    def no(self):
        self.close()


window = Window()
window.run()

