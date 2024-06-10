"""
todo
"""
from tkinter import Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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
        self.gui.settings_panel.plot_type[self.current_subplot]()
        self.ax.set_title('Sample Matplotlib Graph')
        self.ax.set_xlabel('X-axis Label')
        self.ax.set_ylabel('Y-axis Label')

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
        self.ax.set_title('Sample Matplotlib Graph')
        self.ax.set_xlabel('X-axis Label')
        self.ax.set_ylabel('Y-axis Label')

    def call_plot(self):
        """
        todo
        """
        for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
            self.ax.plot(self.gui.settings_panel.x_data[self.current_subplot], 
                         self.gui.settings_panel.y_data[self.current_subplot][i])

    def call_bar(self):
        """
        todo
        """
        for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
            self.ax.bar(self.gui.settings_panel.x_data[self.current_subplot], 
                        self.gui.settings_panel.y_data[self.current_subplot][i])

    def call_scatter(self):
        """
        todo
        """
        for i in range(len(self.gui.settings_panel.y_data[self.current_subplot])):
            self.ax.scatter(self.gui.settings_panel.x_data[self.current_subplot], 
            self.gui.settings_panel.y_data[self.current_subplot][i])