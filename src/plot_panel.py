"""
todo
"""
from tkinter import Frame



class PlotPanel(Frame):
    """
    todo
    """

    def __init__(self, parent):

        #initialize superclass
        self.parent = parent
        Frame.__init__(self, self.parent)
        self.main = self.master

        #create frame
        self.frame = Frame(self.main)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.pack_propagate(False)