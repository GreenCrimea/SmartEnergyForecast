"""
todo
"""
from datetime import date
from tkinter import Frame, messagebox
from tkcalendar import Calendar




class DateSelector(Frame):
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
        self.frame.pack(side="bottom", fill="both", expand=True)
        self.frame.pack_propagate(False)

        start_date = gui.dataframe["Date"].iloc[0]
        start_date = start_date.split("-")

        #create calendar
        self.calendar = Calendar(self.frame, font=self.gui.font, selectmode='day', locale='en_US',
               cursor="hand1", year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2]),
               date_pattern="y-mm-d")
        self.calendar.pack(fill="both", expand=True)
        self.get_date_types()
        self.highlight_days()
        self.calendar.bind("<<CalendarSelected>>", self.on_selected)

    def get_date_types(self):
        """
        todo
        """
        self.dates = []
        self.dates_str = []
        for dates in self.gui.dataframe["Date"]:
            self.dates_str.append(dates)
            dates = [int(dates) for dates in dates.split("-")]
            self.dates.append(date(dates[0], dates[1], dates[2]))

    def highlight_days(self):
        """
        todo
        """
        for dates in self.dates:
            self.calendar.calevent_create(dates, "selected", "active")

        self.calendar.tag_config('active', background='#eda8b4')

    def on_selected(self, event):
        """
        todo
        """
        date_selected = event.widget.get_date()
        if date_selected in self.dates_str:
            row_index = self.dates_str.index(date_selected)
            self.gui.table_view.move_table(int(row_index), 0)
        else:
            messagebox.showinfo("Warning", "Date selected is not present in dataset")

    def move_to_date(self, date_index):
        """
        todo
        """
        self.calendar.selection_set(self.dates[date_index])