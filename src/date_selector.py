"""
todo
"""
from tkinter import Frame
from tkcalendar import Calendar



class DateSelector(Frame):
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
        self.frame.pack(fill="both", expand=True)

        #create calendar
        self.calendar = Calendar(self.frame, font="Arial 14", selectmode='day', locale='en_US',
               cursor="hand1", year=2018, month=2, day=5)
        self.calendar.pack(fill="both", expand=True)
