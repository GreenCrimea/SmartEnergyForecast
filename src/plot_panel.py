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

        self.sample()

        # Create a FigureCanvasTkAgg object and attach it to the Tkinter root window
        canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas.draw()

        # Get the canvas widget and pack it into the Tkinter window
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    def sample(self):
        # Create a sample Matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=70)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.gui.settings_panel.x_data, self.gui.settings_panel.y_data[0])
        self.ax.plot(self.gui.settings_panel.x_data, self.gui.settings_panel.y_data[1])
        self.ax.set_title('Sample Matplotlib Graph')
        self.ax.set_xlabel('X-axis Label')
        self.ax.set_ylabel('Y-axis Label')