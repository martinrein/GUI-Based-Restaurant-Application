from tkinter import *
from tkinter import messagebox
import json
import os
import ast

class RestaurantApplication(object):

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()


restaurant_name = 'Wings and Ponchos: Mexican-Western Fusion'

if __name__ == '__main__':
    root = Tk()
    root.title("Restaurant Point of Sale System")
    listbox = RestaurantApplication()
    root.mainloop()