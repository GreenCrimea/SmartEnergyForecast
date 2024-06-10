"""
todo
"""
from datetime import date
from tkinter import Frame, messagebox
from tkcalendar import Calendar
from numpy import setdiff1d




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
        self.inactive_date_indexes = None

        #create calendar
        self.calendar = Calendar(self.frame, font=self.gui.font[2], selectmode='day', locale='en_US',
               cursor="hand1", year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2]),
               date_pattern="y-mm-d")
        self.calendar.pack(fill="both", expand=True)
        self.get_date_types()
        self.highlight_days()
        self.highlight_active()
        self.calendar.bind("<<CalendarSelected>>", self.on_selected)

        #get total and active range
        self.total_range = self.get_date_range_str()
        self.active_range = self.get_date_range_str()
        self.offset = 0

        #
        self.getting_selection = False
        self.selection = None
        self.selection_callback = None

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
        self.active_dates = self.dates
        self.active_dates_str = self.dates_str

    def highlight_days(self):
        """
        todo
        """
        for dates in self.dates:
            self.calendar.calevent_create(dates, "total", "total")
        self.calendar.tag_config('total', background='#eda8b4')

    def highlight_active(self):
        """
        todo
        """
        for dates in self.active_dates:
            self.calendar.calevent_create(dates, "active", "active")
        self.calendar.tag_config('active', background='#8bbf8a')

    def on_selected(self, event):
        """
        todo
        """
        if self.getting_selection:
            date_selected = event.widget.get_date()
            if date_selected in self.dates_str:
                self.getting_selection = False
                self.selection = date_selected
                self.selection_callback()
            else:
                messagebox.showinfo("Warning", "Date selected is not present in dataset")
        else:
            date_selected = event.widget.get_date()
            if date_selected in self.dates_str:
                row_index = self.dates_str.index(date_selected)
                self.gui.table_view.move_table(int(row_index) - self.offset, 0)
            else:
                messagebox.showinfo("Warning", "Date selected is not present in dataset")

    def move_to_date(self, date_index):
        """
        todo
        """
        self.calendar.selection_set(self.dates[date_index - self.offset])

    def get_date_range(self):
        """
        todo
        """
        return (self.dates[0], self.dates[-1])

    def get_date_range_str(self):
        """
        todo
        """
        return (self.dates_str[0], self.dates_str[-1])

    def change_active_range(self, date_from = None, date_to = None, s=""):
        """
        todo
        """
        if s == "F":
            date_to = self.active_range[1]
        elif s == "T":
            date_from = self.active_range[0]

        self.active_range = (date_from, date_to)
        
        from_index = self.dates_str.index(date_from)
        to_index = self.dates_str.index(date_to) + 1

        self.active_dates = self.dates[from_index:to_index]
        self.active_dates_str = self.dates_str[from_index:to_index]

        self.inactive_dates = setdiff1d(self.dates, self.active_dates)
        self.inactive_dates_str = setdiff1d(self.dates_str, self.active_dates_str)

        inactive_beginning_dates = self.dates[from_index:]
        beginning_diff = setdiff1d(self.dates, inactive_beginning_dates)
        self.offset = len(beginning_diff)

        self.inactive_date_indexes = []
        for idx, dates in enumerate(self.dates_str):
            if dates in self.inactive_dates_str:
                self.inactive_date_indexes.append(idx)

        self.gui.table_view.set_inactive_rows()
        self.calendar.calevent_remove("all")
        self.highlight_days()
        self.highlight_active()

