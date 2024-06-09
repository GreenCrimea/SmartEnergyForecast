"""
table_view Module

contains the TableView object for rendering a table to a tkinter instance
"""

from tkinter import Frame
from warnings import filterwarnings
from pandastable import Table#, TableModel



class TableView(Frame):
    """
    Display a canvas containing a table corresponding to a pandas dataframe.
    inherits from the tkinter frame object and calls an instance of the
    pandastable Table
        
        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent, gui):

        #initialize superclass
        self.parent = parent
        Frame.__init__(self, self.parent)
        self.main = self.master
        self.gui = gui

        #ignore FutureWarning
        filterwarnings("ignore", category=FutureWarning)

        #create frame
        self.frame = Frame(self.main)
        self.frame.pack(side="bottom", fill="both", expand=True)

        self.row_selected = None

    def load_dataframe(self, dataframe):
        """
        load a dataframe into the table

            Arguments:
                dataframe (DataFrame) = dataframe to be displayed
        """
        #sample data
        #self.df = TableModel.getSampleData()       
        self.df = dataframe
        self.df.replace("Calm", 0)
        self.table = Table(self.frame, dataframe=self.df, showtoolbar=False, showstatusbar=True)
        self.table.font= self.gui.font[0]
        self.table.fontsize = int(self.gui.font[1])
        self.table.bind("<ButtonRelease-1>", self.on_selected)
        self.table.setFont()
        self.table.show()

    def on_selected(self, event):
        """
        todo
        """
        if self.table.getSelectedRow() != self.row_selected:
            self.row_selected = self.table.getSelectedRow()
            self.gui.date_selector.move_to_date(self.row_selected)

    def move_table(self, row, col):
        """
        todo
        """
        self.gui.table_view.table.movetoSelection(row=row, col=col)
        self.gui.table_view.table.redraw()