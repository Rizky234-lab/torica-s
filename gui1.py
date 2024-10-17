import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas
from data_manager import DataManager


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Furniture")
        self.geometry("400x400")
        self.data_manager = DataManager()
        self.current_data_type = 'warna'

        self.create_frames()
        self.create_widgets()
        self.show_home()

    def create_frames(self):
        self.home_frame = tk.Frame(self)
        self.furniture_frame = tk.Frame(self)
        self.warna_frame = tk.Frame(self)
        self.ukuran_frame = tk.Frame(self)
        self.warna_tambah_frame = tk.Frame(self)
        self.ukuran_tambah_frame = tk.Frame(self)
        self.furniture_tambah_frame = tk.Frame(self)
        self.detail_frame = tk.Frame(self)

    def create_widgets(self):
        # Home frame widgets
        canvas = Canvas(self.home_frame, width=400, height=150, bg="#5960ff", highlightthickness=0)
        canvas.create_text(200, 75, text="DATA FURNITURE", font=("Helvetica", 24, "bold"), fill="white")
        canvas.pack()

        frame = tk.Frame(self.home_frame)
        frame.pack(pady=20)

        button_furniture = tk.Button(frame, text="Furniture", font=("Helvetica", 12, "bold"), compound=tk.TOP, bg="blue", fg="white", padx=20, pady=10, command=lambda: self.show_data('furniture'))
        button_furniture.grid(row=0, column=0, padx=20)

        button_ukuran = tk.Button(frame, text="Ukuran", font=("Helvetica", 12, "bold"), compound=tk.TOP, bg="cyan", fg="white", padx=20, pady=10, command=lambda: self.show_data('ukuran'))
        button_ukuran.grid(row=0, column=1, padx=20)

        button_warna = tk.Button(frame, text="Warna", font=("Helvetica", 12, "bold"), compound=tk.TOP, bg="green", fg="white", padx=20, pady=10, command=lambda: self.show_data('warna'))
        button_warna.grid(row=0, column=2, padx=20)

        # Data frames (furniture, warna, ukuran)
        for frame, title in [(self.furniture_frame, "List Furniture"), (self.warna_frame, "List Warna"), (self.ukuran_frame, "List Ukuran")]:
            label = tk.Label(frame, text=title, font=("Helvetica", 16))
            label.pack(pady=10)
            
            listbox = tk.Listbox(frame, width=40, height=10)
            listbox.pack(pady=10)

            edit_button = tk.Button(frame, text="EDIT", command=lambda f=frame: self.show_edit_dialog(f))
            edit_button.pack(side=tk.LEFT, padx=5, pady=5)

            if frame == self.furniture_frame:
                detail_button = tk.Button(frame, text="Tampilkan Detail", command=self.show_furniture_detail)
                detail_button.pack(pady=5)
                
            back_button = tk.Button(frame, text="BACK", command=self.show_home)
            back_button.pack(pady=10)
            
            if frame == self.warna_frame:
                add_button = tk.Button(frame, text="+", command=self.show_tambah_warna)
                add_button.pack(side=tk.LEFT, padx=5, pady=5)
                
                delete_button = tk.Button(frame, text="-", command=lambda: self.delete_action('warna'))
                delete_button.pack(side=tk.RIGHT, padx=5, pady=5)
                
            if frame == self.ukuran_frame:
                add_button = tk.Button(frame, text="+", command=self.show_tambah_ukuran)
                add_button.pack(side=tk.LEFT, padx=5, pady=5)
                
                delete_button = tk.Button(frame, text="-", command=lambda: self.delete_action('ukuran'))
                delete_button.pack(side=tk.RIGHT, padx=5, pady=5)
                
            if frame == self.furniture_frame:
                add_button = tk.Button(frame, text="+", command=self.show_tambah_furniture)
                add_button.pack(side=tk.LEFT, padx=5, pady=5)
                
                delete_button = tk.Button(frame, text="-", command=lambda: self.delete_action('furniture'))
                delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Warna tambah frame
        label_tambah = tk.Label(self.warna_tambah_frame, text="Tambah Warna Baru", font=("Helvetica", 12))
        label_tambah.pack(pady=5)
        
        self.warna_entry = tk.Entry(self.warna_tambah_frame, width=30)
        self.warna_entry.pack(pady=5)
        
        tambah_button = tk.Button(self.warna_tambah_frame, text="Tambah Warna", command=self.tambah_warna)
        tambah_button.pack(pady=10)
        
        back_button = tk.Button(self.warna_tambah_frame, text="BACK", command=lambda: self.show_data('warna'))
        back_button.pack(pady=10)
        
        # ukuran tambah frame
        label_tambah = tk.Label(self.ukuran_tambah_frame, text="Tambah Ukuran Baru", font=("Helvetica", 12))
        label_tambah.pack(pady=5)
