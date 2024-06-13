"""
welcome_page Module

contains the WelcomePage object rendered when beginning the program
"""
from tkinter import Toplevel



class WelcomePage():
    """
    Display a Toplevel window containing the initial startup options
    to be rendered infront of the gui when beginning the program
        
        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent):

        #initialize tk toplevel
        self.parent = parent
        self.main = Toplevel(self.parent)

        #ensure window stays on top and main window is inactive
        self.main.transient(self.parent)
        self.main.grab_set()
        self.parent.wait_window(self.main)