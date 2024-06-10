"""
table_view Module

contains the TableView object for rendering a table to a tkinter instance
"""

from tkinter import Frame
from warnings import filterwarnings
from pandastable import Table



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
        self.column_selected = None

    def load_dataframe(self, dataframe):
        """
        load a dataframe into the table

            Arguments:
                dataframe (DataFrame) = dataframe to be displayed
        """     
        self.df = dataframe
        self.df.replace("Calm", 0)
        self.table = Table(self.frame, dataframe=self.df, showtoolbar=False, showstatusbar=True)
        self.table.font= self.gui.font[0]
        self.table.fontsize = int(self.gui.font[1])
        self.table.bind("<ButtonRelease-1>", self.on_selected)
        self.table.setFont()
        self.table.show()
        self.table.redraw()

    def on_selected(self, event):
        """
        todo
        """
        if self.table.getSelectedRow() != self.row_selected:
            self.row_selected = self.table.getSelectedRow()
            self.gui.date_selector.move_to_date(self.row_selected)
        if self.table.getSelectedColumn() != self.column_selected:
            column_selected = self.table.getSelectedColumn()

        if self.gui.settings_panel.selecting_column != False:
            column_selected = self.df.columns[column_selected]
            if column_selected not in self.gui.settings_panel.get_ydata_input(self.gui.settings_panel.selecting_column):
                self.gui.settings_panel.insert_ydata_input(self.gui.settings_panel.selecting_column, column_selected)


    def move_table(self, row, col):
        """
        todo
        """
        self.table.movetoSelection(row=row, col=col)
        self.table.redraw()

    def set_inactive_rows(self):
        """
        todo
        """
        if self.gui.date_selector.inactive_date_indexes is not None:
            self.table.delete()
            df = self.gui.dataframe.copy(True)
            df = df.drop(self.gui.date_selector.inactive_date_indexes)
            self.load_dataframe(df)