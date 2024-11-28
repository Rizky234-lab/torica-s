from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime  # For transaction timestamps

# Main application window
root = Tk()
root.geometry("700x400")
root.title("Torica Furniture Store")

# Initialize furniture "databases"
furniturecodes = ['1', '2', '3', '4', '5']
furniturenames = ['Sofa', 'Lemari', 'Kursi', 'Meja', 'Lampu']
cnames = StringVar(value=furniturenames)
persediaan = {'1': 280, '2': 190, '3': 450, '4': 350, '5': 560}

# Color dictionary for furniture colors
color_dict = {'merah': 'Merah', 'biru': 'Biru', 'kuning': 'Kuning', 'hijau': 'Hijau'}
size_dict = {'small': 'Small', 'medium': 'Medium', 'big': 'Big'}



# State variables
selected_color = StringVar()
selected_size = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

# List to store all transactions, including timestamp and other details
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

def calculate_price(furniture_code, size):
    """Calculate the price of a furniture item based on its code and size."""
    base_price = 500_000  # Base price for code '1' and small size
    price_increase = int(furniture_code) * 500  # Increase price based on furniture code
    size_increase = {"small": 0, "medium": 500_000, "big": 1_000_000}  # Size-based increase
    
    # Calculate final price
    return base_price + price_increase + size_increase.get(size, 0)

def sendtocart(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = furniturenames[idx]
        code = furniturecodes[idx]
        color = selected_color.get()
        size = selected_size.get()  # Get selected size

        if persediaan[code] > 0 and color and size:
            price = calculate_price(code, size)  # Calculate price based on furniture code and size
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            persediaan[code] -= 1
            
            transaction = {
                "timestamp": timestamp,
                "furniture": name,
                "color": color_dict[color],
                "size": size.capitalize(),
                "price": f"Rp. {price:,.0f}"
            }
            transactions.append(transaction)
            sentmsg.set(f"Transaksi anda: {transaction['furniture']} ({transaction['size']} - {transaction['color']}) seharga {transaction['price']} | Stok tersisa: {persediaan[code]}")
            statusmsg.set(f"Persediaan {name} ({code}) {persediaan[code]}")
        else:
            if persediaan[code] <= 0:
                sentmsg.set(f"Maaf, stok {name} sudah habis!")
            else:
                sentmsg.set("Tolong pilih warna dan ukuran.")


def open_transactions():
    """Open a new window to display all transactions."""
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions available.")
        return

    trans_window = Toplevel(root)
    trans_window.title("All Transactions")
    trans_window.geometry("700x300")

    # Define Treeview columns
    columns = ("timestamp", "furniture", "color", "size", "price")

    # Create Treeview with columns for each transaction detail
    tree = ttk.Treeview(trans_window, columns=columns, show="headings", height=10)
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Define headings for each column
    tree.heading("timestamp", text="Timestamp")
    tree.heading("furniture", text="Furniture")
    tree.heading("color", text="Color")
    tree.heading("size", text="Size")
    tree.heading("price", text="Price")

     # Insert all transactions into the Treeview
    for trans in transactions:
        tree.insert("", "end", values=(trans["timestamp"], trans["furniture"], trans["color"], trans["size"], trans["price"]))

def save_transactions_to_file():
    """Save all transactions to a text file."""
    if not transactions:
        messagebox.showinfo("Save Transactions", "No transactions to save.")
        return

    file_name = "data_transaksi.txt"  

    try:
        with open(file_name, 'w') as file:
            for trans in transactions:
                line = f"{trans['timestamp']}, {trans['furniture']}, {trans['color']}, {trans['size']}, {trans['price']}\n"
                file.write(line)

        messagebox.showinfo("Save Successful", f"Transactions have been saved to {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save transactions: {str(e)}")

def add_furniture():
    """Allow user to manually add a new furniture item."""
    def save_furniture():
        name = furniture_name_var.get()
        code = str(len(furniturecodes) + 1)  # Generate new code
        stock = stock_var.get()
        
        if name and stock.isdigit():
            furniturenames.append(name)
            furniturecodes.append(code)
            persediaan[code] = int(stock)
            cnames.set(furniturenames)  # Update listbox display
            
            # Save the new furniture to a text file
            with open("data_furniture.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            add_window.destroy()
            messagebox.showinfo("Success", f"{name} has been added to the inventory!")
        else:
            messagebox.showerror("Error", "Please enter a valid name and stock quantity.")

    add_window = Toplevel(root)
    add_window.title("Add New Furniture")
    add_window.geometry("300x200")

    furniture_name_var = StringVar()
    stock_var = StringVar()

    Label(add_window, text="Furniture Name:").pack(pady=5)
    Entry(add_window, textvariable=furniture_name_var).pack(pady=5)

    Label(add_window, text="Stock Quantity:").pack(pady=5)
    Entry(add_window, textvariable=stock_var).pack(pady=5)

    Button(add_window, text="Add Furniture", command=save_furniture).pack(pady=10)

def add_color():
    """Allow user to add new color options for furniture."""
    add_color_window = Toplevel(root)
    add_color_window.title("Add New Color")
    add_color_window.geometry("300x200")

    # Variables for new color
    color_code_var = StringVar()
    color_name_var = StringVar()  # This will store the display name

    # Create and layout widgets
    Label(add_color_window, text="Color Code:").pack(pady=5)
    Entry(add_color_window, textvariable=color_code_var).pack(pady=5)

    Label(add_color_window, text="Display Name:").pack(pady=5)
    Entry(add_color_window, textvariable=color_name_var).pack(pady=5)  # Now using color_name_var

    def save_color():
        code = color_code_var.get().strip().lower()
        name = color_name_var.get().strip()

        if code and name:
            if code in color_dict:
                messagebox.showerror("Error", "This color code already exists!")
                return
            
            # Add new color to dictionary
            color_dict[code] = name

            # Save the new color to a text file
            with open("data_warna.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            # Create new radio button for the color
            new_radio = ttk.Radiobutton(c, text=name, variable=selected_color, value=code)
            
            # Find the row after the last color radio button
            last_row = 0
            for widget in c.grid_slaves():
                if isinstance(widget, ttk.Radiobutton) and widget.grid_info()['column'] == 1:
                    last_row = max(last_row, widget.grid_info()['row'])
            
            # Place the new radio button
            new_radio.grid(column=1, row=last_row + 1, sticky=W, padx=20)

            messagebox.showinfo("Success", f"New color '{name}' has been added!")
            add_color_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter both color code and display name!")

    Button(add_color_window, text="Add Color", command=save_color).pack(pady=20)

def add_size():
    """Allow user to add new size options for furniture."""
    add_size_window = Toplevel(root)
    add_size_window.title("Add New Size")
    add_size_window.geometry("300x200")

    # Variables for new size
    size_code_var = StringVar()
    size_name_var = StringVar()  # This will store the display name

    # Create and layout widgets
    Label(add_size_window, text="Size Code:").pack(pady=5)
    Entry(add_size_window, textvariable=size_code_var).pack(pady=5)

    Label(add_size_window, text="Display Name:").pack(pady=5)
    Entry(add_size_window, textvariable=size_name_var).pack(pady=5)  # Now using size_name_var

    def save_size():
        code = size_code_var.get().strip().lower()
        name = size_name_var.get().strip()

        if code and name:
            if code in size_dict:
                messagebox.showerror("Error", "This size code already exists!")
                return
            
            # Add new size to dictionary
            size_dict[code] = name

            # Save the new size to a text file
            with open("data_ukuran.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            # Create new radio button for the size
            new_radio = ttk.Radiobutton(c, text=name, variable=selected_size, value=code)
            
            # Find the row after the last size radio button
            last_row = 0
            for widget in c.grid_slaves():
                if isinstance(widget, ttk.Radiobutton) and widget.grid_info()['column'] == 2:
                    last_row = max(last_row, widget.grid_info()['row'])
            
            # Place the new radio button
            new_radio.grid(column=2, row=last_row + 1, sticky=W, padx=20)

            messagebox.showinfo("Success", f"New size '{name}' has been added!")
            add_size_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter both size code and display name!")

    Button(add_size_window, text="Add Size", command=save_size).pack(pady=20)


# Placeholder functions for menu actions
def open_main_menu():
    show_frame(main_frame)

def exit_app():
    root.quit()

def add_transaction():
    add_furniture()

def edit_transaction():
    if not transactions:
        messagebox.showinfo("Edit Transaction", "No transactions to edit.")
        return

    # Create a new window to select and edit a transaction
    edit_window = Toplevel(root)
    edit_window.title("Edit Transaction")
    edit_window.geometry("400x300")

    # Dropdown to select transaction
    selected_transaction_var = StringVar()
    transaction_options = [f"{i+1}. {t['furniture']} - {t['size']} - {t['color']} - {t['price']}" for i, t in enumerate(transactions)]
    selected_transaction_var.set(transaction_options[0])  # Default to the first transaction

    Label(edit_window, text="Select Transaction to Edit:").pack(pady=5)
    transaction_menu = OptionMenu(edit_window, selected_transaction_var, *transaction_options)
    transaction_menu.pack(pady=5)

    # Editable fields for transaction details
    Label(edit_window, text="Furniture Name:").pack(pady=5)
    furniture_name_var = StringVar()
    Entry(edit_window, textvariable=furniture_name_var).pack(pady=5)

    Label(edit_window, text="Furniture Code:").pack(pady=5)
    furniture_code_var = StringVar()
    Entry(edit_window, textvariable=furniture_code_var).pack(pady=5)

    Label(edit_window, text="Stock Quantity:").pack(pady=5)
    stock_var = StringVar()
    Entry(edit_window, textvariable=stock_var).pack(pady=5)

    Label(edit_window, text="Price:").pack(pady=5)
    price_var = StringVar()
    Entry(edit_window, textvariable=price_var).pack(pady=5)

    # Function to load selected transaction data
    def load_selected_transaction():
        index = int(selected_transaction_var.get().split(".")[0]) - 1
        selected_transaction = transactions[index]

        furniture_name_var.set(selected_transaction["furniture"])
        furniture_code_var.set(furniturecodes[furniturenames.index(selected_transaction["furniture"])])
        stock_var.set(persediaan[furniture_code_var.get()])
        price_var.set(selected_transaction["price"])

    # Button to load data of selected transaction
    Button(edit_window, text="Load Data", command=load_selected_transaction).pack(pady=5)

    # Save changes made to the transaction
    def save_edited_transaction():
        try:
            index = int(selected_transaction_var.get().split(".")[0]) - 1
            edited_furniture_name = furniture_name_var.get()
            edited_code = furniture_code_var.get()
            edited_stock = int(stock_var.get())  # Ensure stock is an integer
            edited_price = price_var.get()

            # Update the transaction data
            transactions[index]["furniture"] = edited_furniture_name
            transactions[index]["price"] = edited_price

            # Update furniture database as well
            if edited_code in furniturecodes:
                furniturenames[furniturecodes.index(edited_code)] = edited_furniture_name
                persediaan[edited_code] = edited_stock
            else:
                messagebox.showerror("Error", "Invalid furniture code.")

            messagebox.showinfo("Edit Successful", "Transaction has been successfully updated.")
            edit_window.destroy()  # Close the edit window after saving

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data for all fields.")

    Button(edit_window, text="Save Changes", command=save_edited_transaction).pack(pady=20)

# Usage: Attach the new edit_transaction function to the help menu.
    help_menu.add_command(label="Edit Transaction", command=edit_transaction)


def delete_transaction():
    if not transactions:
        messagebox.showinfo("Delete Transaction", "No transactions to delete.")
        return

    # Membuat list pilihan transaksi berdasarkan deskripsi (nama furniture dan rincian lain)
    transaction_options = [f"{i+1}. {t['furniture']} - {t['size']} - {t['color']} - {t['price']}" for i, t in enumerate(transactions)]
    
    # Membuka jendela dialog untuk memilih transaksi yang ingin dihapus
    delete_window = Toplevel(root)
    delete_window.title("Delete Transaction")
    delete_window.geometry("400x200")

    Label(delete_window, text="Pilih transaksi yang ingin dihapus:").pack(pady=10)
    
    selected_transaction_var = StringVar()
    selected_transaction_var.set(transaction_options[0])  # Default ke transaksi pertama

    # Dropdown menu untuk memilih transaksi
    transaction_menu = OptionMenu(delete_window, selected_transaction_var, *transaction_options)
    transaction_menu.pack(pady=10)

    # Fungsi untuk menghapus transaksi yang dipilih
    def confirm_delete():
        selected_index = int(selected_transaction_var.get().split(".")[0]) - 1
        selected_transaction = transactions[selected_index]

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Apakah Anda yakin ingin menghapus transaksi ini?\n{selected_transaction['furniture']} - {selected_transaction['size']} - {selected_transaction['color']} - {selected_transaction['price']}"
        )

        if confirm:
            transactions.pop(selected_index)  # Hapus transaksi yang dipilih
            messagebox.showinfo("Delete Successful", "Transaksi berhasil dihapus.")
            delete_window.destroy()  # Tutup dialog setelah transaksi dihapus

    Button(delete_window, text="Delete Transaction", command=confirm_delete).pack(pady=20)


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
file_menu.add_command(label="Open Transaction", command=open_transactions)
file_menu.add_command(label="Save Transactions", command=save_transactions_to_file)  # Added this line
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Help Menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="Add Furniture", command=add_furniture)
help_menu.add_command(label="Add Color", command=add_color)
help_menu.add_command(label="Add Size", command=add_size)  
help_menu.add_command(label="Delete Transaction", command=delete_transaction)
menubar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the root window
root.config(menu=menubar)

# Show the login frame initially
show_frame(login_frame)

# Start the GUI loop
root.mainloop()
