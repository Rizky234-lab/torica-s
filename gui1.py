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


        self.ukuran_entry = tk.Entry(self.ukuran_tambah_frame, width=30)
        self.ukuran_entry.pack(pady=5)
        
        tambah_button = tk.Button(self.ukuran_tambah_frame, text="Tambah Ukuran", command=self.tambah_ukuran)
        tambah_button.pack(pady=10)
        
        back_button = tk.Button(self.ukuran_tambah_frame, text="BACK", command=lambda: self.show_data('ukuran'))
        back_button.pack(pady=10)
        
        # furniture tambah frame
        label_tambah = tk.Label(self.furniture_tambah_frame, text="Tambah furniture Baru", font=("Helvetica", 12))
        label_tambah.pack(pady=5)
        
        self.nama_furniture_entry = tk.Entry(self.furniture_tambah_frame, width=30)
        self.nama_furniture_entry.pack(pady=5)

        self.ukuran_var = tk.StringVar()
        self.warna_var = tk.StringVar()
        
        label_ukuran = tk.Label(self.furniture_tambah_frame, text="Pilih Ukuran", font=("Helvetica", 10))
        label_ukuran.pack(pady=5)
        
        self.ukuran_option = tk.OptionMenu(self.furniture_tambah_frame, self.ukuran_var, *self.data_manager.list_data('ukuran').keys())
        self.ukuran_option.pack(pady=5)
        
        label_warna = tk.Label(self.furniture_tambah_frame, text="Pilih Warna", font=("Helvetica", 10))
        label_warna.pack(pady=5)
        
        self.warna_option = tk.OptionMenu(self.furniture_tambah_frame, self.warna_var, *self.data_manager.list_data('warna').keys())
        self.warna_option.pack(pady=5)
        
        tambah_button = tk.Button(self.furniture_tambah_frame, text="Tambah Furniture", command=self.tambah_furniture)
        tambah_button.pack(pady=10)
        
        back_button = tk.Button(self.furniture_tambah_frame, text="BACK", command=lambda: self.show_data('furniture'))
        back_button.pack(pady=10)

        # Detail frame
        self.detail_label = tk.Label(self.detail_frame, text="", font=("Helvetica", 12))
        self.detail_label.pack(pady=10)

        back_button = tk.Button(self.detail_frame, text="BACK", command=self.show_data)
        back_button.pack(pady=10)

        self.edit_frame = tk.Frame(self)
        label_edit = tk.Label(self.edit_frame, text="Edit Data", font=("Helvetica", 12))
        label_edit.pack(pady=5)
        
        self.edit_entry = tk.Entry(self.edit_frame, width=30)
        self.edit_entry.pack(pady=5)
        
        save_button = tk.Button(self.edit_frame, text="SAVE", command=self.save_edit)
        save_button.pack(pady=10)
        
        back_button = tk.Button(self.edit_frame, text="BACK", command=self.show_data)
        back_button.pack(pady=10)

    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack()

    def show_data(self, data_type=None):
        self.hide_all_frames()
        if data_type:
            self.current_data_type = data_type
        if self.current_data_type == 'furniture':
            frame = self.furniture_frame
        elif self.current_data_type == 'warna':
            frame = self.warna_frame
        elif self.current_data_type == 'ukuran':
            frame = self.ukuran_frame
        frame.pack()
        self.update_listbox(self.current_data_type)

    def show_tambah_warna(self):
        self.hide_all_frames()
        self.warna_tambah_frame.pack()
        
    def show_tambah_ukuran(self):
        self.hide_all_frames()
        self.ukuran_tambah_frame.pack()
        
    def show_tambah_furniture(self):
        self.hide_all_frames()
        self.furniture_tambah_frame.pack()
        self.update_options()

    def hide_all_frames(self):
        for frame in (self.home_frame, self.furniture_frame, self.warna_frame, self.ukuran_frame, self.warna_tambah_frame, self.ukuran_tambah_frame, self.furniture_tambah_frame, self.detail_frame, self.edit_frame):
            frame.pack_forget()

    def update_listbox(self, data_type):
        listbox = self.furniture_frame.winfo_children()[1] if data_type == 'furniture' else self.warna_frame.winfo_children()[1] if data_type == 'warna' else self.ukuran_frame.winfo_children()[1]
        listbox.delete(0, tk.END)
        items = self.data_manager.list_data(data_type)
        for item_id, item_name in items.items():
            listbox.insert(tk.END, f"{item_id}: {item_name}")
