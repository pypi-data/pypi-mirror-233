import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sys


class App:
    def __init__(self, root, df):
        self.root = root
        self.x_options = []  # Empty list for X options initially
        self.y_options = []  # Empty list for Y options initially
        self.selected_x = tk.StringVar()
        self.selected_y = tk.StringVar()
        self.create_widgets()
        self.df = df

    def create_widgets(self):
        self.option_frame = ttk.Frame(self.root)
        self.option_frame.pack(padx=10, pady=10)

        self.x_label = ttk.Label(self.option_frame, text="X:")
        self.x_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.x_combobox = ttk.Combobox(self.option_frame, textvariable=
            self.selected_x, values=self.x_options)
        self.x_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.y_label = ttk.Label(self.option_frame, text="Y:")
        self.y_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.y_combobox = ttk.Combobox(self.option_frame, textvariable=
            self.selected_y, values=self.y_options)
        self.y_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.plot_button = ttk.Button(self.option_frame,
                    text="Plot according Iteration", command=self.plot_iter)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.plot_button = ttk.Button(self.option_frame,
                    text="Plot according Sorted X", command=self.plot_sorted_X)
        self.plot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.exit_button = ttk.Button(self.option_frame,
                    text="Exit", command=sys.exit)
        self.exit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    def update_options(self, x_options, y_options):
        self.x_options = x_options
        self.y_options = y_options
        self.x_combobox['values'] = self.x_options
        self.y_combobox['values'] = self.y_options

    def plot_iter(self):

        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        # Get the arrays of values for the selected options
        x_values = self.df[selected_x].values
        y_values = self.df[selected_y].values

        fig, ax = plt.subplots()
        ax.plot(x_values, y_values)
        ax.scatter(x_values, y_values)

        for iteration, x,y in zip(self.df['IterationNumber'],x_values,y_values):
            ax.annotate(iteration, (x, y), textcoords="offset points",
                        xytext=(0, 10), ha='center', va='bottom')

        ax.grid()
        ax.set_xlabel(selected_x)
        ax.set_ylabel(selected_y)
        ax.set_title(f"{selected_x} vs {selected_y}")

        # Avoid scientific notations
        ax.ticklabel_format(useOffset=False, style='plain')

        #window = ImageWindow(self.root, fig, f"{selected_x} vs {selected_y}")
        plt.show()


    def plot_sorted_X(self):

        selected_x = self.selected_x.get()
        selected_y = self.selected_y.get()

        sorted_X_df = self.df.sort_values(by=[selected_x])

        # Get the arrays of values for the selected options
        x_values = sorted_X_df[selected_x].values
        y_values = sorted_X_df[selected_y].values

        fig, ax = plt.subplots()
        ax.plot(x_values, y_values)
        ax.scatter(x_values, y_values)

        for iteration, x,y in zip(sorted_X_df['IterationNumber'],
                                  x_values,y_values):
            ax.annotate(iteration, (x, y), textcoords="offset points",
                        xytext=(0, 10), ha='center', va='bottom')

        ax.grid()
        ax.set_xlabel(selected_x)
        ax.set_ylabel(selected_y)
        ax.set_title(f"{selected_x} vs {selected_y}")

        # Avoid scientific notations
        ax.ticklabel_format(useOffset=False, style='plain')

        #window = ImageWindow(self.root, fig, f"{selected_x} vs {selected_y}")
        plt.show()