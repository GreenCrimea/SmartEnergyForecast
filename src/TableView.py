from tkinter import *
from pandastable import Table, TableModel, config

class TableView(Frame):

    def __init__(self, parent):

        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry("1000x400")
        self.main.title("test table")
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=df, showtoolbar=False, showstatusbar=True)
        pt.show()
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)
        pt.show()