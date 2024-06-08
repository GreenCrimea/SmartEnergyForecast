from tkinter import *
from pandastable import Table, TableModel, config

class TableView(Frame):

    def __init__(self, parent):

        self.parent = parent
        Frame.__init__(self, self.parent)
        self.main = self.master
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=True)
        df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=df, showtoolbar=False, showstatusbar=True)
        pt.show()
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)
        pt.show()