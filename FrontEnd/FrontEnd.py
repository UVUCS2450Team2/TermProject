from tkinter import *

class Window:
    """
    Insert description here
    """
    def __init__(self):
        """
        Insert description here
        """
        self.root = Tk
        self.main_frame = Frame
        self.login_screen = TwoColumnFrame
        self.work_screen = TabFrame

    def run(self):
        """
        Insert description here
        """
        return

    def exit(self):
        """
        Insert description here
        """
        return

class Tab(Widget):
    """
    Insert description here
    """
    def __init__(self):
        """
        Insert description here
        """
        self.tab_frame = Frame
        self.title = Label
        self.body_frame = Frame

    def show(self):
        """
        Insert description here
        """
        return

    def hide(self):
        """
        Insert description here
        """
        return

class TwoColumnFrame(Widget):
    """
    Insert description here
    """
    def __init__(self):
        self.left_frame = Frame
        self.Right_frame = Frame

    def show(self):
        """
        Insert description here
        """
        return
    
    def hide(self):
        """
        Insert description here
        """
        return

class TabFrame(Widget):
    """
    Insert description here
    """
    def __init__(self):
        """
        Insert description here
        """
        self.tabs_frame = Frame
        self.body_frame = Frame
        self.tabs = []
        self.active_tab = True

    def show(self):
        """
        Insert description here
        """
        return

    def hide(self):
        """
        Insert description here
        """
        return

    def focus_tab(tab: Tab):
        """
        Insert description here
        """
        return

