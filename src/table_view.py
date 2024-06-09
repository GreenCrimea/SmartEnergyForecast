"""
table_view Module

contains the TableView object for rendering a table to a tkinter instance
"""

from tkinter import Frame
from pandastable import Table, TableModel

class TableView(Frame):
    """
    Display a canvas containing a table corresponding to a pandas dataframe.
    inherits from the tkinter frame object and calls an instance of the
    pandastable Table
        
        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent):

        #initialize superclass
        self.parent = parent
        Frame.__init__(self, self.parent)
        self.main = self.master

        #create frame
        self.frame = Frame(self.main)
        self.frame.pack(fill="both", expand=True)

        self.df = None
        self.table = None

    def load_dataframe(self, dataframe):
        """
        load a dataframe into the table

            Arguments:
                dataframe (DataFrame) = dataframe to be displayed
        """
        #sample data
        #self.df = TableModel.getSampleData()
        
        self.df = dataframe
        self.table = Table(self.frame, dataframe=self.df, showtoolbar=False, showstatusbar=True)
        self.table.show()
