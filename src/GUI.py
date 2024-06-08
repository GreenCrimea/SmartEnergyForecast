from tkinter import * 
from src.TableView import TableView



class GUI(Frame):

    def __init__(self, parent = None):

        self.parent=parent
        if not self.parent:
            Frame.__init__(self)
            self.main=self.master
        else:
            self.main=Toplevel()
            self.master=self.main

        self.master.geometry("1000x600")

        self.welcome_page()

        pt = TableView(self.main)

    def welcome_page(self):
        test_label = Label(self.main, text="TEST")
        test_label.pack(side=LEFT, padx=50)


