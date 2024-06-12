"""
todo
"""
from tkinter import Frame, Label, Entry, Button, messagebox, Canvas, Scrollbar, Text, IntVar, Radiobutton
from tkinter.ttk import Combobox
from matplotlib.pyplot import plot, bar, scatter
from numpy import arange
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

        self.data_1_active = self.gui.data_1
        self.data_2_active = self.gui.data_2

        self.selecting_column = False
        self.selecting_axis = 1

        self.from_len = 0
        self.to_len = 0

        self.default_graph_settings()
        self.initialize_date_range()
        self.initialize_settings_panel()
        self.populate_ydata_input(1)

    def default_graph_settings(self):
        """
        todo
        """
        self.plot_type = {1: None}

        self.subplot_dimensions = (1,1)
        self.num_subplots = 1

        self.x_data = {1: arange(len(self.gui.dataframe))}

        self.y_data = {1: []}
        self.active_columns = {1: ["MaximumTemperature__C_", "MinimumTemperature__C_"]}
        self.y_data[1].append(self.data_1_active["MaximumTemperature__C_"])
        self.y_data[1].append(self.data_1_active["MinimumTemperature__C_"])

        #second axis
        self.s_y_data = {1: []}
        self.s_active_columns = {1: ["house3_average"]}
        self.s_y_data[1].append(self.data_1_active["house3_average"])

    def initialize_settings_panel(self):
        """
        todo
        """
        self.settings_frame = Frame(self.frame)
        self.settings_frame.pack(side="top", fill="both", expand=True)
        self.settings_frame.pack_propagate(False)

        self.scrollbar_frame = Frame(self.settings_frame, bg="blue")
        self.scrollbar_frame.pack(side="right", fill="y", expand=True)

        self.settings_canvas = Canvas(self.settings_frame)
        self.settings_canvas.pack(side="left", fill="y", expand=True)

        self.settings_scrollbar = Scrollbar(self.scrollbar_frame, orient="vertical", command=self.settings_canvas.yview)
        self.settings_scrollbar.pack(side="right", fill="y", expand=True)

        self.scrollable_frame = Frame(self.settings_canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.settings_canvas.configure(
                scrollregion=self.settings_canvas.bbox("all")
            )
        )

        self.settings_canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows and macOS
        self.settings_canvas.bind("<Button-4>", self.on_mouse_wheel)    # Linux (scroll up)
        self.settings_canvas.bind("<Button-5>", self.on_mouse_wheel)    # Linux (scroll down)

        self.settings_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.settings_canvas.configure(yscrollcommand=self.settings_scrollbar.set)

        #subplot size
        self.subplot_frame = Frame(self.scrollable_frame)
        self.subplot_frame.pack(side="top", expand=False, fill="x", pady=2)
        self.subplot_label = Label(self.subplot_frame, text="Subplot Dimensions:")
        self.subplot_label.pack(side="left", padx=4)
        self.subplot_x_input = Entry(self.subplot_frame, width=3)
        self.subplot_x_input.insert(0, str(self.subplot_dimensions[0]))
        self.subplot_x_input.pack(side="left")
        self.subplot_by_label = Label(self.subplot_frame, text="by")
        self.subplot_by_label.pack(side="left", padx=4)
        self.subplot_y_input = Entry(self.subplot_frame, width=3)
        self.subplot_y_input.insert(0, str(self.subplot_dimensions[1]))
        self.subplot_y_input.pack(side="left")
        self.subplot_button = Button(self.subplot_frame, text="Ok", command=self.subplot_button_click)
        self.subplot_button.pack(side="left", padx=3)

        #plot type
        self.plot_type_menu = {}
        for i in range(self.num_subplots):
            plot_type_frame = Frame(self.scrollable_frame)
            plot_type_frame.pack(side="top", fill="x")
            plot_type_label = Label(plot_type_frame, text=f"Plot {i+1} type:")
            plot_type_label.pack(side="left", padx=4)
            plot_plot_button = Button(plot_type_frame, text="plot", relief="sunken", command=lambda i=i: self.plot_button(i+1))
            plot_plot_button.pack(side="left", padx=2)
            plot_bar_button = Button(plot_type_frame, text="bar", relief="raised", command=lambda i=i: self.bar_button(i+1))
            plot_bar_button.pack(side="left", padx=2)
            plot_scatter_button = Button(plot_type_frame, text="scatter", relief="raised", command=lambda i=i: self.scatter_button(i+1))
            plot_scatter_button.pack(side="left", padx=2)
            new_dict = {i+1: [plot_type_frame, plot_type_label, plot_plot_button, plot_bar_button, plot_scatter_button]}
            self.plot_type_menu.update(new_dict)

        #y data
        self.y_data_menu = {}
        self.eyedropper_icon = Image.open("assets/eye-dropper.png")
        self.eyedropper_icon = ImageTk.PhotoImage(self.eyedropper_icon)
        for i in range(self.num_subplots):
            y_data_frame = Frame(self.scrollable_frame, height=100)
            y_data_frame.pack(side="top", fill="x", pady=4)
            y_data_frame.pack_propagate(False)
            y_data_label = Label(y_data_frame, text=f"Plot {i+1} y-data:")
            y_data_label.pack(side="left", padx=4)
            y_data_input = Text(y_data_frame, font=("Arial", 8), wrap="word", width=25)
            y_data_input.pack(side="left")
            y_data_button_frame = Frame(y_data_frame)
            y_data_button_frame.pack(side="right", fill="both", expand=True)
            y_data_button_frame.pack_propagate(False)
            y_data_select_button = Button(y_data_button_frame, image=self.eyedropper_icon,
                                          command= lambda i=i: self.get_ydata(i+1))
            y_data_select_button.pack(side="top", pady=8)
            CreateToolTip(y_data_select_button, text="Select columns from the table as y-data input")
            y_data_ok_button = Button(y_data_button_frame, text="Ok", command= lambda i=i: self.update_ydata(i+1))
            y_data_ok_button.pack(side="bottom", pady=8)
            CreateToolTip(y_data_ok_button, text="confirm selection")
            new_dict = {i+1: [y_data_frame, y_data_label, y_data_input, y_data_button_frame,
                              y_data_select_button, y_data_ok_button]}
            self.y_data_menu.update(new_dict)

        #second axis button:
        self.s_axis_menu = {}
        for i in range(self.num_subplots):
            var = IntVar()
            s_axis_frame = Frame(self.scrollable_frame, height=30)
            s_axis_frame.pack(side="top", fill="x", pady=4)
            s_axis_frame.pack_propagate(False)
            s_axis_label = Label(s_axis_frame, text=f"Plot {i+1} Second Y axis:")
            s_axis_label.pack(side="left", padx=4)
            s_axis_on_button = Radiobutton(s_axis_frame, variable=var, value=1, text="On", 
                                           command=lambda i=i: self.s_axis_on(i))
            s_axis_on_button.pack(side="left", fill="y", padx=2)
            s_axis_off_button = Radiobutton(s_axis_frame, variable=var, value=0, text="Off", 
                                command=lambda i=i: self.s_axis_off(i))
            s_axis_off_button.pack(side="left", fill="y", padx=2)

        #second axis y data
        if len(self.gui.s_axis) < self.num_subplots:
                if i > 0 and i >= len(self.gui.s_axis):
                    self.gui.s_axis.append(False)

        self.s_y_data_menu = {}
        for i in range(self.num_subplots):
            if self.gui.s_axis[i] == True:
                s_y_data_frame = Frame(self.scrollable_frame, height=100)
                s_y_data_frame.pack(side="top", fill="x", pady=4)
                s_y_data_frame.pack_propagate(False)
                s_y_data_label = Label(s_y_data_frame, text=f"Plot {i+1} 2nd y-data:")
                s_y_data_label.pack(side="left", padx=4)
                s_y_data_input = Text(s_y_data_frame, font=("Arial", 8), wrap="word", width=22)
                s_y_data_input.pack(side="left")
                s_y_data_button_frame = Frame(s_y_data_frame)
                s_y_data_button_frame.pack(side="right", fill="both", expand=True)
                s_y_data_button_frame.pack_propagate(False)
                s_y_data_select_button = Button(s_y_data_button_frame, image=self.eyedropper_icon,
                                              command= lambda i=i: self.get_ydata(i+1, True))
                s_y_data_select_button.pack(side="top", pady=8)
                CreateToolTip(y_data_select_button, text="Select columns from the table as y-data input")
                s_y_data_ok_button = Button(s_y_data_button_frame, text="Ok", command= lambda i=i: self.update_ydata(i+1, True))
                s_y_data_ok_button.pack(side="bottom", pady=8)
                CreateToolTip(y_data_ok_button, text="confirm selection")
                new_dict = {i+1: [s_y_data_frame, s_y_data_label, s_y_data_input, s_y_data_button_frame,
                                  s_y_data_select_button, s_y_data_ok_button]}
                self.s_y_data_menu.update(new_dict)

        #title
        self.title_menu = {}
        for i in range(self.num_subplots):
            title_frame = Frame(self.scrollable_frame, height=30)
            title_frame.pack(side="top", fill="x", pady=4)
            title_frame.pack_propagate(False)
            title_label = Label(title_frame, text=f"Plot {i+1} title:")
            title_label.pack(side="left", padx=4)
            title_input = Entry(title_frame, width=19)
            title_input.pack(side="left", padx=4)
            title_ok_button = Button(title_frame, text="Ok", command= lambda i=i: self.update_title(i+1))
            title_ok_button.pack(side="right")
            new_dict = {i+1: [title_frame, title_label, title_input, title_ok_button]}
            self.title_menu.update(new_dict)

        #y label
        self.y_label_menu = {}
        for i in range(self.num_subplots):
            y_label_frame = Frame(self.scrollable_frame, height=30)
            y_label_frame.pack(side="top", fill="x", pady=4)
            y_label_frame.pack_propagate(False)
            y_label_label = Label(y_label_frame, text=f"Plot {i+1} y-Label:")
            y_label_label.pack(side="left", padx=4)
            y_label_input = Entry(y_label_frame, width=17)
            y_label_input.pack(side="left", padx=4)
            y_label_ok_button = Button(y_label_frame, text="Ok", command= lambda i=i: self.update_y_label(i+1))
            y_label_ok_button.pack(side="right")
            new_dict = {i+1: [y_label_frame, y_label_label, y_label_input, y_label_ok_button]}
            self.y_label_menu.update(new_dict)

        #second axis y label
        self.s_y_label_menu = {}
        for i in range(self.num_subplots):
            if self.gui.s_axis[i] == True:
                s_y_label_frame = Frame(self.scrollable_frame, height=30)
                s_y_label_frame.pack(side="top", fill="x", pady=4)
                s_y_label_frame.pack_propagate(False)
                s_y_label_label = Label(s_y_label_frame, text=f"Plot {i+1} 2nd y-Label:")
                s_y_label_label.pack(side="left", padx=4)
                s_y_label_input = Entry(s_y_label_frame, width=13)
                s_y_label_input.pack(side="left", padx=4)
                s_y_label_ok_button = Button(s_y_label_frame, text="Ok", command= lambda i=i: self.update_y_label(i+1, True))
                s_y_label_ok_button.pack(side="right")
                new_dict = {i+1: [s_y_label_frame, s_y_label_label, s_y_label_input, s_y_label_ok_button]}
                self.s_y_label_menu.update(new_dict)

        #x label
        self.x_label_menu = {}
        for i in range(self.num_subplots):
            x_label_frame = Frame(self.scrollable_frame, height=30)
            x_label_frame.pack(side="top", fill="x", pady=4)
            x_label_frame.pack_propagate(False)
            x_label_label = Label(x_label_frame, text=f"Plot {i+1} x-Label:")
            x_label_label.pack(side="left", padx=4)
            x_label_input = Entry(x_label_frame, width=17)
            x_label_input.pack(side="left", padx=4)
            x_label_ok_button = Button(x_label_frame, text="Ok", command= lambda i=i: self.update_x_label(i+1))
            x_label_ok_button.pack(side="right")
            new_dict = {i+1: [x_label_frame, x_label_label, x_label_input, x_label_ok_button]}
            self.x_label_menu.update(new_dict)

        #x ticks
        self.x_ticks_menu = {}
        for i in range(self.num_subplots):
            var = IntVar()
            x_ticks_frame = Frame(self.scrollable_frame, height=30)
            x_ticks_frame.pack(side="top", fill="x", pady=4)
            x_ticks_frame.pack_propagate(False)
            x_ticks_label = Label(x_ticks_frame, text=f"Plot {i+1} x-ticks:")
            x_ticks_label.pack(side="left", fill="y", padx=4)
            x_ticks_days_button = Radiobutton(x_ticks_frame, variable=var, value=1, text="Days", 
                                           command=lambda i=i: self.x_ticks_days(i))
            x_ticks_days_button.pack(side="left", fill="y", padx=2)
            x_ticks_date_button = Radiobutton(x_ticks_frame, variable=var, value=0, text="Date", 
                                command=lambda i=i: self.x_ticks_date(i))
            x_ticks_date_button.pack(side="left", fill="y", padx=2)

        #grid button:
        self.grid_menu = {}
        for i in range(self.num_subplots):
            var = IntVar()
            grid_frame = Frame(self.scrollable_frame, height=30)
            grid_frame.pack(side="top", fill="x", pady=4)
            grid_frame.pack_propagate(False)
            grid_label = Label(grid_frame, text=f"Plot {i+1} Gridlines:")
            grid_label.pack(side="left", padx=4)
            grid_pad = Frame(grid_frame, width=10)
            grid_pad.pack(side="left")
            grid_on_button = Radiobutton(grid_frame, variable=var, value=1, text="On", 
                                           command=lambda i=i: self.grid_on(i))
            grid_on_button.pack(side="left", fill="y", padx=2)
            grid_off_button = Radiobutton(grid_frame, variable=var, value=0, text="Off", 
                                command=lambda i=i: self.grid_off(i))
            grid_off_button.pack(side="left", fill="y", padx=2)

        #ylim
        self.ylim_menu = {}
        for i in range(self.num_subplots):
            ylim_frame = Frame(self.scrollable_frame, height=30)
            ylim_frame.pack(side="top", fill="x", pady=4)
            ylim_frame.pack_propagate(False)
            ylim_label = Label(ylim_frame, text=f"Plot {i+1} y-Limits:")
            ylim_label.pack(side="left", padx=4)
            ylim_input = Entry(ylim_frame, width=17)
            ylim_input.pack(side="left", padx=4)
            ylim_ok_button = Button(ylim_frame, text="Ok", command= lambda i=i: self.update_ylim(i+1))
            ylim_ok_button.pack(side="right")
            new_dict = {i+1: [ylim_frame, ylim_label, ylim_input, ylim_ok_button]}
            self.ylim_menu.update(new_dict)

        #2nd axis ylim
        self.s_ylim_menu = {}
        for i in range(self.num_subplots):
            if self.gui.s_axis[i] == True:
                s_ylim_frame = Frame(self.scrollable_frame, height=30)
                s_ylim_frame.pack(side="top", fill="x", pady=4)
                s_ylim_frame.pack_propagate(False)
                s_ylim_label = Label(s_ylim_frame, text=f"Plot {i+1} 2nd y-Limits:")
                s_ylim_label.pack(side="left", padx=4)
                s_ylim_input = Entry(s_ylim_frame, width=12)
                s_ylim_input.pack(side="left", padx=4)
                s_ylim_ok_button = Button(s_ylim_frame, text="Ok", command= lambda i=i: self.update_ylim(i+1, True))
                s_ylim_ok_button.pack(side="right")
                new_dict = {i+1: [s_ylim_frame, s_ylim_label, s_ylim_input, s_ylim_ok_button]}
                self.s_ylim_menu.update(new_dict)

        #legend
        self.legend_menu = {}
        for i in range(self.num_subplots):
            values = ["best", 'upper left', 'upper right', 'lower left', 'lower right', \
                      'upper center', 'lower center', 'center left', 'center right', "center"]
            var=IntVar()
            legend_frame = Frame(self.scrollable_frame, height=30)
            legend_frame.pack(side="top", fill="x", pady=4)
            legend_frame.pack_propagate(False)
            legend_label = Label(legend_frame, text=f"Plot {i+1} Legend:")
            legend_label.pack(side="left", fill="y", padx=4)
            legend_on_button = Radiobutton(legend_frame, variable=var, value=1, text="On", 
                                           command=lambda i=i: self.legend_on(i))
            legend_on_button.pack(side="left", fill="y", padx=2)
            legend_off_button = Radiobutton(legend_frame, variable=var, value=0, text="Off", 
                                command=lambda i=i: self.legend_off(i))
            legend_off_button.pack(side="left", fill="y", padx=2)
            legend_loc_frame = Frame(self.scrollable_frame, height=30)
            legend_loc_frame.pack(side="top", fill="x", pady=4)
            legend_loc_frame.pack_propagate(False)
            legend_loc_label = Label(legend_loc_frame, text="Legend location:")
            legend_loc_label.pack(side="left", fill="y", padx=3)
            legend_loc_input = Combobox(legend_loc_frame, values=values, width=15)
            legend_loc_input.pack(side="left", fill="y", padx=3)
            legend_loc_button = Button(legend_loc_frame, text="Ok", command=lambda i=i: self.legend_loc(i))
            legend_loc_button.pack(side="right")
            new_dict = {i+1: [legend_frame, legend_label, legend_on_button, legend_off_button,
                              legend_loc_frame, legend_loc_label, legend_loc_input, legend_loc_button]}
            self.legend_menu.update(new_dict)

        #colour
        self.colour_menu = {}
        for i in range(self.num_subplots):
            values = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",\
                      "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "black"]
            colour_menu_element = {}
            if i+1 in self.y_data:
                x = len(self.y_data[i+1])
            else:
                x = 2
            for j in range(x): 
                var=IntVar()
                colour_frame = Frame(self.scrollable_frame, height=30)
                colour_frame.pack(side="top", fill="x", pady=4)
                colour_frame.pack_propagate(False)
                colour_label = Label(colour_frame, text=f"Plot {i+1} item {j+1} Colour:")
                colour_label.pack(side="left", fill="y", padx=4)
                colour_input = Combobox(colour_frame, values=values, width=10)
                colour_input.pack(side="left", fill="y", padx=3)
                colour_button = Button(colour_frame, text="Ok", command=lambda i=i, j=j: self.set_colour(i, j))
                colour_button.pack(side="right")
                new_dict = {j: [colour_frame, colour_label, colour_input, colour_button]}
                colour_menu_element.update(new_dict)
            _new_dict = {i+1: colour_menu_element}
            self.colour_menu.update(_new_dict)

        #colour 2nd axis
        self.s_colour_menu = {}
        for i in range(self.num_subplots):
            if self.gui.s_axis[i] == True:
                values = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",\
                          "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "black"]
                s_colour_menu_element = {}
                if i+1 in self.s_y_data:
                    x = len(self.s_y_data[i+1])
                else:
                    x = 1
                for j in range(x): 
                    var=IntVar()
                    s_colour_frame = Frame(self.scrollable_frame, height=30)
                    s_colour_frame.pack(side="top", fill="x", pady=4)
                    s_colour_frame.pack_propagate(False)
                    s_colour_label = Label(s_colour_frame, text=f"Plot{i+1}-2 item{j+1} Colour:")
                    s_colour_label.pack(side="left", fill="y", padx=4)
                    s_colour_input = Combobox(s_colour_frame, values=values, width=10)
                    s_colour_input.pack(side="left", fill="y", padx=3)
                    s_colour_button = Button(s_colour_frame, text="Ok", command=lambda i=i, j=j: self.set_colour(i, j, True))
                    s_colour_button.pack(side="right")
                    new_dict = {j: [s_colour_frame, s_colour_label, s_colour_input, s_colour_button]}
                    s_colour_menu_element.update(new_dict)
                _new_dict = {i+1: s_colour_menu_element}
                self.s_colour_menu.update(_new_dict)

    def set_colour(self, i, j, s_axis=False):
        """
        todo
        """
        if s_axis == True:
            input = self.s_colour_menu[i+1][j]
            input = input[2].get()
            label1 = self.gui.plot_panel.s_colours[0]
            if len(self.gui.plot_panel.s_colours) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.s_colours.append(label1)
            self.gui.plot_panel.s_colours[i][j] = input
            self.redraw_settings()
        else:
            input = self.colour_menu[i+1][j]
            input = input[2].get()
            label1 = self.gui.plot_panel.colours[0]
            if len(self.gui.plot_panel.colours) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.colours.append(label1)
            self.gui.plot_panel.colours[i][j] = input
            self.redraw_settings()

    def grid_on(self, i):
        """
        todo
        """
        if self.gui.plot_panel.grid[i] == False:
            self.gui.plot_panel.grid[i] = True
        if len(self.gui.plot_panel.grid) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.grid.append(False)
        self.redraw_settings()

    def grid_off(self, i):
        """
        todo
        """
        if self.gui.plot_panel.grid [i] == True:
            self.gui.plot_panel.grid[i] = False
        if len(self.gui.plot_panel.grid) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.grid.append(False)
        self.redraw_settings()

    def s_axis_on(self, i):
        """
        todo
        """
        if self.gui.s_axis[i] == False:
            self.gui.s_axis[i] = True
        if len(self.gui.s_axis) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.s_axis.append(False)
        self.redraw_settings()

    def s_axis_off(self, i):
        """
        todo
        """
        if self.gui.s_axis[i] == True:
            self.gui.s_axis[i] = False
        if len(self.gui.s_axis) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.s_axis.append(False)
        self.redraw_settings()

    def update_ylim(self, i, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            input = self.s_ylim_menu[i][2].get()
            input = input.replace(" ", "").split(",")
            if len(self.gui.plot_panel.s_ylim) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.s_ylim.append(False)
            self.gui.plot_panel.s_ylim[i-1] = [input[0], input[1]]
            self.redraw_settings()
        else:
            input = self.ylim_menu[i][2].get()
            input = input.replace(" ", "").split(",")
            if len(self.gui.plot_panel.ylim) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.ylim.append(False)
            self.gui.plot_panel.ylim[i-1] = [input[0], input[1]]
            self.redraw_settings()

    def x_ticks_date(self, i):
        """
        todo
        """
        if self.gui.plot_panel.x_ticks[i] == 1:
            self.gui.plot_panel.x_ticks[i] = 0
        if len(self.gui.plot_panel.x_ticks) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.x_ticks.append(1)
        self.redraw_settings()

    def x_ticks_days(self, i):
        """
        todo
        """
        if self.gui.plot_panel.x_ticks[i] == 0:
            self.gui.plot_panel.x_ticks[i] = 1
        if len(self.gui.plot_panel.x_ticks) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.x_ticks.append(1)
        self.redraw_settings()

    def legend_on(self, i):
        """
        todo
        """
        if self.gui.plot_panel.legend[i] == False:
            self.gui.plot_panel.legend[i] = True
        if len(self.gui.plot_panel.legend) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.legend.append(False)
        self.redraw_settings()

    def legend_off(self, i):
        """
        todo
        """
        if self.gui.plot_panel.legend[i] == True:
            self.gui.plot_panel.legend[i] = False
        if len(self.gui.plot_panel.legend) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.legend.append(False)
        self.redraw_settings()

    def legend_loc(self, i):
        """
        todo
        """
        self.gui.plot_panel.legend_loc[i] = self.legend_menu[i+1][6].get()
        if len(self.gui.plot_panel.legend_loc) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.legend_loc.append("lower right")
        self.redraw_settings()

    def update_x_label(self, i):
        """
        todo
        """
        input = self.x_label_menu[i][2].get()
        label1 = self.gui.plot_panel.x_labels[0]
        if len(self.gui.plot_panel.x_labels) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.x_labels.append(label1)
        self.gui.plot_panel.x_labels[i-1] = input
        self.redraw_settings()

    def update_y_label(self, i, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            input = self.s_y_label_menu[i][2].get()
            label1 = self.gui.plot_panel.s_y_labels[0]
            if len(self.gui.plot_panel.s_y_labels) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.s_y_labels.append(label1)
            self.gui.plot_panel.s_y_labels[i-1] = input
            self.redraw_settings()
        else:
            input = self.y_label_menu[i][2].get()
            label1 = self.gui.plot_panel.y_labels[0]
            if len(self.gui.plot_panel.y_labels) < self.num_subplots:
                for i in range(len(self.num_subplots) -1):
                    self.gui.plot_panel.y_labels.append(label1)
            self.gui.plot_panel.y_labels[i-1] = input
            self.redraw_settings()

    def update_title(self, i):
        """
        todo
        """
        input = self.title_menu[i][2].get()
        title1 = self.gui.plot_panel.titles[0]
        if len(self.gui.plot_panel.titles) < self.num_subplots:
            for i in range(len(self.num_subplots) -1):
                self.gui.plot_panel.titles.append(title1)
        self.gui.plot_panel.titles[i-1] = input
        self.redraw_settings()

    def update_ydata(self, i, second_axis=False):
        """
        todo
        """
        if second_axis == True:
            input_list = self.get_ydata_input(i, True)
            input_list = input_list[:-1]
        else:
            input_list = self.get_ydata_input(i)
            input_list = input_list[:-1]

        data_list = []
        if second_axis == True:
            for j in range(len(self.s_y_data[i])):
                data_list.append(self.s_y_data[i][j].name)
        else:
            for j in range(len(self.y_data[i])):
                data_list.append(self.y_data[i][j].name)

        column_list = []
        if second_axis == True:
            for item in input_list:
                if item[0] == " ":
                    item = item[1:]
                column_list.append(item)
                if item not in data_list:
                    self.s_y_data[i].append(self.data_1_active[item])
        else:
            for item in input_list:
                if item[0] == " ":
                    item = item[1:]
                column_list.append(item)
                if item not in data_list:
                    self.y_data[i].append(self.data_1_active[item])

        new_col = []
        for k in range(len(input_list)):
            new_col.append(input_list[k])
            
        if second_axis == True:
            self.s_active_columns[i] = new_col
        else:
            self.active_columns[i] = new_col
        self.redraw_settings()

        if second_axis == True:
            self.reset_ydata_input(i, True)
            for col in new_col:
                self.insert_ydata_input(i, col, True)
            self.selecting_axis = 1
            self.selecting_column = False
        else:
            self.reset_ydata_input(i)
            for col in new_col:
                self.insert_ydata_input(i, col)
            self.selecting_column = False
        

    def get_ydata(self, i, second_axis=False):
        """
        todo
        """
        self.selecting_column = i
        if second_axis == True:
            self.selecting_axis = 2

    def get_ydata_input(self, i, second_axis=False):
        """
        todo
        """
        if second_axis == True:
            string = self.s_y_data_menu[i][2].get("1.0", "end")
        else:
            string = self.y_data_menu[i][2].get("1.0", "end")
        list_ = [item for item in string.replace('"', '').replace("\n", "").split(",") if item]
        list__ = []
        for item in list_:
            if item[0] == " ":
                item = item[1:]
            list__.append(item)
        return list__

    def reset_ydata_input(self, i, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            self.s_y_data_menu[i][2].delete("1.0", "end")
        else:
            self.s_y_data_menu[i][2].delete("1.0", "end")

    def insert_ydata_input(self, i, string, second_axis=False):
        """
        todo
        """
        if second_axis == True:
            self.s_y_data_menu[i][2].insert("end", f'"{string}", ')
        else:
            self.y_data_menu[i][2].insert("end", f'"{string}", ')

    def populate_ydata_input(self, i, second_axis=False):
        """
        todo
        """
        if second_axis == True:
            for item in self.s_y_data[i]:
                self.s_y_data_menu[i][2].insert("end", f'"{item.name}", ')
        else:
            for item in self.y_data[i]:
                self.y_data_menu[i][2].insert("end", f'"{item.name}", ')

    def subplot_button_click(self):
        """
        todo
        """
        self.subplot_dimensions = (int(self.subplot_x_input.get()), int(self.subplot_y_input.get()))
        self.num_subplots = int(self.subplot_x_input.get()) * int(self.subplot_y_input.get())
        self.redraw_settings()

    def redraw_settings(self):
        """
        todo
        """

        self.frame.forget()
        self.frame.destroy()

        self.frame = Frame(self.main)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.pack_propagate(False)

        self.initialize_date_range()
        self.initialize_settings_panel()

        self.data_1_active = self.gui.table_view.df
        self.data_2_active = self.gui.table_view.df

        new_y_data = {}
        s_new_y_data = {}
        for i in range(self.num_subplots):

            #legend
            if len(self.gui.plot_panel.legend) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.legend):
                    self.gui.plot_panel.legend.append(True)

            #ylim
            if len(self.gui.plot_panel.ylim) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.ylim):
                    self.gui.plot_panel.ylim.append(False)

            #2nd axis ylim
            if len(self.gui.plot_panel.s_ylim) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.s_ylim):
                    self.gui.plot_panel.s_ylim.append(False)

            #legend location
            if len(self.gui.plot_panel.legend_loc) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.legend_loc):
                    self.gui.plot_panel.legend_loc.append("lower right")

            #x ticks
            if len(self.gui.plot_panel.x_ticks) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.x_ticks):
                    self.gui.plot_panel.x_ticks.append(1)

            #grid
            if len(self.gui.plot_panel.grid) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.grid):
                    self.gui.plot_panel.grid.append(False)

            #ydata
            new_y_data.update({i+1: []})
            if len(self.active_columns) == self.num_subplots:
                for j in range(len(self.active_columns[i+1])):
                    new_y_data[i+1].append(self.data_1_active[self.active_columns[i+1][j]])
            else:
                new_dict_ = {}
                for j in range(len(self.active_columns[1])):
                    new_dict_.update({j+1: self.active_columns[1]})
                    new_y_data[i+1].append(self.data_1_active[self.active_columns[1][j]])
                self.active_columns = new_dict_

            #second ydata
            s_new_y_data.update({i+1: []})
            if len(self.s_active_columns) == self.num_subplots:
                for j in range(len(self.s_active_columns[i+1])):
                    s_new_y_data[i+1].append(self.data_1_active[self.s_active_columns[i+1][j]])
            else:
                new_dict_ = {}
                for j in range(len(self.s_active_columns[1])):
                    new_dict_.update({j+1: self.s_active_columns[1]})
                    s_new_y_data[i+1].append(self.data_1_active[self.s_active_columns[1][j]])
                self.s_active_columns = new_dict_

        self.y_data = new_y_data
        self.s_y_data = s_new_y_data
        self.x_data[1] = arange(len(self.y_data[1][0]))
        x_data_ = self.x_data[1]
        self.gui.plot_panel.current_subplot = 1
        self.gui.plot_panel.new_fig()
        for i in range(self.num_subplots):

            #titles
            if len(self.gui.plot_panel.titles) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.titles):
                    self.gui.plot_panel.titles.append(f"Plot {i+1}")
            #y labels
            if len(self.gui.plot_panel.y_labels) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.y_labels):
                    self.gui.plot_panel.y_labels.append(f"Y-axis")

            #colours
            if len(self.gui.plot_panel.colours) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.colours):
                    self.gui.plot_panel.colours.append(["tab:blue", "tab:orange"])
            if len(self.gui.plot_panel.colours[i]) < len(self.y_data[i+1]):
                for j in range(len(self.gui.plot_panel.colours[i]),len(self.y_data[i+1])):
                    self.gui.plot_panel.colours[i][j].append("tab:green")

            #2nd axis colours
            if len(self.gui.plot_panel.s_colours) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.s_colours):
                    self.gui.plot_panel.s_colours.append(["tab:red"])
            if len(self.gui.plot_panel.s_colours[i]) < len(self.s_y_data[i+1]):
                for j in range(len(self.gui.plot_panel.s_colours[i]),len(self.s_y_data[i+1])):
                    self.gui.plot_panel.s_colours[i].append("tab:green")

            #2nd axis y labels
            if len(self.gui.plot_panel.s_y_labels) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.s_y_labels):
                    self.gui.plot_panel.s_y_labels.append(f"2nd Y-axis")

            #x labels
            if len(self.gui.plot_panel.x_labels) < self.num_subplots:
                if i > 0 and i >= len(self.gui.plot_panel.x_labels):
                    self.gui.plot_panel.x_labels.append(f"X-axis")

            self.plot_type[i+1] = self.gui.plot_panel.call_plot 
            #ydata
            if i+1 not in self.y_data:
                self.y_data[i+1] = []
                for item in self.y_data[1]:
                    self.y_data[i+1].append(item)
            #s ydata
            if i+1 not in self.s_y_data:
                self.s_y_data[i+1] = []
                for item in self.s_y_data[1]:
                    self.s_y_data[i+1].append(item)

            self.x_data[i+1] = x_data_
            self.gui.plot_panel.redraw_plot()
            self.gui.plot_panel.current_subplot = self.gui.plot_panel.current_subplot + 1
            self.populate_ydata_input(i+1)
            if self.gui.s_axis[i] == True:
                self.populate_ydata_input(i+1, True)
        self.gui.plot_panel.current_subplot = 1      

    def plot_button(self, subplot):
        """
        todo
        """
        self.gui.plot_panel.current_subplot = subplot
        self.plot_type[subplot] = self.gui.plot_panel.call_plot
        self.plot_type_menu[subplot][2].configure(relief="sunken")
        self.plot_type_menu[subplot][3].configure(relief="raised")
        self.plot_type_menu[subplot][4].configure(relief="raised")
        self.gui.plot_panel.redraw_plot()
        self.gui.plot_panel.current_subplot = 1

    def bar_button(self, subplot):
        """
        todo
        """
        self.gui.plot_panel.current_subplot = subplot
        self.plot_type[subplot] = self.gui.plot_panel.call_bar
        self.plot_type_menu[subplot][2].configure(relief="raised")
        self.plot_type_menu[subplot][3].configure(relief="sunken")
        self.plot_type_menu[subplot][4].configure(relief="raised")
        self.gui.plot_panel.redraw_plot()
        self.gui.plot_panel.current_subplot = 1

    def scatter_button(self, subplot):
        """
        todo
        """
        self.gui.plot_panel.current_subplot = subplot
        self.plot_type[subplot] = self.gui.plot_panel.call_scatter
        self.plot_type_menu[subplot][2].configure(relief="raised")
        self.plot_type_menu[subplot][3].configure(relief="raised")
        self.plot_type_menu[subplot][4].configure(relief="sunken")
        self.gui.plot_panel.redraw_plot()
        self.gui.plot_panel.current_subplot = 1

    def on_mouse_wheel(self, event):
        """
        todo
        """
        if event.delta:
            # Windows and macOS
            self.settings_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            # Linux scroll up
            self.settings_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            # Linux scroll down
            self.settings_canvas.yview_scroll(1, "units")

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
        self.date_from_date.delete(0,self.from_len)
        self.date_to_date.delete(0,self.to_len)
        date_range = self.gui.date_selector.active_range
        self.date_from_date.insert(0,date_range[0])
        self.date_to_date.insert(0,date_range[1])

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
        self.from_len = len(date_from_selection)
        self.gui.date_selector.selection = None
        self.gui.date_selector.selection_callback = None
        self.gui.date_selector.change_active_range(date_from=date_from_selection, s="F")
        self.redraw_settings()


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
        self.to_len = len(date_to_selection)
        self.gui.date_selector.selection = None
        self.gui.date_selector.selection_callback = None
        self.gui.date_selector.change_active_range(date_to=date_to_selection, s="T")
        self.redraw_settings()
