from tkinter import * 



class GUI(Frame):

    def __init__(self, parent = None):

        self.parent=parent
        if not self.parent:
            Frame.__init__(self)
            self.main=self.master
        else:
            self.main=Toplevel()
            self.master=self.main

        self.welcome_page()

    def welcome_page(self):
        test_label = Label(self.main, text="TEST")
        test_label.pack(padx=100, pady=100)


