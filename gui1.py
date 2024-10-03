import tkinter as tk
from tkinter import messagebox

# Membuat jendela utama
root = tk.Tk()
root.title("Pilih Warna untuk Melihat Daftar Furnitur Kami")
root.geometry("400x400")
root.config(bg="cyan")  # Set default background color

# Pesan selamat datang
messagebox.showinfo("Hello World", "Selamat datang di Torica World! Semua furnitur ada di sini.")

# Data furnitur berdasarkan warna, ID, dan ukuran
furniture_data = {
    "abu abu": {},
    "coklat": {},
    "olive": {},
    "hitam": {},
}

# Warna latar belakang
color_mapping = {
    "abu abu": "grey",
    "coklat": "brown",
    "olive": "olive",
    "hitam": "black",
}

def show_furniture():
    selected_color = color_var.get()
    if selected_color in furniture_data:
        items = furniture_data[selected_color]
        message = f"Furnitur berwarna {selected_color}:\n"
        if items:
            for item, details in items.items():
                message += f"{item} (ID: {details['ID']}, Ukuran: {details['Ukuran']})\n"
        else:
            message += "Tidak ada furnitur yang tersedia."
        messagebox.showinfo("Furnitur", message)
        # Mengubah warna latar belakang
        root.config(bg=color_mapping[selected_color])
    else:
        messagebox.showwarning("Peringatan", "Silakan pilih warna yang valid!")

def add_furniture():
    def submit_furniture():
        furniture_name = name_entry.get()
        furniture_id = id_entry.get()
        furniture_size = size_entry.get()
        furniture_color = color_var.get()

        if furniture_name and furniture_id and furniture_size:
            furniture_data[furniture_color][furniture_name] = {
                "ID": furniture_id,
                "Ukuran": furniture_size
            }
            messagebox.showinfo("Berhasil", f"Furnitur '{furniture_name}' telah ditambahkan!")
            add_window.destroy()
        else:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")

    add_window = tk.Toplevel(root)
    add_window.title("Tambah Furnitur")
    add_window.geometry("300x250")

    tk.Label(add_window, text="Nama Furnitur:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="ID Furnitur:").pack(pady=5)
    id_entry = tk.Entry(add_window)
    id_entry.pack(pady=5)

    tk.Label(add_window, text="Ukuran Furnitur:").pack(pady=5)
    size_entry = tk.Entry(add_window)
    size_entry.pack(pady=5)

    submit_button = tk.Button(add_window, text="Tambahkan Furnitur", command=submit_furniture)
    submit_button.pack(pady=20)

def remove_furniture():
    def submit_removal():
        furniture_name = name_entry.get()
        furniture_color = color_var.get()

        if furniture_color in furniture_data and furniture_name in furniture_data[furniture_color]:
            del furniture_data[furniture_color][furniture_name]
            messagebox.showinfo("Berhasil", f"Furnitur '{furniture_name}' telah dihapus!")
            remove_window.destroy()
        else:
            messagebox.showwarning("Peringatan", "Furnitur tidak ditemukan!")

    remove_window = tk.Toplevel(root)
    remove_window.title("Hapus Furnitur")
    remove_window.geometry("300x200")

    tk.Label(remove_window, text="Nama Furnitur yang ingin dihapus:").pack(pady=5)
    name_entry = tk.Entry(remove_window)
    name_entry.pack(pady=5)

    submit_button = tk.Button(remove_window, text="Hapus Furnitur", command=submit_removal)
    submit_button.pack(pady=20)

# Variabel untuk warna yang dipilih
color_var = tk.StringVar(value="abu abu")

# Membuat label
label = tk.Label(root, text="Pilihlah warna kesukaan anda:", bg="white", font=("Arial", 12))
label.pack(pady=20)

# Membuat pilihan warna
colors = ["abu abu", "coklat", "olive", "hitam"]
for color in colors:
    rb = tk.Radiobutton(root, text=color.capitalize(), variable=color_var, value=color, bg="white")
    rb.pack(anchor=tk.W)

# Membuat tombol untuk menampilkan furnitur
show_button = tk.Button(root, text="Tampilkan Furnitur", command=show_furniture, bg="lightgray")
show_button.pack(pady=10)

# Membuat tombol untuk menambahkan furnitur
add_button = tk.Button(root, text="Tambah Furnitur", command=add_furniture, bg="lightgreen")
add_button.pack(pady=10)

# Membuat tombol untuk menghapus furnitur
remove_button = tk.Button(root, text="Hapus Furnitur", command=remove_furniture, bg="lightcoral")
remove_button.pack(pady=10)

# Menjalankan aplikasi
root.mainloop()
