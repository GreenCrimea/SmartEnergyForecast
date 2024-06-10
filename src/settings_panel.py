"""
todo
"""
from tkinter import Frame, Label, Entry, Button, messagebox
from PIL import ImageTk, Image
from src.tooltip import CreateToolTip



class SettingsPanel(Frame):
    """
    todo
    """

    def __init__(self, parent, gui):

        #initialize superclass
        self.parent = parent
        Frame.__init__(self, self.parent)
        self.main = self.master
        self.gui = gui

        #create frame
        self.frame = Frame(self.main)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.pack_propagate(False)

        self.initialize_date_range()

    def initialize_date_range(self):
        """
        todo
        """
        self.calendar_icon = Image.open("assets/calendar.png")
        self.calendar_icon = ImageTk.PhotoImage(self.calendar_icon)

        #date to
        self.date_to = Frame(self.frame, height=24)
        self.date_to.pack(side="bottom", fill="x", expand=False)
        self.date_to.pack_propagate(False)

        self.date_to_label_frame = Frame(self.date_to, width=100)
        self.date_to_label_frame.pack(side="left", fill="y", expand=False)
        self.date_to_label_frame.pack_propagate(False)

        self.date_to_label = Label(self.date_to_label_frame, text="Date to:", 
                                   font=(self.gui.font[0], int(self.gui.font[1])))
        self.date_to_label.pack(side="left")

        self.date_to_date = Entry(self.date_to, justify="center",
                                  font=(self.gui.font[0], int(self.gui.font[1])))
        self.date_to_date.pack(side="left")

        self.date_to_button = Button(self.date_to, image=self.calendar_icon,
                                       command=self.select_date_to)
        self.date_to_button.pack(side="right", padx=3)
        CreateToolTip(self.date_to_button, text="Use calendar to select ending date")

        self.date_to_confirm = Button(self.date_to, text="Ok", command=self.apply_date_to)
        self.date_to_confirm.pack(side="right")
        CreateToolTip(self.date_to_confirm, text="Apply ending date input")


        #date from
        self.date_from = Frame(self.frame, height=28)
        self.date_from.pack(side="bottom", fill="x", expand=False)
        self.date_from.pack_propagate(False)

        self.date_from_label_frame = Frame(self.date_from, width=100)
        self.date_from_label_frame.pack(side="left", fill="y", expand=False)
        self.date_from_label_frame.pack_propagate(False)

        self.date_from_label = Label(self.date_from_label_frame, text="Date from:", 
                                     font=(self.gui.font[0], int(self.gui.font[1])))
        self.date_from_label.pack(side="left")

        self.date_from_date = Entry(self.date_from, justify="center", 
                                    font=(self.gui.font[0], int(self.gui.font[1])))
        self.date_from_date.pack(side="left")

        self.date_from_button = Button(self.date_from, image=self.calendar_icon,
                                       command=self.select_date_from)
        self.date_from_button.pack(side="right", padx=3)
        CreateToolTip(self.date_from_button, text="Use calendar to select starting date")

        self.date_from_confirm = Button(self.date_from, text="Ok", command=self.apply_date_from)
        self.date_from_confirm.pack(side="right")
        CreateToolTip(self.date_from_confirm, text="Apply starting date input")

        self.update_date_fromto()

    def apply_date_from(self):
        """
        todo
        """
        input = self.date_from_date.get()
        if input in self.gui.date_selector.dates_str:
            self.gui.date_selector.selection = input
            self.set_date_from()

    def apply_date_to(self):
        """
        todo
        """
        input = self.date_to_date.get()
        if input in self.gui.date_selector.dates_str:
            self.gui.date_selector.selection = input
            self.set_date_to()

    def update_date_fromto(self):
        """
        todo
        """
        range = self.gui.date_selector.active_range
        self.date_from_date.delete(0,len(self.date_from_date.get()) + 1)
        self.date_from_date.insert(0,range[0])
        self.date_to_date.delete(0,len(self.date_from_date.get()) + 1)
        self.date_to_date.insert(0,range[1])

    def select_date_from(self):
        """
        todo
        """
        messagebox.showinfo("Info", "Use the calendar to select new start for the data's range")
        self.gui.date_selector.getting_selection = True
        self.gui.date_selector.selection_callback = self.set_date_from

    def set_date_from(self):
        """
        todo
        """
        date_from_selection = self.gui.date_selector.selection
        self.gui.date_selector.selection = None
        self.gui.date_selector.selection_callback = None
        self.gui.date_selector.change_active_range(date_from=date_from_selection, s="F")
        self.update_date_fromto()


    def select_date_to(self):
        """
        todo
        """
        messagebox.showinfo("Info", "Use the calendar to select new end for the data's range")
        self.gui.date_selector.getting_selection = True
        self.gui.date_selector.selection_callback = self.set_date_to

    def set_date_to(self):
        """
        todo
        """
        date_to_selection = self.gui.date_selector.selection
        self.gui.date_selector.selection = None
        self.gui.date_selector.selection_callback = None
        self.gui.date_selector.change_active_range(date_to=date_to_selection, s="T")
        self.update_date_fromto()
