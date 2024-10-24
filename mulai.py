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
