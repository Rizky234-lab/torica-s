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
        canvas = Canvas(self.home_frame, width=400, height=150, bg="blue", highlightthickness=0)
        canvas.create_text(200, 75, text="DATA FURNITURE", font=("Times new roman", 24, "bold"), fill="white")
        canvas.pack()

        frame = tk.Frame(self.home_frame)
        frame.pack(pady=20)

        button_furniture = tk.Button(frame, text="Furniture", font=("Times new roman", 12), compound=tk.TOP, bg="blue", fg="white", padx=20, pady=10, command=lambda: self.show_data('furniture'))
        button_furniture.grid(row=0, column=0, padx=20)

        button_ukuran = tk.Button(frame, text="Ukuran", font=("Times new roman", 12), compound=tk.TOP, bg="blue", fg="white", padx=20, pady=10, command=lambda: self.show_data('ukuran'))
        button_ukuran.grid(row=0, column=1, padx=20)

        button_warna = tk.Button(frame, text="WARNA", font=("Times new roman", 12), compound=tk.TOP, bg="blue", fg="white", padx=20, pady=10, command=lambda: self.show_data('warna'))
        button_warna.grid(row=0, column=2, padx=20)

        # Data frames (furniture, warna, ukuran)
        for frame, title in [(self.furniture_frame, "List Furniture"), (self.warna_frame, "List Warna"), (self.ukuran_frame, "List Ukuran")]:
            label = tk.Label(frame, text=title, font=("Helvetica", 16))
            label.pack(pady=10)
            
            listbox = tk.Listbox(frame, width=40, height=10)
            listbox.pack(pady=10)

            edit_button = tk.Button(frame, text="Edit", command=lambda f=frame: self.show_edit_dialog(f))
            edit_button.pack(side=tk.LEFT, padx=5, pady=5)

            if frame == self.furniture_frame:
                detail_button = tk.Button(frame, text="Tampilkan Detail", command=self.show_furniture_detail)
                detail_button.pack(pady=5)
                
            back_button = tk.Button(frame, text="Kembali", command=self.show_home)
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
        
        back_button = tk.Button(self.warna_tambah_frame, text="Kembali", command=lambda: self.show_data('warna'))
        back_button.pack(pady=10)
        
        # ukuran tambah frame
        label_tambah = tk.Label(self.ukuran_tambah_frame, text="Tambah Ukuran Baru", font=("Helvetica", 12))
        label_tambah.pack(pady=5)
        
        self.ukuran_entry = tk.Entry(self.ukuran_tambah_frame, width=30)
        self.ukuran_entry.pack(pady=5)
        
        tambah_button = tk.Button(self.ukuran_tambah_frame, text="Tambah Ukuran", command=self.tambah_ukuran)
        tambah_button.pack(pady=10)
        
        back_button = tk.Button(self.ukuran_tambah_frame, text="Kembali", command=lambda: self.show_data('ukuran'))
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
        
        back_button = tk.Button(self.furniture_tambah_frame, text="Kembali", command=lambda: self.show_data('furniture'))
        back_button.pack(pady=10)

        # Detail frame
        self.detail_label = tk.Label(self.detail_frame, text="", font=("Helvetica", 12))
        self.detail_label.pack(pady=10)

        back_button = tk.Button(self.detail_frame, text="Kembali", command=self.show_data)
        back_button.pack(pady=10)

        self.edit_frame = tk.Frame(self)
        label_edit = tk.Label(self.edit_frame, text="Edit Data", font=("Helvetica", 12))
        label_edit.pack(pady=5)
        
        self.edit_entry = tk.Entry(self.edit_frame, width=30)
        self.edit_entry.pack(pady=5)
        
        save_button = tk.Button(self.edit_frame, text="Simpan", command=self.save_edit)
        save_button.pack(pady=10)
        
        back_button = tk.Button(self.edit_frame, text="Kembali", command=self.show_data)
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

    def tambah_warna(self):
        warna = self.warna_entry.get().strip()
        if warna:
            if self.data_manager.add_data('warna', warna):
                messagebox.showinfo("Sukses", f"Warna '{warna}' berhasil ditambahkan.")
                self.warna_entry.delete(0, tk.END)
                self.show_data('warna')
            else:
                messagebox.showerror("Error", "Gagal menambahkan warna.")
        else:
            messagebox.showwarning("Peringatan", "Nama warna tidak boleh kosong.")

    def tambah_ukuran(self):
        ukuran = self.ukuran_entry.get().strip()
        if ukuran:
            if self.data_manager.add_data('ukuran', ukuran):
                messagebox.showinfo("Sukses", f"Ukuran '{ukuran}' berhasil ditambahkan.")
                self.ukuran_entry.delete(0, tk.END)
                self.show_data('ukuran')
            else:
                messagebox.showerror("Error", "Gagal menambahkan ukuran.")
        else:
            messagebox.showwarning("Peringatan", "Nama ukuran tidak boleh kosong.")

    def tambah_furniture(self):
        nama = self.nama_furniture_entry.get().strip()
        ukuran = self.ukuran_var.get()
        warna = self.warna_var.get()
        if nama and ukuran and warna:
            if self.data_manager.add_furniture(nama, ukuran, warna):
                messagebox.showinfo("Sukses", f"Furniture '{nama}' berhasil ditambahkan.")
                self.nama_furniture_entry.delete(0, tk.END)
                self.show_data('furniture')
            else:
                messagebox.showerror("Error", "Gagal menambahkan furniture.")
        else:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")

    def delete_action(self, data_type):
        selected_indices = self.get_selected_indices(data_type)
        if selected_indices:
            selected_index = selected_indices[0]
            listbox = self.furniture_frame.winfo_children()[1] if data_type == 'furniture' else self.warna_frame.winfo_children()[1] if data_type == 'warna' else self.ukuran_frame.winfo_children()[1]
            item_text = listbox.get(selected_index)
            item_id = item_text.split(":")[0].strip()
            confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus item ini?\n{item_text}")
            if confirm:
                if self.data_manager.delete_item(data_type, item_id):
                    messagebox.showinfo("Sukses", f"{data_type.capitalize()} dengan ID {item_id} berhasil dihapus.")
                    self.update_listbox(data_type)
                else:
                    messagebox.showerror("Error", f"Gagal menghapus {data_type} dengan ID {item_id}.")
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih item yang ingin dihapus.")

    def get_selected_indices(self, data_type):
        listbox = self.furniture_frame.winfo_children()[1] if data_type == 'furniture' else self.warna_frame.winfo_children()[1] if data_type == 'warna' else self.ukuran_frame.winfo_children()[1]
        return listbox.curselection()

    def show_edit_dialog(self, frame):
        selected_indices = self.get_selected_indices(self.current_data_type)
        if selected_indices:
            index = selected_indices[0]
            selected_item = frame.winfo_children()[1].get(index)
            parts = selected_item.split(":", 1)
            if len(parts) == 2:
                item_id = parts[0].strip()
                item_name = parts[1].strip()
                self.edit_entry.delete(0, tk.END)
                self.edit_entry.insert(0, item_name)
                self.edit_frame.pack()
                self.current_edit_id = item_id  # Store the ID for saving later
            else:
                messagebox.showwarning("Peringatan", "Format data tidak sesuai.")
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih item yang ingin diedit.")

    def save_edit(self):
        new_name = self.edit_entry.get().strip()
        if new_name == "":
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
            return
        if hasattr(self, 'current_edit_id'):
            success = self.data_manager.update_item(self.current_data_type, self.current_edit_id, new_name)
            if success:
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                self.update_listbox(self.current_data_type)
                self.edit_entry.delete(0, tk.END)
                self.edit_frame.pack_forget()  # Hide edit frame after saving
            else:
                messagebox.showerror("Error", "Gagal memperbarui data.")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada item yang sedang diedit.")

    def show_furniture_detail(self):
        selected_indices = self.get_selected_indices('furniture')
        if selected_indices:
            index = selected_indices[0]
            selected_item = self.furniture_frame.winfo_children()[1].get(index)
            item_id, item_name = selected_item.split(": ")
            self.detail_label.config(text=f"Detail Furniture:\nID: {item_id}\nNama: {item_name}")
            self.detail_frame.pack()
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih furniture untuk melihat detail.")

# Pastikan untuk membuat instance dari Application dan menjalankan main loop
if __name__ == "__main__":
    app = Application()
    app.mainloop()
