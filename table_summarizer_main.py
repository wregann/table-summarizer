import tkinter as tk
from turtle import back, bgcolor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import ts_config as cf

class UpperRightStats(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.stats_labels = None
    def add_onevar_stats(self, data):
        if self.stats_labels != None:
            print("Previous Statistics Not Cleared")

        # Summary Statistics
        self.stats_labels = [
        tk.Label(self.parent, font = cf.h2_font, text="Summary Statistics", bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Mean: " + str(np.mean(data)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Median: " + str(np.median(data)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Std: " + str(np.std(data)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Min: " + str(np.min(data)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Max: " + str(np.max(data)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Q1: " + str(np.quantile(data, 0.25)), bg=cf.bg_color),
        tk.Label(self.parent, font = cf.body_font, text="Q3: " + str(np.quantile(data, 0.75)), bg=cf.bg_color)
        ]
        for i, label in enumerate(self.stats_labels):
            label.grid(row=i + 1, column=2, sticky="W")

    def clear_stats_labels(self):
        if self.stats_labels is not None:
            for label in self.stats_labels:
                try:
                    label.destroy()
                except Exception as e:
                    print(e)
                    print("Error in removing label")
        self.stats_labels = None


class BottomGraphs(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
    def add_onevar_graphs(self, data):
        fig = plt.figure(figsize = (8, 4), 
                dpi = 100, facecolor=cf.bg_color)
        gs = fig.add_gridspec(1,10)

        # Add Histogram
        histogram_ax = fig.add_subplot(gs[0,0:7])
        histogram_ax.hist(data)
        histogram_ax.set_title("Histogram")
        histogram_ax.set_facecolor(cf.bg_color)
        whisker_ax = fig.add_subplot(gs[0,8:11])
        whisker_ax.boxplot(data)
        whisker_ax.set_title("Whisker")
        whisker_ax.set_facecolor(cf.bg_color)

        # plt figure
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=20, column=0, columnspan=3, sticky="W") # row 20 was arbitrary

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().delete("all")
        self.canvas = None


class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.data = None
        self.parent.geometry(cf.window_geom)
        self.parent.configure(background=cf.bg_color)
        self.parent.title("Table Summarizer")
        self.selected_column = tk.StringVar(self.parent)
        self.select_options = [""]
        self.selected_column.set(self.select_options[0])
        # Create Stats Page
        self.upper_right_stats = UpperRightStats(self.parent)
        self.bottom_graphs = BottomGraphs(self.parent)

        tk.Label(self.parent, font = cf.h1_font, text="Table Summarizer", bg=cf.bg_color).grid(
            row=0, column=0, columnspan=3)
        tk.Button(self.parent, text='Find Table', font=cf.body_font, command=lambda : self.get_data_file()).grid(row=2, column=0)
        self.option_menu = tk.OptionMenu(self.parent, self.selected_column, *self.select_options, 
            command = lambda : self.change_column()).grid(row=4, column=0)

        #x = np.random.normal(loc=0, scale=25, size=(500))
        #self.upper_right_stats.add_onevar_stats(x)
        #self.bottom_graphs.add_onevar_graphs(x)

    def change_column(self):
        self.bottom_graphs.clear_canvas()
        self.upper_right_stats.clear_stats_labels()
        if self.selected_column.get() != "" and self.data is not None:
            self.bottom_graphs.add_onevar_graphs(self.data[self.selected_column.get()])
            self.upper_right_stats.add_onevar_stats(self.data[self.selected_column.get()])
    
    def get_data_file(self):
        x_frame = pd.DataFrame(np.random.normal(0,100,size=(213, 4)), columns=list('ABCD'))
        self.data = x_frame
        self.select_options = list(self.data.columns)
        self.selected_column.set(self.select_options[0])
        if self.option_menu is not None:
            self.option_menu.destroy()
        self.option_menu = tk.OptionMenu(self.parent, self.selected_column, *self.select_options, 
            command = lambda q : self.change_column()).grid(row=4, column=0)

if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root)
    root.mainloop()

# Matplotlib Tool Bar
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

