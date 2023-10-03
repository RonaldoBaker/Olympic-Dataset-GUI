# File: athlete_dataset.py
# Author: Ronaldo R Baker
# Date: Last modified 03 OCT 2023
# Description:
# This application uses a public dataset from Kaggle of Olympic Athletes.
# You are able to filter the data according to five different categories,
# then view that data in a table, and save either data formats.
# Every time you press the filter button on the Filter page, the 'update' button
# on the Table page must be used to update the current information showing on 
# the treeview widget, and the labels at the top which show the current chosen filters.
#
# Every time the 'filter' button is pressed it filters the original dataset, 
# not the data that was the result of the last filtering
#
# NOTE:
# There is a gap in the home page below the introductory text to include an image
# In the HomePage class, create_widgets method, there is a block of code written to 
# input an image, however, this has not worked in this application, will need to be worked on. 


import sys
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# CONSTANTS #
BUTTON_STYLE = ("Bahnschrift", 18, "bold")
HEADING_STYLE = ("Bahnschrift", 18, "normal")
FILTER_STYLE = ("Bahnschrift", 15, "normal")
RICH_BLACK = "#030C11"
GHOST_WHITE = "#fffaff"
FRENCH_GREY = "#c9c9cf"
PLATINUM = "#dfdfe2"
SKY_BLUE = "#00b8f5"
DATASET = pd.read_csv("athlete_events_shortened.csv")

# VARIABLES #
filtered_dataset = pd.DataFrame()
current_filters = ""
updated_dataset = False


# FUNCTIONS #
def save_file():
    global filtered_dataset
    filtered_dataset.to_csv("filtered_dataset.csv", index=False)
    messagebox.showinfo("Data saved", "The current filtered dataset has been saved.")


def update():
    global filtered_dataset
    global current_filters
    global updated_dataset
    current_frame = app.frame
    # The treeview and label widgets are only updated if the user has
    # filtered the dataset again
    if updated_dataset == True:
        current_frame.filter_info.config(text="")
        current_frame.filter_info.config(text="Applied filters: " + current_filters)
        current_filters = ""
        for item in current_frame.table.get_children():
            current_frame.table.delete(item)
        for i in range(len(filtered_dataset)):
            current_frame.table.insert(parent = "", index = 1, values = (filtered_dataset.iloc[i, 1], filtered_dataset.iloc[i, 2], 
                filtered_dataset.iloc[i, 3], filtered_dataset.iloc[i, 4], filtered_dataset.iloc[i, 5],))
    updated_dataset = False


def sub_filter(df, filter, option):
    sub_df = df[(df[filter] == option)]
    return sub_df


def filter_dataset():
    global DATASET
    global filtered_dataset
    global current_filters
    global updated_dataset
    filtered_dataset = DATASET.copy()
    errors = ""
    entered_filters = 0
    successful_filters = 0
    # Retrieve current frame as object to access Entry values from the FilterPage
    current_frame = app.frame

    input_sex = current_frame.sex_entry.get().strip().upper()
    input_age = current_frame.age_entry.get().strip()
    input_country = current_frame.country_entry.get().strip()
    input_year = current_frame.year_entry.get().strip()
    input_sport = current_frame.sport_entry.get().strip()

    if input_sex != "":
        entered_filters += 1
        if input_sex == "F" or input_sex == "M":
            filtered_dataset = sub_filter(filtered_dataset, "Sex", input_sex)
            current_filters += f"Sex: {input_sex}, "
            successful_filters += 1
        else:
            errors += "Input for sex must be 'M' or 'F'\n"

    if input_age != "":
        entered_filters += 1
        try:
            input_age = int(input_age)
        except ValueError:
            errors += "Input for age must be a number\n"
        else:
            if input_age > 0:
                if sub_filter(filtered_dataset, "Age", input_age).size > 0:
                    filtered_dataset = sub_filter(filtered_dataset, "Age", input_age)
                    current_filters += f"Age: {input_age}, "
                    successful_filters += 1
                else:
                    errors += f"There are no records matching {input_age}\n"
            else:
                errors += "Input age must be greater than 0\n"

    if input_country != "":
        entered_filters += 1
        if any(char.isdigit() for char in input_country) == False:
            if sub_filter(filtered_dataset, "Team", input_country).size > 0:
                filtered_dataset = sub_filter(filtered_dataset, "Team", input_country)
                current_filters += f"Country: {input_country}, "
                successful_filters += 1
            else:
                errors += f"There are no records matching {input_country}\n"
        else:
            errors += "Input for country cannot contain numbers\n"

    if input_year != "":
        entered_filters += 1
        try:
            input_year = int(input_year)
        except ValueError:
            errors += "Input for year must only contain numbers\n"
        else:
            if input_year > 0:
                if sub_filter(filtered_dataset, "Year", input_year).size > 0:
                    filtered_dataset = sub_filter(filtered_dataset, "Year", input_year)
                    current_filters += f"Year: {input_year}, "
                    successful_filters += 1
                else:
                    errors += f"There are no records matching {input_year}\n"
            else:
                errors += "Input year must be greater than 0\n"

    if input_sport != "":
        entered_filters += 1
        if any(char.isdigit() for char in input_sport) == False:
            if sub_filter(filtered_dataset, "Sport", input_sport).size > 0:
                filtered_dataset = sub_filter(filtered_dataset, "Sport", input_sport)
                current_filters += f"Sport: {input_sport}"
                successful_filters += 1
            else:
                errors += f"There are no records matching {input_sport}\n"
        else:
            errors += "Input for sport cannot contain numbers\n"

    updated_dataset = True
    if len(errors) > 0:
        messagebox.showwarning("Error", (errors + f"\n{successful_filters}/{entered_filters} filters were applied successfully"))
    else:
        messagebox.showinfo("Filtered", 
            f"Data has been successfully filtered\n{successful_filters}/{entered_filters} filters were applied successfully")


# CLASSES (USER INTERFACE) #
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Olympics Database")
        self.geometry("700x600")
        self.minsize(700, 600)

        # Frame for the options bar
        self.option = OptionsBar(self, self, SKY_BLUE)
        self.test_value = 1

        # Container for each frame (page)
        container = tk.Frame(self, background=PLATINUM)
        container.place(x=0, rely=0.15, relwidth=1, relheight=0.85)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of frames
        self.frames = {}
        for F in (HomePage, FilterPage, TablePage):
            self.frame = F(container)
            self.frames[F] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage, self.option.home_indicate)

    def hide_all_indicators(self):
        self.option.home_indicate.config(bg=SKY_BLUE)
        self.option.filter_indicate.config(bg=SKY_BLUE)
        self.option.table_indicate.config(bg=SKY_BLUE)

    def show_indicator(self, label):
        self.hide_all_indicators()
        label.config(bg=RICH_BLACK)

    def show_frame(self, container, label):
        self.show_indicator(label)
        self.frame = self.frames[container]
        # Raising the current frame to the top
        self.frame.tkraise()


class OptionsBar(tk.Frame):
    def __init__(self, parent, controller, colour):
        super().__init__(master=parent, background=colour)
        self.place(x=0, y=0, relwidth=1, relheight=0.15)
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.create_widgets(controller)

    def create_widgets(self, controller):
        home_button = tk.Button(
            self,
            text="Home",
            bd=0,
            font=BUTTON_STYLE,
            background=SKY_BLUE,
            command=lambda: controller.show_frame(HomePage, self.home_indicate),
        )
        filter_button = tk.Button(
            self,
            text="Filter",
            bd=0,
            font=BUTTON_STYLE,
            background=SKY_BLUE,
            command=lambda: controller.show_frame(FilterPage, self.filter_indicate),
        )
        table_button = tk.Button(
            self,
            text="Table",
            bd=0,
            font=BUTTON_STYLE,
            background=SKY_BLUE,
            command=lambda: controller.show_frame(TablePage, self.table_indicate),
        )

        self.home_indicate = tk.Label(self, text="", background=SKY_BLUE)
        self.home_indicate.place(x=84, y=65, width=64, height=5)

        self.filter_indicate = tk.Label(self, text="", background=SKY_BLUE)
        self.filter_indicate.place(x=319, y=65, width=60, height=5)

        self.table_indicate = tk.Label(self, text="", background=SKY_BLUE)
        self.table_indicate.place(x=553, y=65, width=60, height=5)

        home_button.grid(row=0, column=0)
        filter_button.grid(row=0, column=1)
        table_button.grid(row=0, column=2)


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, background=PLATINUM)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=1, uniform="a")
        self.create_widgets()
        self.home_value = 22

    def create_widgets(self):

        home_page_info = "This application utilises a public domain dataset '120 Years of\nOlympics History: Athletes and Results' provided by Kaggle,\na data science competition platform with access to open datasets.\n\nBy using the following 'Filter', 'Table' and 'Graph' tabs you can\nfilter the data by five categories and display that data in a table."
        
        #canvas = tk.Canvas(master = self, width = 700, height = 255, highlightthickness = 0)
        #bg = tk.PhotoImage(file = "olympic_logo_reduced.png")
        #canvas.create_image(0, 0, image = bg)
        #canvas.grid(row = 1, column = 0)

        info_text = tk.Label(
            self,
            text=home_page_info,
            font=("Bahnschrift", 17, "normal"),
            justify="left",
            padx=10,
            pady=10,
            background=PLATINUM,
        )
        info_text.grid(row=0, column=0, sticky="nw")


class FilterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, background=PLATINUM)
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.grid_columnconfigure(0, weight=1, uniform="b")
        self.grid_columnconfigure(1, weight=1, uniform="b")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(
            self,
            text="You may filter the dataset according to the\nfollowing five categories: ",
            font=HEADING_STYLE,
            justify="left",
            padx=10,
            pady=15,
            background=PLATINUM,
        )
        sex_label = tk.Label(self, text="Sex (M or F): ", font=FILTER_STYLE, background=PLATINUM)
        age_label = tk.Label(self, text="Age: ", font=FILTER_STYLE, background=PLATINUM)
        country_label = tk.Label(self, text="Country: ", font=FILTER_STYLE, background=PLATINUM)
        year_label = tk.Label(self, text="Year: ", font=FILTER_STYLE, background=PLATINUM)
        sport_label = tk.Label(self, text="Sport: ", font=FILTER_STYLE, background=PLATINUM)
        filter_button = tk.Button(self, text="FILTER", font=FILTER_STYLE, background=PLATINUM, command=filter_dataset)
        self.sex_entry = tk.Entry(self)
        self.age_entry = tk.Entry(self)
        self.country_entry = tk.Entry(self)
        self.year_entry = tk.Entry(self)
        self.sport_entry = tk.Entry(self)

        label.grid(row=0, column=0, columnspan=2, sticky="nw")
        sex_label.grid(row=1, column=0, sticky="e")
        age_label.grid(row=2, column=0, sticky="e")
        country_label.grid(row=3, column=0, sticky="e")
        year_label.grid(row=4, column=0, sticky="e")
        sport_label.grid(row=5, column=0, sticky="e")

        self.sex_entry.grid(row=1, column=1, sticky="w")
        self.age_entry.grid(row=2, column=1, sticky="w")
        self.country_entry.grid(row=3, column=1, sticky="w")
        self.year_entry.grid(row=4, column=1, sticky="w")
        self.sport_entry.grid(row=5, column=1, sticky="w")

        filter_button.grid(row=6, column=0, columnspan=2)


class TablePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, background=PLATINUM)
        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=9, uniform="a")
        self.grid_rowconfigure(2, weight=1, uniform="a")
        self.create_place_widgets()

    def create_place_widgets(self):
        self.filter_info = tk.Label(self, text="Applied filters: ", font=("Bahnschrift", 12, "normal"), background=PLATINUM)
        self.filter_info.grid(row=0, column=0, columnspan=2)

        save_button = tk.Button(self, text="SAVE", font=("Bahnschrift", 12, "normal"), background=PLATINUM, command=save_file)
        save_button.grid(row=2, column=1, sticky="nsew")

        update_button = tk.Button(self, text="UPDATE", font=("Bahnschrift", 12, "normal"), background=PLATINUM, command=update)
        update_button.grid(row=2, column=0, sticky="nsew")

        self.table = ttk.Treeview(self, columns=("c1", "c2", "c3", "c4", "c5"), show="headings")
        self.table.heading("c1", text="Sex")
        self.table.column("c1", stretch=False, width=110)
        self.table.heading("c2", text="Age")
        self.table.column("c2", stretch=False, width=110)
        self.table.heading("c3", text="Team")
        self.table.column("c3", stretch=False, width=160)
        self.table.heading("c4", text="Year")
        self.table.column("c4", stretch=False, width=160)
        self.table.heading("c5", text="Sport")
        self.table.column("c5", stretch=False, width=160)
        self.table.grid(row=1, column=0, columnspan=2, sticky="nsew")


# MAIN APPLICATION #

app = Application()
app.mainloop()
