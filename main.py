from tkinter import *
from tkinter import messagebox
import json
import os
import ast

class RestaurantApplication(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.resizable(width=False, height=False)
        self.geometry('900x375')
        self.title('Restaurant Point of Sale System')

        # Create List variables
        self.list_var1 = StringVar()
        self.list_var2 = StringVar()

        # Set Initial Values
        self.initial_values()

        # Create Frame Widgets
        self.main_frame = Frame(self)#, relief=RIDGE, bd=10)
        self.button_frame = Frame(self.main_frame)

        # Label Widgets
        self.label_header = Label(self.main_frame, text=self.restaurant_name, font=("bold",30))
        self.label_header.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.label_description = Label(self.main_frame, font=("bold",14), anchor=W, justify=LEFT,\
            text=self.description)
        self.label_description.place(relx=0.5, rely=0.28, anchor=CENTER)

        self.listbox1 = Listbox(self.main_frame, listvariable=self.list_var1, selectmode='single')
        self.listbox2 = Listbox(self.main_frame, listvariable=self.list_var2, selectmode='single')

        self.add_button = Button(self.button_frame, text='Add - >', width=10)
        self.remove_button = Button(self.button_frame, text='< - Remove', width=10)
        self.proceed_button = Button(self.button_frame, text='Proceed', width=10)#, command=self.move_to_left)

        # packing
        self.add_button.place(anchor=CENTER,relx=0.5,rely=0.1)
        self.remove_button.place(anchor=CENTER,relx=0.5,rely=0.45)
        self.proceed_button.place(anchor=CENTER,relx=0.5,rely=0.8)

        self.listbox1.place(height=225, width=325, rely=0.4)
        self.listbox2.place(height=225, width=450, rely=0.4, relx=0.5)

        self.button_frame.place(height=225, width=126, rely=0.4, relx=0.36)
        self.main_frame.place(height=375, width=900)

    def initial_values(self):
        self.restaurant_name = 'Wings and Ponchos: Mexican-Western Fusion'
        self.description = 'Welcome to ' + self.restaurant_name + '!\n\n' + \
            'Select an item from the right panel and press the Add button to add the item in'\
                + 'your order. Your orders will appear on the left panel.\nTo cancel an order, '\
                    + 'select the order from the left panel and click the Remove button. Press the'\
                        + 'Proceed button to confirm your order.'
        self.get_items()

    def get_items(self):
        item_file = open('items.txt', 'r')
        item_contents = item_file.read()
        self.item_list = ast.literal_eval(item_contents)
        item_file.close()

app = RestaurantApplication()
app.mainloop()
