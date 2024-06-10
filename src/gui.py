"""
gui Module

contains the gui object which is the parent of the tkinter instance
"""
from tkinter import Frame, Toplevel, Button
from src.table_view import TableView
from src.welcome_page import WelcomePage
from src.date_selector import DateSelector
from src.settings_panel import SettingsPanel
from src.plot_panel import PlotPanel
from src.data_handler import drop_extra_col, import_dataset, wPATHS



class GUI(Frame):
    """
    Creates a tkinter window using TopLevel() which is the master
    parent for the tk instance. Can be instantiated with an optional
    parent.

        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent = None, geometry = "1000x600"):

        #initialize parent or top level window
        self.parent=parent
        if not self.parent:
            Frame.__init__(self)
            self.main=self.master
        else:
            self.main=Toplevel()
            self.master=self.main

        #style
        self.master.geometry(geometry)
        self.font = ("Arial", "10", "Arial 10")

        #active data
        self.dataframe = None

        #initialize default main layout
        self.create_layout_framing()
        self.create_table_toolbar()
        self.load_data()
        self.select_table()
        self.create_table()
        self.create_date_selector()
        self.create_settings_panel()
        self.create_plot_panel()

        #bind resizing to layout
        self.main.bind('<Configure>', self.update_sizes)

        #open welcome page
        #self.create_welcome_page()

    def create_table_toolbar(self):
        """
        todo
        """
        self.selected_table = 1

        self.table_1_button = Button(self.right_bar_frame, text="Table 1", relief="sunken", command=self.table_1_click)
        self.table_1_button.pack(side="left", expand=False, fill="y", padx=8)
        self.table_1_button.pack_propagate(False)

        self.table_2_button = Button(self.right_bar_frame, text="Table 2", relief="raised", command=self.table_2_click)
        self.table_2_button.pack(side="left", expand=False, fill="y", padx=8)
        self.table_2_button.pack_propagate(False)

        self.analyze_button = Button(self.right_bar_frame, text="Analyze Dataset", command=None)
        self.analyze_button.pack(side="right", expand=False, fill="y", padx=14)
        self.analyze_button.pack_propagate(False)

    def table_1_click(self):
        """
        todo
        """
        if self.selected_table == 1:
            pass
        else:
            self.selected_table = 1
            self.select_table()
            self.table_view.table.forget()
            self.table_view.table.destroy()
            self.table_view.frame.forget()
            self.table_view.frame.destroy()
            self.table_view.forget()
            self.table_view.destroy()
            self.create_table()
            self.table_view.set_inactive_rows()
            self.table_1_button.config(relief="sunken")
            self.table_2_button.config(relief="raised")

    def table_2_click(self):
        """
        todo
        """
        if self.selected_table == 2:
            pass
        else:
            self.selected_table = 2
            self.select_table()
            self.table_view.table.forget()
            self.table_view.table.destroy()
            self.table_view.frame.forget()
            self.table_view.frame.destroy()
            self.table_view.forget()
            self.table_view.destroy()
            self.create_table()
            self.table_view.set_inactive_rows()
            self.table_2_button.configure(relief="sunken")
            self.table_1_button.configure(relief="raised")

    def load_data(self):
        """
        todo
        """
        
        self.data_1 = import_dataset(wPATHS, index_col=False, concat=True, skiprows=8)
        self.data_2 = import_dataset(wPATHS, index_col=False, concat=True, skiprows=8)
        self.data_1 = drop_extra_col(self.data_1)

    def select_table(self):
        """
        todo
        """
        if self.selected_table == 1:
            self.dataframe = self.data_1
        elif self.selected_table == 2:
            self.dataframe = self.data_2

    def create_table(self):
        """
        initialize a Tableview object in its empty state 
        """
        self.table_view = TableView(self.right_table_frame, self)   
        self.table_view.load_dataframe(self.dataframe)
        self.table_view.pack_propagate(False)

    def create_date_selector(self):
        """
        todo
        """
        self.date_selector = DateSelector(self.left_bottom_frame, self)
        self.date_selector.pack_propagate(False)

    def create_settings_panel(self):
        """
        todo
        """
        self.settings_panel = SettingsPanel(self.left_top_frame, self)
        self.settings_panel.pack_propagate(False)

    def create_plot_panel(self):
        """
        todo
        """
        self.plot_panel = PlotPanel(self.right_top_frame)
        self.plot_panel.pack_propagate(False)


    def create_welcome_page(self):
        """
        initialize a WelcomePage object
        """
        self.welcome = WelcomePage(self.main)

    def update_sizes(self, event):
        """
        todo
        """
        width = self.main.winfo_width()
        height = self.main.winfo_height()

        # Update left frame width to 20% of total width
        if width < 1001:
            self.left_frame.config(width=int(0.35 * width))
        else:
            self.left_frame.config(width=int(0.25 * width))

        # Update heights
        self.left_top_frame.config(height=int(0.65 * height))
        self.left_bottom_frame.config(height=int(0.35 * height))
        self.right_bottom_frame.config(height=int(0.35 * height))
        self.right_top_frame.config(height=int(0.60 * height))
        self.right_table_frame.config(height=int((0.40 * height) - 30))

    def create_layout_framing(self):
        """
        todo
        """
        self.left_frame = Frame(self.main)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)

        self.left_bottom_frame = Frame(self.left_frame)
        self.left_bottom_frame.pack(side="bottom", expand=True, fill="both")
        self.left_bottom_frame.pack_propagate(False)

        self.left_top_frame = Frame(self.left_frame)
        self.left_top_frame.pack(side="top", expand=True, fill="both")
        self.left_top_frame.pack_propagate(False)

        self.right_frame = Frame(self.main)
        self.right_frame.pack(side="left", expand=True, fill="both")
        self.right_frame.pack_propagate(False)

        self.right_bottom_frame = Frame(self.right_frame)
        self.right_bottom_frame.pack(side="bottom", expand=True, fill="both")
        self.right_bottom_frame.pack_propagate(False)

        self.right_top_frame = Frame(self.right_frame)
        self.right_top_frame.pack(side="top", expand=True, fill="both")
        self.right_top_frame.pack_propagate(False)

        self.right_bar_frame = Frame(self.right_bottom_frame, height=30)
        self.right_bar_frame.pack(side="top", expand=True, fill="both")
        self.right_bar_frame.pack_propagate(False)

        self.right_table_frame = Frame(self.right_bottom_frame)
        self.right_table_frame.pack(side="bottom", expand=True, fill="both")
        self.right_table_frame.pack_propagate(False)
