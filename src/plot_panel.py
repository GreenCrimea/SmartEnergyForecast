"""
todo
"""
from tkinter import Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import arange, linspace



class PlotPanel(Frame):
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

        self.current_subplot = 1

        #set plot default
        self.gui.settings_panel.plot_type[self.current_subplot] = self.call_plot
        self.titles = [f'Plot {self.current_subplot}']
        self.y_labels = ["Y-axis"]
        self.s_y_labels = ["2nd Y-axis"]
        self.x_labels = ["X-axis"]
        self.legend = [True]
        self.legend_loc = ["lower right"]
        self.x_ticks = [1]
        self.ylim = [False]
        self.s_ylim = [False]
        self.colours = [["tab:blue", "tab:orange"]]
        self.s_colours = [["tab:red"]]
        self.grid = [False]

        #draw default graph
        self.init_graph()

        # Create a FigureCanvasTkAgg object and attach it to the Tkinter root window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()

        # Get the canvas widget and pack it into the Tkinter window
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    def new_fig(self):
        self.fig = None
        self.fig = Figure(figsize=(5, 4), dpi=70)

    def redraw_plot(self):
        """
        todo
        """
        #remove old frame, canvas and fig
        self.frame.forget()
        self.frame.destroy()
        self.canvas = None

        #draw new frame
        self.frame = Frame(self.main)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.pack_propagate(False)
    
        self.ax = self.fig.add_subplot(
            self.gui.settings_panel.subplot_dimensions[0],
            self.gui.settings_panel.subplot_dimensions[1],
            self.current_subplot
        )
        #ylim
        if self.ylim[self.current_subplot-1] != False:
            lims = self.ylim[self.current_subplot-1]
            self.ax.set_ylim(int(lims[0]), int(lims[1]))

        self.gui.settings_panel.plot_type[self.current_subplot]()
        self.ax.set_title(self.titles[self.current_subplot-1])
        self.ax.set_xlabel(self.x_labels[self.current_subplot-1])
        self.ax.set_ylabel(self.y_labels[self.current_subplot-1])
        self.ax.set_xlim(0,len(self.gui.date_selector.active_dates))
        #xticks
        if self.x_ticks[self.current_subplot-1] == 0:
            labels = []
            for i in linspace(0, len(self.gui.date_selector.active_dates)-1, 5).astype(int):
                labels.append(self.gui.date_selector.active_dates[i])
            self.ax.set_xticks(linspace(1, len(self.gui.date_selector.active_dates), 5),
                                   labels=labels)
        #second_axis
        if self.gui.s_axis[self.current_subplot-1] == True:
            self.ax2 = self.ax.twinx()
            self.gui.settings_panel.plot_type[self.current_subplot](True)
            self.ax2.set_ylabel(self.s_y_labels[self.current_subplot-1])
            if self.s_ylim[self.current_subplot-1] != False:
                lims = self.s_ylim[self.current_subplot-1]
                self.ax2.set_ylim(int(lims[0]), int(lims[1]))
            self.ax.legend(loc=self.legend_loc[self.current_subplot-1])
            self.ax2.legend(loc="lower right")
        else:
            #legend
            if self.legend[self.current_subplot-1] == True:
               self.ax.legend(loc=self.legend_loc[self.current_subplot-1])
        
        #grid
        if self.grid[self.current_subplot-1] == True:
            self.ax.grid(True)


        #self.fig.tight_layout()

        #draw new canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    def init_graph(self):
        """
        todo
        """
        self.fig = Figure(figsize=(5, 4), dpi=70)
        self.ax = self.fig.add_subplot(
            self.gui.settings_panel.subplot_dimensions[0],
            self.gui.settings_panel.subplot_dimensions[1],
            1
        )
        self.gui.settings_panel.plot_type[self.current_subplot]()
        self.ax.set_xlim(0,len(self.gui.date_selector.active_dates))
        self.ax.set_title("Minimum and Maximum Temperatures")
        self.ax.set_xlabel('Days')
        self.ax.set_ylabel('Temperature (c)')
        self.ax.legend()

    def call_plot(self, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            for i in range(len(self.gui.settings_panel.s_y_data[self.current_subplot])):
                self.ax2.plot(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.s_y_data[self.current_subplot][i],
                             color=self.s_colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.s_y_data[self.current_subplot][i].name)
        else:
            for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
                self.ax.plot(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.y_data[self.current_subplot][i],
                             color=self.colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.y_data[self.current_subplot][i].name)

    def call_bar(self, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            for i in range(len(self.gui.settings_panel.s_y_data[self.current_subplot])):
                self.ax2.bar(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.s_y_data[self.current_subplot][i],
                             color=self.s_colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.s_y_data[self.current_subplot][i].name)
        else:
            for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
                self.ax.bar(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.y_data[self.current_subplot][i],
                             color=self.colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.y_data[self.current_subplot][i].name)

    def call_scatter(self, s_axis = False):
        """
        todo
        """
        if s_axis == True:
            for i in range(len(self.gui.settings_panel.s_y_data[self.current_subplot])):
                self.ax2.scatter(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.s_y_data[self.current_subplot][i],
                             color=self.s_colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.s_y_data[self.current_subplot][i].name)
        else:
            for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
                self.ax.scatter(self.gui.settings_panel.x_data[self.current_subplot], 
                             self.gui.settings_panel.y_data[self.current_subplot][i],
                             color=self.colours[self.current_subplot-1][i],
                             label=self.gui.settings_panel.y_data[self.current_subplot][i].name)