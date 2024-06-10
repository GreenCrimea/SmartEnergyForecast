"""
todo
"""
from tkinter import Frame, Label, Entry, Button, messagebox, Canvas, Scrollbar
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

        self.default_graph_settings()
        self.initialize_date_range()
        self.initialize_settings_panel()

    def default_graph_settings(self):
        """
        todo
        """
        self.plot_type = {1: None}

        self.subplot_dimensions = (1,1)
        self.num_subplots = 1

        self.x_data = {1: arange(len(self.gui.dataframe))}

        self.y_data = {1: []}
        self.y_data[1].append(self.data_1_active["Maximum temperature (°C)"])
        self.y_data[1].append(self.data_2_active["Minimum temperature (°C)"])

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

        for i in range(50):
            Label(self.scrollable_frame, text=f"Label {i}").pack()
            Entry(self.scrollable_frame).pack()

    def subplot_button_click(self):
        """
        todo
        """
        self.subplot_dimensions = (int(self.subplot_x_input.get()), int(self.subplot_y_input.get()))
        self.num_subplots = int(self.subplot_x_input.get()) * int(self.subplot_y_input.get())
        self.redraw_settings()
        y_data_ = self.y_data[1]
        x_data_ = self.x_data[1]
        self.gui.plot_panel.current_subplot = 1
        self.gui.plot_panel.new_fig()
        for i in range(self.num_subplots):
            self.plot_type[i+1] = self.gui.plot_panel.call_plot    
            self.y_data[i+1] = y_data_   
            self.x_data[i+1] = x_data_
            self.gui.plot_panel.redraw_plot()
            self.gui.plot_panel.current_subplot = self.gui.plot_panel.current_subplot + 1
        self.gui.plot_panel.current_subplot = 1

    def redraw_settings(self):
        """
        todo
        """
        self.frame.forget()
        self.frame.destroy()

        self.frame = Frame(self.main)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.pack_propagate(False)

        self.initialize_settings_panel()        

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
