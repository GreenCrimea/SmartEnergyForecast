"""
gui Module

contains the gui object which is the parent of the tkinter instance
"""
from tkinter import Frame, Toplevel, Button, Label
from pandas import read_csv, concat
from src.table_view import TableView
from src.welcome_page import WelcomePage
from src.date_selector import DateSelector
from src.settings_panel import SettingsPanel
from src.plot_panel import PlotPanel
from src.data_handler import drop_extra_col, import_dataset, wPATHS, wPATHS2
from src.tooltip import CreateToolTip
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class GUI(Frame):
    """
    Creates a tkinter window using TopLevel() which is the master
    parent for the tk instance. Can be instantiated with an optional
    parent.

        Arguments:
            parent (Tk) = The parent tk object 
    """

    def __init__(self, parent = None, geometry = "1000x600"):

        self.month_map = {
            "Jan": '01',
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }

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

        #second axis settings
        self.s_axis = [False]

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
        creates the toolbar above the table, containing buttons to
        switch between table1 and table2, as well as an analyze dataset
        button
        """
        self.selected_table = 1

        ##table 1 button
        #self.table_1_button = Button(self.right_bar_frame, text="Table 1", relief="sunken", command=self.table_1_click)
        #self.table_1_button.pack(side="left", expand=False, fill="y", padx=8)
        #self.table_1_button.pack_propagate(False)

        ##table 2 button
        #self.table_2_button = Button(self.right_bar_frame, text="Table 2", relief="raised", command=self.table_2_click)
        #self.table_2_button.pack(side="left", expand=False, fill="y", padx=8)
        #self.table_2_button.pack_propagate(False)

        #analyze dataset button
        self.analyze_button = Button(self.right_bar_frame, text="Analyze Dataset", command=self.analyze_dataset)
        self.analyze_button.pack(side="right", expand=False, fill="y", padx=14)
        self.analyze_button.pack_propagate(False)
        CreateToolTip(self.analyze_button, text="Analyze data in subplot 1")

    def analyze_dataset(self):
        """
        todo
        """
        window = Toplevel()
        for i in range(len(self.settings_panel.y_data)):
            data_list = self.settings_panel.y_data[i+1]
            for data in data_list:
                frame = Frame(window)
                frame.pack()
                name_frame = Frame(frame)
                name_frame.pack(side="left")
                data_frame = Frame(frame)
                data_frame.pack(side="right", pady=25)
                label_frame = Frame(name_frame)
                label_frame.pack(side="top")
                label = Label(label_frame, text=data.name.replace("_", " "))
                label.pack(side="left")

                val_frame = Frame(data_frame)
                val_frame.pack(side="left")

                max_frame = Frame(val_frame)
                max_frame.pack(side="top")
                max_l = Label(max_frame, text=f"Max: {data.max():.2f}")
                max_l.pack(side="left")

                min_frame = Frame(val_frame)
                min_frame.pack(side="top")
                min_l = Label(min_frame, text=f"Min: {data.min():.2f}")
                min_l.pack(side="left")

                avg_frame = Frame(val_frame)
                avg_frame.pack(side="top")
                avg_l = Label(avg_frame, text=f"Average: {data.mean():.2f}")
                avg_l.pack(side="left")

                std_frame = Frame(val_frame)
                std_frame.pack(side="top")
                std_l = Label(std_frame, text=f"Standard Deviation: {data.std():.2f}")
                std_l.pack()

                plot_frame = Frame(data_frame)
                plot_frame.pack(side="right", padx=20)

                fig = Figure(figsize=(5, 4), dpi=70)

                canvas = FigureCanvasTkAgg(fig, master=plot_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side="right", fill="both", expand=1)

                ax = fig.add_subplot(1,1,1)

                ax.hist(data, bins=10, alpha=0.7)
                ax.set_title(f"{data.name.replace("_", " ")} Histogram")
                ax.set_ylabel("Amount")
                ax.set_xlabel("Value")
                ax.grid(True)
            

        if self.s_axis[0] == True:
            for i in range(len(self.settings_panel.s_y_data)):
                data_list = self.settings_panel.s_y_data[i+1]
                for data in data_list:
                    frame = Frame(window)
                    frame.pack()
                    name_frame = Frame(frame)
                    name_frame.pack(side="left")
                    data_frame = Frame(frame)
                    data_frame.pack(side="right", pady=25)
                    label_frame = Frame(name_frame)
                    label_frame.pack(side="top")
                    label = Label(label_frame, text=data.name.replace("_", " "))
                    label.pack(side="left")

                    val_frame = Frame(data_frame)
                    val_frame.pack(side="left")

                    max_frame = Frame(val_frame)
                    max_frame.pack(side="top")
                    max_l = Label(max_frame, text=f"Max: {data.max():.2f}")
                    max_l.pack(side="left")

                    min_frame = Frame(val_frame)
                    min_frame.pack(side="top")
                    min_l = Label(min_frame, text=f"Min: {data.min():.2f}")
                    min_l.pack(side="left")

                    avg_frame = Frame(val_frame)
                    avg_frame.pack(side="top")
                    avg_l = Label(avg_frame, text=f"Average: {data.mean():.2f}")
                    avg_l.pack(side="left")

                    std_frame = Frame(val_frame)
                    std_frame.pack(side="top")
                    std_l = Label(std_frame, text=f"Standard Deviation: {data.std():.2f}")
                    std_l.pack()

                    plot_frame = Frame(data_frame)
                    plot_frame.pack(side="right", padx=20)

                    fig = Figure(figsize=(5, 4), dpi=70)

                    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

                    ax = fig.add_subplot(1,1,1)

                    ax.hist(data, bins=10, alpha=0.7)
                    ax.set_title(f"{data.name.replace("_", " ")} Histogram")
                    ax.set_ylabel("Amount")
                    ax.set_xlabel("Value")
                    ax.grid(True)


    def table_1_click(self):
        """
        triggered when the table1 button is clicked, destroys the current
        table and re-renders table1
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
            #self.table_1_button.config(relief="sunken")
            #self.table_2_button.config(relief="raised")

    def table_2_click(self):
        """
        triggered when the table2 button is clicked, destroys the current
        table and re-renders table2
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
            #self.table_2_button.configure(relief="sunken")
            #self.table_1_button.configure(relief="raised")

    def load_data(self):
        """
        use the data_handler module to import the datasets
        """
        self.data_1 = import_dataset(wPATHS2, index_col=False, concat=False, skiprows=False)
        self.data_2 = read_csv("./datasets/houses_daily_statistics.csv", index_col=False, encoding="latin-1")
        self.fix_months()
        self.data_2.drop("date", axis=1, inplace=True)
        self.data_1 = concat([self.data_1, self.data_2], axis=1)
        #self.data_1 = drop_extra_col(self.data_1)

    def fix_months(self):
        date = self.data_1["Date"]
        #date2 = self.data_2["Date"]
        var1 = []
        var2 = []
        for dates in date:
            dates = dates.split("-")
            num = [self.month_map[item] for item in dates if item.isalpha()]
            var1.append(f"{dates[2]}-{num[0]}-{dates[0]}")
        #for dates in date2:
        #    dates = dates.split("-")
        #    num = [self.month_map[item] for item in dates if item.isalpha()]
        #    var2.append(f"{dates[2]}-{num[0]}-{dates[0]}")
        
        self.data_1["Date"] = var1
        #self.data_2["Date"] = var2


    def select_table(self):
        """
        change which dataset is in self.dataframe based on the selected table
        """
        if self.selected_table == 1:
            self.dataframe = self.data_1
        elif self.selected_table == 2:
            self.dataframe = self.data_2

    def create_table(self):
        """
        initialize a Tableview object 
        """
        self.table_view = TableView(self.right_table_frame, self)   
        self.table_view.load_dataframe(self.dataframe)
        self.table_view.pack_propagate(False)

    def create_date_selector(self):
        """
        initialize a DateSelector object 
        """
        self.date_selector = DateSelector(self.left_bottom_frame, self)
        self.date_selector.pack_propagate(False)

    def create_settings_panel(self):
        """
        Initialize a SettingsPanel object
        """
        self.settings_panel = SettingsPanel(self.left_top_frame, self)
        self.settings_panel.pack_propagate(False)

    def create_plot_panel(self):
        """
        Initalize a PlotPanel object
        """
        self.plot_panel = PlotPanel(self.right_top_frame, self)
        self.plot_panel.pack_propagate(False)


    def create_welcome_page(self):
        """
        initialize a WelcomePage object
        """
        self.welcome = WelcomePage(self.main)

    def update_sizes(self, event):
        """
        triggered on a window resize, ensures that the scale and ratio
        of different elements stays consistent

            Arguments:
                event (?) = Tk event, not used
        """
        width = self.main.winfo_width()
        height = self.main.winfo_height()

        # Update left frame width
        if width < 1001:
            self.left_frame.config(width=int(0.35 * width))
        else:
            self.left_frame.config(width=int(0.185 * width))

        # Update heights
        self.left_top_frame.config(height=int(0.65 * height))
        self.left_bottom_frame.config(height=int(0.35 * height))
        self.right_bottom_frame.config(height=int(0.35 * height))
        self.right_top_frame.config(height=int(0.60 * height))
        self.right_table_frame.config(height=int((0.40 * height) - 30))

    def create_layout_framing(self):
        """
        creates a hierarchy of frames to then pack the main objects into
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
