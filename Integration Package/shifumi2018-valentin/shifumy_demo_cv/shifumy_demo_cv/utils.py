# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""


def get_screen_dimension():
    import tkinter as tk
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return height, width