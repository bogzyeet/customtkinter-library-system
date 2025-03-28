# *************************************************************************************
# *                                                                                   *
# *                           School Library Management System                        *
# *                                                                                   *
# *                            Author: Nikhil Kumar Jangir                            *
# *                        Contact Email: krunkistic@gmail.com                        *
# *                                                                                   *
# *    This program is the intellectual property of Nikhil Kumar Jangir. Unauthorized *
# *    copying, stealing, or distribution of this program, in whole or in part, is    *
# *    strictly prohibited unless prior written permission is obtained from the       *
# *    author.                                                                        *
# *                                                                                   *
# *    If you have been granted permission to use this program, you are required to   *
# *    give proper credit to the author by including the author's name in your        *
# *    project and acknowledging their contribution.                                  *
# *                                                                                   *
# *    For any queries, permission requests, or to contact the author, please email   *
# *    krunkistic@gmail.com.                                                          *
# *                                                                                   *
# *************************************************************************************


import customtkinter  # pip install customtkinter
import os
import sqlite3
from PIL import Image, ImageTk  # pip install Pillow
from customtkinter import *
from tkinter import ttk
from CTkMessagebox import CTkMessagebox  # pip install CTkMessagebox
from datetime import datetime
import requests
from io import BytesIO

# Connect to the database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Customtkinter -> My Favorite Dark theme
customtkinter.set_default_color_theme("dark-blue")

def format_log_entry(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "Added book" in action:
        action = "📚 " + action
    elif "Deleted book" in action:
        action = "🗑️ " + action
    elif "Borrowed" in action:
        action = "📖 " + action
    elif "Returned" in action:
        action = "📘 " + action
    elif "Searched for" in action:
        action = "🔍 " + action
    elif "logged in" in action.lower():
        action = "👤 " + action
    elif "logged out" in action.lower():
        action = "🚪 " + action
    return f"[{timestamp}] {action}\n"

global file
file = open(os.path.join("resource_files/", "history.txt"), "a+", encoding="utf-8")

class WebImage:
     def __init__(self,url):
          if url.startswith('http'):
               u = requests.get(url)
               self.image = customtkinter.CTkImage(Image.open(BytesIO(u.content)))
          else:
               self.image = customtkinter.CTkImage(Image.open(url))
          
     def get(self):
          return self.image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
            
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
            font=(None, 10),
        )
        style.map("Treeview", background=[("selected", "invalid", "#22559b")])

        style.configure(
            "Treeview.Heading",
            background="#565b5e",
            foreground="white",
            relief="flat",
            font=(None, 13),
        )
        style.map("Treeview.Heading", background=[("active", "invalid", "#3484F0")])

        style.configure(
            "delete.Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
            font=(None, 10),
        )
        style.map("delete.Treeview", background=[("selected", "#22559b")])

        self.title("School Library Management System")
        self.geometry("900x550")
        self.resizable(0, 0)
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "resource_files"
        )

        libimage = Image.open(os.path.join(image_path, "mainlogo.png"))
        libicon = ImageTk.PhotoImage(libimage)
        self.wm_iconbitmap()
        self.iconphoto(True, libicon)
        if self.get_logged() == 0:
            self.show_login_screen()
        else:
            global role
            global avatar
            global username
            username = self.get_loggedusername()
            avatar = self.get_user_avatar(username)
            role = self.get_user_role(username)
            file.write(format_log_entry(f"User '{username}' logged in"))
            self.show_main_app()
            
    def show_login_screen(self):
        
        # load images with light and dark mode image
        loginbg = Image.open("resource_files/deblogin-1.png").resize((1200, 850),Image.LANCZOS)
        loginbgmain = ImageTk.PhotoImage(loginbg)
       
        self.bglbl = customtkinter.CTkLabel(master=self, image=loginbgmain)
        self.bglbl.place(relx=0.5, rely=0.5, anchor='center')
        
        self.frame1=customtkinter.CTkFrame(master=self, width=320, height=360, corner_radius=15, background_corner_colors=("#2048bf","#2048bf","#2048bf","#2048bf"))
        self.frame1.place(relx=0.5, rely=0.5, anchor='center')

        self.l2=customtkinter.CTkLabel(master=self.frame1, text="Log-in to your Account",font=('Century Gothic',20))
        self.l2.place(x=50, y=45)

        self.entry1=customtkinter.CTkEntry(master=self.frame1, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=110)

        self.entry2=customtkinter.CTkEntry(master=self.frame1, width=220, placeholder_text='Password', show="*")
        self.entry2.place(x=50, y=165)

        #Create login button
        self.button1 = customtkinter.CTkButton(master=self.frame1, width=220, text="Login", command=self.login, corner_radius=6)
        self.button1.place(x=50, y=240)
        
    def login(self):
        global username
        username = self.entry1.get()
        password = self.entry2.get()

        # Checking username and password
        cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password))
        account = cursor.fetchone()

        if account:
            self.entry1.delete(0, customtkinter.END)
            self.entry2.delete(0, customtkinter.END)

            # Update login status for future
            cursor.execute(f'UPDATE logged SET loggedin = 1, username = "{username}"')
            conn.commit()
            file.write(format_log_entry(f"User '{username}' logged in"))
            global role
            global avatar
            avatar = self.get_user_avatar(username)
            role = self.get_user_role(username)
            self.show_main_app()
        else:
            CTkMessagebox(title="Login Failed", message="Invalid username or password")
            self.entry1.delete(0, customtkinter.END)
            self.entry2.delete(0, customtkinter.END)
            
        
    def show_main_app(self):
        
        image_path = os.path.join( 
            os.path.dirname(os.path.realpath(__file__)), "resource_files"
        )
        
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        
        self.search_book_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "search_book_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "search_book_light.png")),
            size=(20, 20),
        )
        
        self.add_book_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_book_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_book_light.png")),
            size=(20, 20),
        )
        
        self.delete_book_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "delete_book_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "delete_book_light.png")),
            size=(20, 20),
        )
        
        self.return_book_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "return_book_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "return_book_light.png")),
            size=(20, 20),
        )
        
        self.borrow_book_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "borrow_book_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "borrow_book_light.png")),
            size=(20, 20),
        )
        
        self.log_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "log_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "log_light.png")),
            size=(20, 20),
        )
        
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(10, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
                self.navigation_frame,
                text=f"  Welcome {username}!",
                image=WebImage(avatar).get(),
                compound="left",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.navigation_frame_label.bind("<Enter>", self.on_enter)
        
        self.logout_btncheck = None

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Search Books",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.search_book_image,
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Add Book",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_book_image,
            anchor="w",
            command=self.frame_3_button_event,
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Delete Book",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.delete_book_image,
            anchor="w",
            command=self.frame_4_button_event,
        )
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Return Book",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.return_book_image,
            anchor="w",
            command=self.frame_5_button_event,
        )
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Borrow Book",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.borrow_book_image,
            anchor="w",
            command=self.frame_6_button_event,
        )
        self.frame_6_button.grid(row=6, column=0, sticky="ew")
        
        self.frame_7_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Show Logs",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.log_image,
            anchor="w",
            command=self.frame_7_button_event,
        )
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.credits = customtkinter.CTkLabel(
            self.navigation_frame,
            text="By Nikhil Kumar Jangir",
            font=customtkinter.CTkFont(size=13, weight="bold"),
        )
        self.credits.grid(row=10, column=0, padx=20, pady=(0, 60), sticky="s")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            variable=customtkinter.StringVar(value="Dark"),
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(
            row=10, column=0, padx=20, pady=(0, 20), sticky="s"
        )
        
        
        
        # -------------------------------------------------------------------------------------
        # --------------------------------- Home/First Frame ----------------------------------
        # -------------------------------------------------------------------------------------


        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.home_frame,
            text="",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "books.png")),
                size=(640, 200),
            ),
        )
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20)

        self.all_data_refresh()

        self.table = ttk.Treeview(
            self.home_frame,
            columns=("ID", "Title", "Author", "Availability"),
            show="headings",
            height=13,
            style="Treeview",
        )

        self.ctk_table_scrollbar = customtkinter.CTkScrollbar(
            self.home_frame, command=self.table.yview
        )
        self.ctk_table_scrollbar.grid(row=1, column=0, sticky="e")
        self.table.configure(yscrollcommand=self.ctk_table_scrollbar.set)

        self.table.column("ID", minwidth=10, width=20)
        self.table.column("Title", minwidth=290)
        self.table.column("Author", minwidth=150)
        self.table.column("Availability", minwidth=100)
        self.table.heading("ID", text="ID")
        self.table.heading("Title", text="Title")
        self.table.heading("Author", text="Author")
        self.table.heading("Availability", text="Availability")
        self.table.grid(row=1, column=0, sticky="nsew", padx=50, pady=(0, 0))

        self.display_books(self.table)

        self.home_frame_button_4 = customtkinter.CTkButton(
            self.home_frame,
            text="Refresh Data",
            command=lambda: [self.display_books(self.table), self.all_data_refresh()],
        )
        self.home_frame_button_4.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        
        
        
        
        # -------------------------------------------------------------------------------------
        # ---------------------------------- Second Frame -------------------------------------
        # -------------------------------------------------------------------------------------
        

        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.search_heading = customtkinter.CTkLabel(
            self.second_frame,
            text="Search Books here!",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.search_heading.grid(row=0, column=0, padx=30, pady=20, sticky="w")

        self.search_book_entry = customtkinter.CTkEntry(
            master=self.second_frame, width=400, placeholder_text="Search Book Name"
        )
        self.search_book_entry.grid(row=1, column=0, padx=30, pady=(10, 10), sticky="w")

        self.search_button_1 = customtkinter.CTkButton(
            master=self.second_frame,
            width=120,
            text="Search",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.search_books,
            hover_color="gray10",
        )
        self.search_button_1.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="e")

        self.search_table = ttk.Treeview(
            self.second_frame,
            columns=("ID", "Title", "Author", "Availability"),
            show="headings",
        )
        self.search_table.column("ID", minwidth=30, width=20)
        self.search_table.column("Title", minwidth=290)
        self.search_table.column("Author", minwidth=150)
        self.search_table.column("Availability", minwidth=100)
        self.search_table.heading("ID", text="ID")
        self.search_table.heading("Title", text="Title")
        self.search_table.heading("Author", text="Author")
        self.search_table.heading("Availability", text="Availability")
        self.search_table.grid(row=2, column=0, sticky="nsew", padx=50, pady=20)
        self.search_table.bind("<Motion>", "break")




        # -------------------------------------------------------------------------------------
        # ----------------------------------- Third Frame -------------------------------------
        # -------------------------------------------------------------------------------------

        self.third_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        if role == "student":
            self.addbooktop = customtkinter.CTkLabel(
                self.third_frame,
                text="Only Administrators are allowed to use this feature!",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.addbooktop.grid(row=0, column=0, padx=130, pady=150, sticky="nsew")
        else:
            self.new_book_title_var = customtkinter.StringVar()
            self.new_book_author_var = customtkinter.StringVar()
            self.new_book_avail_var = customtkinter.StringVar(value="Available")

            self.addbooktop = customtkinter.CTkLabel(
                self.third_frame,
                text="Add Book here!",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            )
            self.addbooktop.grid(row=0, column=0, padx=30, pady=20, sticky="w")

            self.addbooktitle = customtkinter.CTkLabel(
                self.third_frame,
                text="Title:",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            )
            self.addbooktitle.grid(row=1, column=0, padx=30, pady=0, sticky="w")

            self.new_book_title = customtkinter.CTkEntry(
                master=self.third_frame,
                width=400,
                placeholder_text="Title here",
                textvariable=self.new_book_title_var,
            )
            self.new_book_title.grid(row=2, column=0, padx=30, pady=0, sticky="w")

            customtkinter.CTkLabel(
                self.third_frame,
                text="Author:",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            ).grid(row=3, column=0, padx=30, pady=(20, 0), sticky="w")

            self.new_book_author = customtkinter.CTkEntry(
                master=self.third_frame,
                width=400,
                placeholder_text="Author here",
                textvariable=self.new_book_author_var,
            )
            self.new_book_author.grid(row=4, column=0, padx=30, pady=0, sticky="w")

            self.addbookavail = customtkinter.CTkLabel(
                self.third_frame,
                text="Availability:",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            )
            self.addbookavail.grid(row=5, column=0, padx=30, pady=(20, 0), sticky="w")

            self.new_book_availability = customtkinter.CTkOptionMenu(
                master=self.third_frame,
                values=["Available", "Borrowed"],
                variable=self.new_book_avail_var,
            )
            self.new_book_availability.grid(row=6, column=0, padx=30, pady=0, sticky="w")

            self.addbookbtn = customtkinter.CTkButton(
                self.third_frame, text="Add Book", command=self.add_book
            )
            self.addbookbtn.grid(row=8, column=0, padx=30, pady=50, sticky="w")


        # -------------------------------------------------------------------------------------
        # ----------------------------------- Fourth Frame ------------------------------------
        # -------------------------------------------------------------------------------------

        self.fourth_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        if role == "student":           
            self.deletebooktop = customtkinter.CTkLabel(
                self.fourth_frame,
                text="Only Administrators are allowed to use this feature!",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.deletebooktop.grid(row=0, column=0, padx=130, pady=150, sticky="nsew")
        else:
            self.fourth_frame.grid_columnconfigure(0, weight=1)
            
            customtkinter.CTkLabel(
                self.fourth_frame,
                text="Select a book below to delete and then click here ➡️",
                font=customtkinter.CTkFont(size=15, weight="bold"),
            ).grid(row=0, column=0, padx=95, pady=(20, 0), sticky="w")

            self.delete_table = ttk.Treeview(
                self.fourth_frame,
                columns=("ID", "Title", "Author", "Availability"),
                height=15,
                show="headings",
                style="delete.Treeview",
            )

            self.delete_table_scrollbar = customtkinter.CTkScrollbar(
                self.fourth_frame, command=self.delete_table.yview
            )
            self.delete_table_scrollbar.grid(row=1, column=0, sticky="e")
            self.delete_table.configure(yscrollcommand=self.delete_table_scrollbar.set)

            self.delete_table.column("ID", minwidth=30, width=20)
            self.delete_table.column("Title", minwidth=290)
            self.delete_table.column("Author", minwidth=150)
            self.delete_table.column("Availability", minwidth=100)
            self.delete_table.heading("ID", text="ID")
            self.delete_table.heading("Title", text="Title")
            self.delete_table.heading("Author", text="Author")
            self.delete_table.heading("Availability", text="Availability")
            self.delete_table.grid(
                row=1, column=0, sticky="nsew", padx=(120, 70), pady=(50, 0)
            )
            self.delete_table.bind("<Motion>", "break")

            self.delete_button_1 = customtkinter.CTkButton(
                master=self.fourth_frame,
                width=120,
                text="Delete Book",
                fg_color="transparent",
                border_width=2,
                text_color=("gray10", "#DCE4EE"),
                command=self.delete_book,
                hover_color="gray10",
            )
            self.delete_button_1.grid(
                row=0, column=0, padx=(0, 80), pady=(20, 0), sticky="e"
            )



        # -------------------------------------------------------------------------------------
        # ----------------------------------- Fifth Frame -------------------------------------
        # -------------------------------------------------------------------------------------

        self.fifth_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.fifth_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.fifth_frame,
            text="Select a book below to return and then click here ➡️",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, padx=95, pady=(20, 0), sticky="w")

        self.return_table = ttk.Treeview(
            self.fifth_frame,
            columns=("ID", "Title", "Author", "Availability"),
            height=15,
            show="headings",
            style="delete.Treeview",
        )

        self.return_table_scrollbar = customtkinter.CTkScrollbar(
            self.fifth_frame, command=self.return_table.yview
        )
        self.return_table_scrollbar.grid(row=1, column=0, sticky="e")
        self.return_table.configure(yscrollcommand=self.return_table_scrollbar.set)

        self.return_table.column("ID", minwidth=30, width=20)
        self.return_table.column("Title", minwidth=290)
        self.return_table.column("Author", minwidth=150)
        self.return_table.column("Availability", minwidth=100)
        self.return_table.heading("ID", text="ID")
        self.return_table.heading("Title", text="Title")
        self.return_table.heading("Author", text="Author")
        self.return_table.heading("Availability", text="Availability")
        self.return_table.grid(
            row=1, column=0, sticky="nsew", padx=(120, 70), pady=(50, 0)
        )
        self.return_table.bind("<Motion>", "break")

        self.return_button_1 = customtkinter.CTkButton(
            master=self.fifth_frame,
            width=120,
            text="Return Book",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.return_book,
            hover_color="gray10",
        )
        self.return_button_1.grid(
            row=0, column=0, padx=(0, 80), pady=(20, 0), sticky="e"
        )




        # -------------------------------------------------------------------------------------
        # ----------------------------------- Sixth Frame -------------------------------------
        # -------------------------------------------------------------------------------------
        
        
        self.sixth_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.sixth_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.sixth_frame,
            text="Select a book below to borrow and then click here ➡️",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, padx=95, pady=(20, 0), sticky="w")

        self.borrow_table = ttk.Treeview(
            self.sixth_frame,
            columns=("ID", "Title", "Author", "Availability"),
            height=15,
            show="headings",
            style="delete.Treeview",
        )

        self.borrow_table_scrollbar = customtkinter.CTkScrollbar(
            self.sixth_frame, command=self.borrow_table.yview
        )
        self.borrow_table_scrollbar.grid(row=1, column=0, sticky="e")
        self.borrow_table.configure(yscrollcommand=self.borrow_table_scrollbar.set)

        self.borrow_table.column("ID", minwidth=30, width=20)
        self.borrow_table.column("Title", minwidth=290)
        self.borrow_table.column("Author", minwidth=150)
        self.borrow_table.column("Availability", minwidth=100)
        self.borrow_table.heading("ID", text="ID")
        self.borrow_table.heading("Title", text="Title")
        self.borrow_table.heading("Author", text="Author")
        self.borrow_table.heading("Availability", text="Availability")
        self.borrow_table.grid(
            row=1, column=0, sticky="nsew", padx=(120, 70), pady=(50, 0)
        )
        self.borrow_table.bind("<Motion>", "break")

        self.borrow_button_1 = customtkinter.CTkButton(
            master=self.sixth_frame,
            width=120,
            text="Borrow Book",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.borrow_book,
            hover_color="gray10",
          )
        self.borrow_button_1.grid(
            row=0, column=0, padx=(0, 80), pady=(20, 0), sticky="e"
        )




            # -------------------------------------------------------------------------------------
            # ----------------------------------- Seventh Frame -----------------------------------
            # -------------------------------------------------------------------------------------
            
            
        self.seventh_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        
        if role == "student":           
            self.logtop = customtkinter.CTkLabel(
                self.seventh_frame,
                text="Only Administrators are allowed to use this feature!",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.logtop.grid(row=0, column=0, padx=130, pady=150, sticky="nsew")
        else:  
            self.logs_container = customtkinter.CTkScrollableFrame(
                self.seventh_frame,
                width=800,
                height=518,
            )
            self.logs_container.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
            
            self.seventh_frame.grid_columnconfigure(0, weight=1)
            self.seventh_frame.grid_rowconfigure(1, weight=1)
            

            self.display_logs()
        

            # the default frame
        self.select_frame_by_name("home")
        
        

    def select_frame_by_name(self, name):

        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )

        for i in range(2, 8):
            button_name = f"frame_{i}_button"
            button = getattr(self, button_name, None)
            button.configure(
                fg_color=("gray75", "gray25") if name == f"frame_{i}" else "transparent"
            )
            

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()
        if name == "frame_6":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()
        if name == "frame_7":
            self.seventh_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.seventh_frame.grid_forget()
            
            
    # -------------------------------------------------------------------------------------
    # ---------------------------- All Main Functions -------------------------------------
    # -------------------------------------------------------------------------------------   
             
    def create_log_card(self, log_entry):
        card = customtkinter.CTkFrame(self.logs_container, corner_radius=10)
        card.grid_columnconfigure(0, weight=1)
        
        # parse the timestamp and their actions from logs
        parts = log_entry.strip().split('] ')
        if len(parts) == 2:
            timestamp = parts[0][1:]
            action = parts[1]
            
            # make timestamp label
            time_label = customtkinter.CTkLabel(
                card,
                text=timestamp,
                font=("Arial", 10),
                text_color="gray70"
            )
            time_label.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
            
            # make action label
            action_label = customtkinter.CTkLabel(
                card,
                text=action,
                font=("Arial", 12),
                wraplength=700
            )
            action_label.grid(row=1, column=0, padx=10, pady=(0,5), sticky="w")
        
        return card
    
    def display_logs(self):
        # remove existing log cards
        self.logs_container.grid_forget()
        for widget in self.logs_container.winfo_children():
            widget.destroy()
        
        # reading logs in chunks for better performance
        file.seek(0)
        logs = file.readlines()
        
        # displaying only the last 50 logs for better performance
        for row, log in enumerate(logs[-50:]):
            # handling both old and new types of log i had
            if '~' in log:
                timestamp, action = log.split('~', 1)
                formatted_log = f"[{timestamp.strip()}] {action.strip()}"
            else:
                formatted_log = log.strip()
            
            card = self.create_log_card(formatted_log)
            card.grid(row=row, column=0, padx=5, pady=2, sticky="ew")
        
        self.logs_container.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

            
    def count_books(self):
        cursor.execute("SELECT COUNT(*) FROM books")
        return cursor.fetchone()[0]

    def count_available(self):
        cursor.execute("SELECT COUNT(*) FROM books where availability='Available'")
        return cursor.fetchone()[0]

    def count_borrowed(self):
        cursor.execute("SELECT COUNT(*) FROM books where availability='Borrowed'")
        return cursor.fetchone()[0]

    def all_data_refresh(self):
        self.thetable_label = customtkinter.CTkLabel(
            self.home_frame,
            text=f"{self.count_books()}           {self.count_borrowed()}",
            compound="center",
            font=customtkinter.CTkFont(size=38, weight="bold"),
            bg_color="#4b98d1",
        )
        self.thetable_label.grid(row=0, column=0, padx=240, pady=20, sticky="w")

        self.thetable_label1 = customtkinter.CTkLabel(
            self.home_frame,
            text=f"{self.count_available()}",
            compound="right",
            font=customtkinter.CTkFont(size=38, weight="bold"),
            bg_color="#4b98d1",
        )
        self.thetable_label1.grid(row=0, column=0, padx=125, pady=0, sticky="e")

    def display_books(self, tablename):
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        tablename.delete(*tablename.get_children())
        for book in books:
            tablename.insert("", "end", values=book)

    def search_books(self):
        keyword = self.search_book_entry.get()
        if keyword:
            cursor.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                (f"%{keyword}%", f"%{keyword}%"),
            )
            books = cursor.fetchall()
            if not books:
                CTkMessagebox(
                    title="Search Books",
                    message="No Book found",
                    icon="info",
                    fade_in_duration=2,
                )
            else:
                self.search_table.delete(*self.search_table.get_children())
                file.write(f"{datetime.now()} ~ {username} ~ Searched for {keyword}\n")
                for book in books:
                    self.search_table.insert("", "end", values=book)
        else:
            CTkMessagebox(
                title="Search Books", message="Please enter a keyword.", icon="warning"
            )

    def add_book(self):
        title = self.new_book_title.get()
        author = self.new_book_author.get()
        availability = self.new_book_availability.get()

        if title and author and availability:
            cursor.execute(
                "INSERT INTO books (title, author, availability) VALUES (?, ?, ?)",
                (title, author, availability),
            )
            conn.commit()
            CTkMessagebox(
                title="Info",
                message="Book added successfully.",
                icon="info",
                fade_in_duration=5,
            )
            file.write(format_log_entry(f"📚 Book '{title}' has been added by {username}"))
            self.new_book_title_var.set("")
            self.new_book_author_var.set("")
        else:
            CTkMessagebox(
                title="Add Book",
                message="Please enter all the book details.",
                icon="warning",
            )

    def delete_book(self):
        selected_item = self.delete_table.focus()
        if selected_item:
            confirmemsg = CTkMessagebox(
                title="Delete Book",
                message="Are you sure you want to delete this book?",
                icon="question",
                option_1="No",
                option_2="Yes",
            )
            confirmed = confirmemsg.get()
            if confirmed == "Yes":
                book_name = self.delete_table.item(selected_item)["values"][1]
                file.write(format_log_entry(f"🗑️ Book '{book_name}' has been deleted by {username}"))
                book_id = self.delete_table.item(selected_item)["values"][0]
                cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
                conn.commit()
                self.delete_table.delete(selected_item)
                CTkMessagebox(
                    title="Delete Book",
                    message="Book deleted successfully.",
                    icon="info",
                )
        else:
            CTkMessagebox(
                title="Delete Book", message="No book selected.", icon="warning"
            )

    def borrow_book(self):
        selected_item = self.borrow_table.selection()
        if selected_item:
            book_id = self.borrow_table.item(selected_item, "values")[0]
            book_title = self.borrow_table.item(selected_item, "values")[1]
            availability = self.borrow_table.item(selected_item, "values")[3]

            if availability == "Available":
                confirmemsg = CTkMessagebox(
                    title="Borrow Book",
                    message=f"Are you sure you want to borrow {book_title}?",
                    icon="question",
                    option_1="No",
                    option_2="Yes",
                )
                confirmed = confirmemsg.get()
                if confirmed == "Yes":                
                    cursor.execute(
                        "UPDATE books SET availability='Borrowed' WHERE id=?",
                        (book_id,),
                    )
                    conn.commit()
                    CTkMessagebox(
                        title="Borrow Book",
                        message=f"Book {book_title} borrowed by {username}.",
                        icon="info",
                    )
                    file.write(format_log_entry(f"📖 Book '{book_title}' has been borrowed by {username}"))
                    self.display_books(self.borrow_table)
            else:
                CTkMessagebox(
                    title="Borrow Book",
                    message="Book is not available.",
                    icon="warning",
                )
        else:
            CTkMessagebox(
                title="Borrow Book", message="No book selected.", icon="warning"
            )

    def return_book(self):
        selected_item = self.return_table.selection()
        if selected_item:
            book_id = self.return_table.item(selected_item, "values")[0]
            book_title = self.return_table.item(selected_item, "values")[1]
            availability = self.return_table.item(selected_item, "values")[3]

            if availability == "Borrowed":
                confirmemsg = CTkMessagebox(
                    title="Return Book",
                    message=f"Are you sure you want to return {book_title}?",
                    icon="question",
                    option_1="No",
                    option_2="Yes",
                )
                confirmed = confirmemsg.get()
                if confirmed == "Yes":
                    cursor.execute(
                        "UPDATE books SET availability='Available' WHERE id=?",
                        (book_id,),
                    )
                    conn.commit()
                    CTkMessagebox(
                        title="Return Book",
                        message=f"Book '{book_title}' returned by {username}.",
                        icon="info",
                    )
                    file.write(format_log_entry(f"📘 Book '{book_title}' has been returned by {username}"))
                    self.display_books(self.return_table)
            else:
                CTkMessagebox(
                    title="Return Book", message="Book is not borrowed.", icon="warning"
                )
        else:
            CTkMessagebox(
                title="Return Book", message="No book selected.", icon="warning"
            )
            
    def on_enter(self, event):
        if self.logout_btncheck is None:
            self.navigation_frame_label.grid_forget()
            self.button = customtkinter.CTkButton(
                master=self.navigation_frame,
                width=120,
                text="Logout",
                fg_color="transparent",
                border_width=2,
                text_color=("gray10", "#DCE4EE"),
                command=self.logoutnow,
                hover_color="gray10",
            )
            self.button.grid(row=0, column=0, padx=20, pady=20)
            self.after(500, self.on_leave)
            
    def on_leave(self):
            self.button.grid_forget()
            self.logout_btncheck = None
            self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
    def get_user_role(self, username):
        cursor.execute("SELECT role FROM accounts WHERE username = ?", (username,))
        role = cursor.fetchone()
        return role[0] if role else None
        
    def get_user_avatar(self, username):
        cursor.execute("SELECT avatar FROM accounts WHERE username = ?", (username,))
        avatar = cursor.fetchone()
        if not avatar or not avatar[0]:
            return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resource_files", "mainlogo.png")
        return avatar[0]
    
    def logoutnow(self):
        confirmemsg = CTkMessagebox(
            title="Logout",
            message=f"Are you sure you want to logout from {username}?",
            icon="question",
            option_1="No",
            option_2="Yes",
        )
        confirmed = confirmemsg.get()
        if confirmed == "Yes":    
            cursor.execute('UPDATE logged SET loggedin = 0, username = " "')
            conn.commit()
            file.write(f"{datetime.now()} ~ Logged out as {username}\n")
            self.home_button_event()
            self.navigation_frame.grid_forget()
            self.home_frame.grid_forget()
            self.show_login_screen()
        
    def get_logged(self):
        cursor.execute("SELECT loggedin FROM logged")
        loggedorno = cursor.fetchone()
        return loggedorno[0]

    def get_loggedusername(self):
        cursor.execute("SELECT username FROM logged")
        loggedorno = cursor.fetchone()
        return loggedorno[0]             

    def home_button_event(self):
        self.select_frame_by_name("home")
        self.all_data_refresh()
        self.display_books(self.table)

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        if role == "admin":
           self.display_books(self.delete_table)

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")
        self.display_books(self.return_table)

    def frame_6_button_event(self):
        self.select_frame_by_name("frame_6")
        self.display_books(self.borrow_table)
        
    def frame_7_button_event(self):
        self.select_frame_by_name("frame_7")
        for widget in self.logs_container.winfo_children():
            widget.destroy()
        
        file.seek(0)
        logs = file.readlines()
        
        row = 0
        for log in logs:
            card = self.create_log_card(log)
            card.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            row += 1

        # just scrolling to the bottom of logs to show the latest when "show logs" frame is clicked    
        self.logs_container.after(500, lambda: self.logs_container._parent_canvas.yview_moveto(1.0))

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    conn.close()
    

# *************************************************************************************
# *                                                                                   *
# *                           School Library Management System                        *
# *                                                                                   *
# *                            Author: Nikhil Kumar Jangir                            *
# *                        Contact Email: krunkistic@gmail.com                        *
# *                                                                                   *
# *    This program is the intellectual property of Nikhil Kumar Jangir. Unauthorized *
# *    copying, stealing, or distribution of this program, in whole or in part, is    *
# *    strictly prohibited unless prior written permission is obtained from the       *
# *    author.                                                                        *
# *                                                                                   *
# *    If you have been granted permission to use this program, you are required to   *
# *    give proper credit to the author by including the author's name in your        *
# *    project and acknowledging their contribution.                                  *
# *                                                                                   *
# *    For any queries, permission requests, or to contact the author, please email   *
# *    krunkistic@gmail.com.                                                          *
# *                                                                                   *
# *************************************************************************************