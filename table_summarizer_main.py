import tkinter as tk
from turtle import back, bgcolor
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import ts_config as cf

class UpperRightStats(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
    def add_onevar_stats(self, data):
        # Summary Statistics
        tk.Label(self.parent, font = cf.h2_font, text="Summary Statistics").grid(row=1, column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Mean: " + str(np.mean(data))).grid(row=2, column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Median: " + str(np.median(data))).grid(row=3, column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Std: " + str(np.std(data))).grid(row=4,column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Min: " + str(np.min(data))).grid(row=5,column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Max: " + str(np.max(data))).grid(row=6,column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Q1: " + str(np.quantile(data, 0.25))).grid(row=7,column=2, sticky="W")
        tk.Label(self.parent, font = cf.body_font, text="Q3: " + str(np.quantile(data, 0.75))).grid(row=8,column=2, sticky="W")


class BottomGraphs(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
    def add_onevar_graphs(self, data):
        fig = plt.figure(figsize = (7, 4), 
                dpi = 100, facecolor=cf.bg_color)
        gs = fig.add_gridspec(1,3)

        # Add Histogram
        histogram_ax = fig.add_subplot(gs[0,0:2])
        histogram_ax.hist(data)
        histogram_ax.set_title("Histogram")
        histogram_ax.set_facecolor(cf.bg_color)
        whisker_ax = fig.add_subplot(gs[0,2])
        whisker_ax.boxplot(data)
        whisker_ax.set_title("Whisker")
        whisker_ax.set_facecolor(cf.bg_color)

        # plt figure
        canvas = FigureCanvasTkAgg(fig, master=self.parent)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=20, column=0, columnspan=3) # row 20 was arbitrary


class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry(cf.window_geom)
        self.parent.configure(background=cf.bg_color)
        self.parent.title("Table Summarizer")
        tk.Label(root, font = cf.h1_font, text="Table Summarizer").grid(row=0, column=0, columnspan=3)
        tk.Button(root, text='Find Table', font=cf.body_font).grid(row=1, column=0)

        self.upper_right_stats = UpperRightStats(self.parent)
        self.bottom_graphs = BottomGraphs(self.parent)

        x = np.random.normal(loc=0, scale=25, size=(500))
        self.upper_right_stats.add_onevar_stats(x)
        self.bottom_graphs.add_onevar_graphs(x)


if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root)
    root.mainloop()

# Matplotlib Tool Bar
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

