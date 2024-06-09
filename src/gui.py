"""
gui Module

contains the gui object which is the parent of the tkinter instance
"""
from tkinter import Frame, Toplevel
from pandas import DataFrame
from src.table_view import TableView
from src.welcome_page import WelcomePage



class GUI(Frame):
    """
    Creates a tkinter window using TopLevel() which is the master
    parent for the tk instance. Can be instantiated with an optional
    parent.

        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent = None, geometry = "1000x600"):

        #initialize parent or top level window
        self.parent=parent
        if not self.parent:
            Frame.__init__(self)
            self.main=self.master
        else:
            self.main=Toplevel()
            self.master=self.main

        self.master.geometry(geometry)

        #initialize default main layout
        self.table = None
        self.create_table()

        #open welcome page
        self.welcome = None
        self.create_welcome_page()

    def create_table(self):
        """
        initialize a Tableview object in its empty state 
        """
        self.table = TableView(self.main)
        self.table.load_dataframe(DataFrame(0, index=[0], columns=[" "]))

    def create_welcome_page(self):
        """
        initialize a WelcomePage object
        """
        self.welcome = WelcomePage(self.main)
