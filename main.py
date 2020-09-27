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
        self.label_header = Label(self.main_frame, text=self.restaurant_name, font=("Helvetica",30))
        self.label_header.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.label_description = Label(self.main_frame, font=("Helvetica",14), anchor=W, justify=LEFT,\
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

        self.withdraw()
        self.security_login()

    def security_login(self):
        self.security_window = Toplevel()
        self.security_window.title('Security Login')

        self.bottom_frame = Frame(self.security_window, height=30)

        self.label_username = Label(self.security_window, text="Enter Username:")
        self.label_password = Label(self.security_window, text="Enter Password:")
        self.entry_username = Entry(self.security_window, width=30)
        self.entry_password = Entry(self.security_window, width=30, show="*")
        self.button_ok = Button(self.security_window, text="OK", width=10, command = lambda: self.login_ok())
        self.button_cancel = Button(self.security_window, text="Cancel", width=10, command = lambda: self.login_error())

        self.label_username.pack(anchor=W)
        self.entry_username.pack()
        self.label_password.pack(anchor=W)
        self.entry_password.pack()
        self.bottom_frame.pack(side=BOTTOM)
        self.button_ok.place(anchor=CENTER, relx=0.3, rely=0.9)
        self.button_cancel.place(anchor=CENTER, relx=0.7, rely=0.9)

    def login_ok(self):
        if ((self.entry_username.get() == 'admin') and (self.entry_password.get() == 'lbymf1d')) or \
            ((self.entry_username.get() == 'customer1') and (self.entry_password.get() == 'password1')) or \
                ((self.entry_username.get() == 'customer2') and (self.entry_password.get() == 'password2')):
            self.deiconify()
            self.security_window.destroy()
        else:
            self.login_error()

    def login_error(self):
        response = messagebox.showerror("Error", "Invalid or incorrect password! The program will exit.")
        if response == 'ok':
            self.quit()

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
