from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import json
import os
import ast

class RestaurantApplication(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.setup_window()
        #self.withdraw()
        #self.security_login()

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
            'Select an item from the right panel and press the Add button to add the item in '\
                + 'your order. Your orders will appear on the left panel.\nTo cancel an order, '\
                    + 'select the order from the left panel and click the Remove button. Press the'\
                        + ' Proceed button to confirm your order.'
        self.listbox_header1 = ['Item', 'Price']
        self.listbox_header2 = ['','Item', 'Subtotal']
        self.total_cost = 0
        self.discount_price = None
        self.discount_str = ''
        self.cash_tendered = 0
        self.change = 0
        self.all_items = ''

    def setup_window(self):
        self.resizable(width=False, height=False)
        self.geometry('900x375')
        self.title('Restaurant Point of Sale System')

        # Set Initial Values
        self.initial_values()

        # Create Frame Widgets
        self.main_frame = Frame(self)
        self.button_frame = Frame(self.main_frame)

        # Create Label Widgets
        self.label_header = Label(self.main_frame, text=self.restaurant_name, font=("Helvetica",30))
        self.label_header.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.label_description = Label(self.main_frame, font=("Helvetica",14), anchor=W, justify=LEFT,\
            text=self.description)
        self.label_description.place(relx=0.5, rely=0.28, anchor=CENTER)

        # Create Listbox Widgets
        self.listbox1 = ttk.Treeview(columns=self.listbox_header1, show="headings")
        vsb1 = ttk.Scrollbar(orient="vertical", command=self.listbox1.yview)
        self.listbox1.configure(yscrollcommand=vsb1.set)
        self.listbox2 = ttk.Treeview(columns=self.listbox_header2, show="headings")
        vsb2 = ttk.Scrollbar(orient="vertical", command=self.listbox2.yview)
        self.listbox2.configure(yscrollcommand=vsb2.set)

        # Create Button Widgets
        self.add_button = Button(self.button_frame, text='Add - >', width=10, command= lambda: self.add_item())
        self.remove_button = Button(self.button_frame, text='< - Remove', width=10, command= lambda: self.remove_item())
        self.proceed_button = Button(self.button_frame, text='Proceed', width=10, command= lambda: self.proceed_items())

        # Display the Widgets
        self.add_button.place(anchor=CENTER,relx=0.5,rely=0.1)
        self.remove_button.place(anchor=CENTER,relx=0.5,rely=0.45)
        self.proceed_button.place(anchor=CENTER,relx=0.5,rely=0.8)
        self.listbox1.place(height=225, width=325, rely=0.4)
        self.listbox2.place(height=225, width=450, rely=0.4, relx=0.5)
        self.button_frame.place(height=225, width=126, rely=0.4, relx=0.36)
        self.main_frame.place(height=375, width=900)

        self.load_initial_listboxes()

    def load_initial_listboxes(self):
        # Read from text file
        item_file = open('items.txt', 'r')
        item_contents = item_file.read()
        self.item_dict = ast.literal_eval(item_contents)
        item_file.close()

        self.listbox1.heading(self.listbox_header1[0], text=self.listbox_header1[0])
        self.listbox1.column(self.listbox_header1[0], minwidth=175, width=200)
        self.listbox1.heading(self.listbox_header1[1], text=self.listbox_header1[1])
        self.listbox1.column(self.listbox_header1[1], minwidth=100, width=100)

        self.listbox2.heading(self.listbox_header2[0], text=self.listbox_header2[0])
        self.listbox2.column(self.listbox_header2[0], minwidth=50, width=50)
        self.listbox2.heading(self.listbox_header2[1], text=self.listbox_header2[1])
        self.listbox2.column(self.listbox_header2[1], minwidth=175, width=250)
        self.listbox2.heading(self.listbox_header2[2], text=self.listbox_header2[2])
        self.listbox2.column(self.listbox_header2[2], minwidth=100, width=100)

        for item in self.item_dict:
            self.listbox1.insert('', 'end', values=(item, ("PHP " + str(self.item_dict[item]) + ".00")))
   
    def add_item(self):
        selected_item = self.listbox1.focus()

        if selected_item == "":
            messagebox.showerror("Add Item", "Please select an item from the left panel.")
        else:
            quantity = simpledialog.askinteger("Add Item", "Enter quantity (1 to 99):",
                                minvalue=1, maxvalue=99)
            if quantity is None:
                pass
            elif quantity < 1:
                messagebox.showwarning("Too small","The allowed minimum value is 1. Please try again.")
            elif quantity > 99:
                messagebox.showwarning("Too large","The allowed maximum value is 99. Please try again.")
            else:
                subtotal_str = self.listbox1.item(selected_item)["values"][1]
                subtotal_int = int(subtotal_str[4:-3])
                self.listbox2.insert('', 'end', values =(str(quantity) +' pc(s)', self.listbox1.item(selected_item)["values"][0], ("PHP " + str(subtotal_int * quantity) + ".00")))
        
    def remove_item(self):
        selected_item = self.listbox2.focus()

        if selected_item == "":
            messagebox.showerror("Remove Item", "Please select an item from the right panel.")
        else:
            self.listbox2.delete(selected_item)

    def proceed_items(self):
        item_count = len(self.listbox2.get_children())

        if item_count == 0:
            messagebox.showerror("Confirm Order", "No orders taken yet. Please take at least one order")
        else:
            answer = messagebox.askyesno("Confirm Order", "Confirm Order?")
            if answer == True:
                self.discount_options()

    def get_total_cost(self, item=""):
        children = self.listbox2.get_children(item)
        for child in children:
            children += self.get_total_cost(child)
            item_cost_str = self.listbox2.item(child)["values"][2]
            item_cost_int = int(item_cost_str[4:-3])
            self.total_cost += item_cost_int

        return children

    def get_all_items(self, item=""):
        children = self.listbox2.get_children(item)
        for child in children:
            children += self.get_total_cost(child)
            item_str1 = self.listbox2.item(child)["values"][0]
            item_str2 = self.listbox2.item(child)["values"][1]
            item_str3 = self.listbox2.item(child)["values"][2]

            self.all_items += item_str1 + ' ' + item_str2 + ' ' + item_str3 + '\n'

        return children

    def discount_options(self):
        self.get_total_cost()
        
        self.discount_choice = simpledialog.askinteger("Discount", "Total cost is PHP " + str(self.total_cost) + '.00\n\nPlease enter which discount code applies:\n[0] None\n[1] Senior (20%)\n[2] Premium Membership (30%)',
                                minvalue=0, maxvalue=2)

        if self.discount_choice is None:
            pass
        elif self.discount_choice < 0:
            messagebox.showwarning("Too small","The allowed minimum value is 0. Please try again.")
        elif self.discount_choice > 2:
            messagebox.showwarning("Too large","The allowed maximum value is 2. Please try again.")
        else:
            if self.discount_choice == 1:
                self.discount_price = self.total_cost * 0.8
                self.discount_str = 'Senior (20%)'
            elif self.discount_choice == 2:
                self.discount_price = self.total_cost * 0.7
                self.discount_str = 'Premium Membership (30%)'
            else:
                self.discount_str = 'None'

            self.payment_prompt()

    def payment_prompt(self):
        if self.discount_price == None:
            payment_needed = self.total_cost
        else:
            payment_needed = self.discount_price

        payment_needed = format(payment_needed, '.2f')

        self.cash_tendered = simpledialog.askfloat("Payment", "You need to pay PHP " + str(payment_needed) + '\n\nPlease enter your payment',
                            minvalue=float(payment_needed))

        if self.cash_tendered is None:
            messagebox.showerror("Error","No payment was given! You need to pay PHP " + str(payment_needed))
            self.payment_prompt()
        elif self.cash_tendered < float(payment_needed):
            messagebox.showerror("Error","Payment is insufficient! You need to pay PHP " + str(payment_needed))
        else:
            self.display_receipt()
        
    def display_receipt(self):
        if self.discount_price == None:
            self.change = self.cash_tendered - self.total_cost
        else:
            self.change = self.cash_tendered - self.discount_price
            self.discount_price = format(self.discount_price, '.2f')
        self.get_all_items()
        self.cash_tendered = format(self.cash_tendered, '.2f')
        self.change = format(self.change, '.2f')

        print_lines = ''
        for i in range(50):
            print_lines += '-' 

        receipt_message = self.restaurant_name + '\n' + print_lines + '\n' + self.all_items + print_lines + '\nTotal Cost: PHP ' + str(format(self.total_cost, '.2f')) + '\nDiscount: ' + self.discount_str

        if self.discount_choice != 0:
            receipt_message += '\nDiscounted Price: PHP ' + str(self.discount_price)
        
        receipt_message += '\nCash Tendered: PHP ' + str(self.cash_tendered) + '\nChange: PHP ' + str(self.change) + '\n' + print_lines + '\nThank you for using this facility!\nCome again!'

        response = messagebox.showinfo("Receipt", receipt_message)

        if response == 'ok':
            yesorno_response = messagebox.askyesno("Save Receipt", "Do you want to save the receipt?")
            if yesorno_response == True:
                f = open("receipt.txt", "w")
                f.write(receipt_message)
                f.close()
            
            self.order_again()

    def order_again(self):
        yesorno_response = messagebox.askyesno("Take Order", "Thank you for your order!\n\nDo you want to use this facility again? Press No to exit this program.")
        if yesorno_response == True:
            self.listbox2.delete(*self.listbox2.get_children())
            self.initial_values()
        else: 
            self.quit()

# class MyDialog(simpledialog.Dialog):

#     def body(self, master):

#         Label(master, text="First:").grid(row=0)
#         Label(master, text="Second:").grid(row=1)

#         self.e1 = Entry(master)
#         self.e2 = Entry(master)

#         self.e1.grid(row=0, column=1)
#         self.e2.grid(row=1, column=1)
#         return self.e1 # initial focus

#     def apply(self):
#         first = self.e1.get()
#         second = self.e2.get()
#         print (first, second)

app = RestaurantApplication()
app.mainloop()


# Clear entire treeview
# tree.delete(*tree.get_children())