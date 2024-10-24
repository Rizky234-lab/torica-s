from tkinter import *
from tkinter import ttk
from tkinter import messagebox  # To show message boxes

# Main application window
root = Tk()
root.geometry("400x300")
root.title("Torica Furniture Store")

# Initialize furniture "databases"
furniturecodes = ('1', '2', '3', '4', '5')
furniturenames = ('Sofa', 'Lemari', 'Kursi', 'Meja', 'Lampu')
cnames = StringVar(value=furniturenames)
persediaan = {'1': 280, '2': 110, '3': 450, '4': 350, '5': 560}

# Color dictionary for furniture leaders
color_dict = {'merah': 'Merah', 'biru': 'Biru', 'kuning': 'Kuning', 'hijau': 'Hijau'}

# State variables
selected_color = StringVar()
selected_size = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

# List to store all transactions
transactions = []

# Create container for multiple screens (Frames)
login_frame = Frame(root, bg="blue")
welcome_frame = Frame(root, bg="blue")
main_frame = Frame(root, bg="white")

# Switch between frames
def show_frame(frame):
    frame.tkraise()

# --- Login Screen ---
def validate_login():
    first_name = first_name_var.get()
    last_name = last_name_var.get()

    if first_name and last_name:
        welcome_label.config(text=f"Welcome {first_name} {last_name}!")
        show_frame(welcome_frame)
    else:
        messagebox.showerror("Error", "Please enter both first and last names.")

first_name_var = StringVar()
last_name_var = StringVar()

Label(login_frame, text="First Name:", bg="blue", fg="white").grid(row=0, column=0, pady=10, padx=10)
Entry(login_frame, textvariable=first_name_var).grid(row=0, column=1, pady=10, padx=10)

Label(login_frame, text="Last Name:", bg="blue", fg="white").grid(row=1, column=0, pady=10, padx=10)
Entry(login_frame, textvariable=last_name_var).grid(row=1, column=1, pady=10, padx=10)

Button(login_frame, text="Login", command=validate_login).grid(row=2, column=0, columnspan=2, pady=20)

# --- Welcome Screen ---
welcome_label = Label(welcome_frame, text="", bg="blue", fg="white", font=("Arial", 16))
welcome_label.pack(pady=50)

Button(welcome_frame, text="Click me to see our furniture collection", 
       command=lambda: show_frame(main_frame)).pack(pady=10)

# --- Main Menu Screen (Furniture App) ---
def showPersediaan(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        code = furniturecodes[idx]
        name = furniturenames[idx]
        stock = persediaan[code]
        statusmsg.set(f"Persediaan {name} ({code}) {stock}")
    sentmsg.set('')  # Clear sent message

def sendtocart(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = furniturenames[idx]
        color = selected_color.get()
        size = selected_size.get()  # Get selected size
        if color and size:
            transaction = f"{size.capitalize()} {color_dict[color]} {name}"
            transactions.append(transaction)  # Save transaction
            sentmsg.set(f"Transaksi anda: {transaction}")
        else:
            sentmsg.set("Tolong pilih warna dan ukuran.")

def open_transactions():
    """Open a new window to display all transactions."""
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions available.")
        return

    trans_window = Toplevel(root)
    trans_window.title("All Transactions")
    trans_window.geometry("300x200")

    # Listbox to show transactions
    lb = Listbox(trans_window)
    lb.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Insert all transactions into the Listbox
    for t in transactions:
        lb.insert(END, t)

# Placeholder functions for menu actions
def open_main_menu():
    show_frame(main_frame)

def exit_app():
    root.quit()

def add_transaction():
    messagebox.showinfo("Add Transaction", "Add transaction placeholder.")

def edit_transaction():
    """Edit a selected transaction with confirmation."""
    if not transactions:
        messagebox.showinfo("Edit Transaction", "No transactions to edit.")
        return

    # Membuka jendela untuk memilih transaksi yang ingin diubah
    idx_to_edit = len(transactions) - 1  # Contoh: Edit transaksi terakhir
    selected_transaction = transactions[idx_to_edit]

    # Menampilkan konfirmasi apakah ingin mengganti transaksi ini
    confirm = messagebox.askyesno(
        "Edit Transaction", 
        f"Apakah kamu akan mengganti transaksi ini?\n{selected_transaction}"
    )

    if confirm:
        # Melakukan edit (misal: ubah warna atau ukuran dari transaksi terakhir)
        new_transaction = f"Medium Biru Sofa"  # Placeholder untuk transaksi baru
        transactions[idx_to_edit] = new_transaction
        messagebox.showinfo("Edit Successful", f"Transaksi berhasil diubah menjadi:\n{new_transaction}")

def delete_transaction():
    """Delete the last transaction with confirmation."""
    if not transactions:
        messagebox.showinfo("Delete Transaction", "No transactions to delete.")
        return

    # Transaksi terakhir
    last_transaction = transactions[-1]

    # Konfirmasi penghapusan
    confirm = messagebox.askyesno(
        "Delete Transaction", 
        f"Apakah kamu ingin menghapus transaksi ini?\n{last_transaction}"
    )

    if confirm:
        # Menghapus transaksi terakhir
        transactions.pop()
        messagebox.showinfo("Delete Successful", "Transaksi terakhir berhasil dihapus.")

# Create and grid the outer content frame
c = ttk.Frame(main_frame, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create widgets
lbox = Listbox(c, listvariable=cnames, height=5)
lbl_color = ttk.Label(c, text="Pilih warna furniture:")
lbl_size = ttk.Label(c, text="Pilih ukuran:")

# Color radio buttons
g1 = ttk.Radiobutton(c, text='Merah', variable=selected_color, value='merah')
g2 = ttk.Radiobutton(c, text='Biru', variable=selected_color, value='biru')
g3 = ttk.Radiobutton(c, text='Kuning', variable=selected_color, value='kuning')
g4 = ttk.Radiobutton(c, text='Hijau', variable=selected_color, value='hijau')

# Size radio buttons
s1 = ttk.Radiobutton(c, text='Big', variable=selected_size, value='big')
s2 = ttk.Radiobutton(c, text='Medium', variable=selected_size, value='medium')
s3 = ttk.Radiobutton(c, text='Small', variable=selected_size, value='small')

send = ttk.Button(c, text='Send to cart', command=sendtocart, default='active')
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

# Grid the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N, S, E, W))

# Grid for color options
lbl_color.grid(column=1, row=0, padx=10, pady=5, sticky=W)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
g4.grid(column=1, row=4, sticky=W, padx=20)

# Grid for size options (beside color options)
lbl_size.grid(column=2, row=0, padx=10, pady=5, sticky=W)
s1.grid(column=2, row=1, sticky=W, padx=20)
s2.grid(column=2, row=2, sticky=W, padx=20)
s3.grid(column=2, row=3, sticky=W, padx=20)

send.grid(column=2, row=4, sticky=E)
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=6, columnspan=2, sticky=(W, E))

# Configure grid resizing
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# Set event bindings
lbox.bind('<<ListboxSelect>>', showPersediaan)
lbox.bind('<Double-1>', sendtocart)
root.bind('<Return>', sendtocart)

# Attach frames to the root window
for frame in (login_frame, welcome_frame, main_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Create the menu bar
menubar = Menu(root)

# File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Main Menu", command=open_main_menu)
file_menu.add_command(label="Open Transaction", command=open_transactions)  # New option
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Help Menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="Add Transaction", command=add_transaction)
help_menu.add_command(label="Clear Transaction", command=delete_transaction)
help_menu.add_command(label="Edit Transaction", command=edit_transaction)
menubar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the root window
root.config(menu=menubar)

# Show the login frame initially
show_frame(login_frame)

# Start the GUI loop
root.mainloop()
