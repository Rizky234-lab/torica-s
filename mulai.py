from tkinter import *
from tkinter import Tk, Button, Toplevel, messagebox, StringVar, Label, Entry, OptionMenu, ttk, OptionMenu,filedialog, BOTH
from datetime import date  
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import shutil
import os
from datetime import date, datetime
import pandas as pd

# Main application window
root = Tk()
root.geometry("700x400")
root.title("Torica Furniture Store")

# Flags
logged_in = True

# Initialize furniture "databases"
furniturecodes = ['1', '2', '3', '4', '5']
furniturenames = ['Sofa', 'Lemari', 'Kursi', 'Meja', 'Lampu']
cnames = StringVar(value=furniturenames)
harga = {'1': 500000, '2': 750000, '3': 250000, '4': 600000, '5': 150000}

# Color dictionary for furniture colors
colornames = ['Merah', 'Biru','Kuning','Hijau']
colorcodes = ['1','2','3','4']
sizenames = ['Small', 'Medium','Big']
sizecodes = ['1','2','3'] 

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
furniture_management_frame = Frame(root, bg="white")
color_management_frame = Frame(root, bg="white")
size_management_frame = Frame(root, bg="white")

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
def showPrice(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        code = furniturecodes[idx]
        name = furniturenames[idx]
        pricedata = harga[code]
        statusmsg.set(f"Persediaan {name} ({code}) {pricedata}")
    sentmsg.set('')  # Clear sent message

def calculate_price(furniture_code, size):
    """Calculate the price of a furniture item based on its code and size."""
    base_price = harga.get(furniture_code)  # Get base price from harga
    size_increase = {"small": 0, "medium": 200_000, "big": 500_000}  # Size-based increase
 
    # Calculate final price
    return base_price + size_increase.get(size, 0)

# Function to handle date selection
def get_selected_date():
    selected_date = cal.get_date()
        # Filter transactions for the selected date
    filtered_transactions = [
            t for t in transactions 
            if t['timestamp'].startswith(selected_date)
        ]
        
        # Show transactions for selected date
    if filtered_transactions:
            trans_window = Toplevel(root)
            trans_window.title(f"Transactions for {selected_date}")
            trans_window.geometry("700x300")
            
            # Create Treeview
            columns = ("timestamp", "details")
            tree = ttk.Treeview(trans_window, columns=columns, show="headings", height=10)
            tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
            
            # Define headings
            tree.heading("timestamp", text="Timestamp")
            tree.heading("details", text="Transaction details")
            
            # Insert filtered transactions
            for trans in filtered_transactions:
                tree.insert("", "end", values=(
                    trans["timestamp"],
                    f"Transaction details"
                ))
                  
    else:
            messagebox.showinfo("No Transactions", 
                              f"No transactions found for {selected_date}")
    
# --- Main Menu Setup ---
def setup_main_menu():
    # Transaction Date
    Label(main_frame, text="Transaction Date:", bg="white").grid(row=0, column=3, pady=5, padx=5)
    global transaction_date
    today = date.today()
    transaction_date = DateEntry(main_frame, selectmode='day', 
                               year=today.year, 
                               month=today.month,
                               day=today.day,
                               width=20)
    transaction_date.grid(row=1, column=3, pady=5, padx=5)

setup_main_menu()

def sendtocart(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = furniturenames[idx]
        code = furniturecodes[idx]
        color = selected_color.get()
        size = selected_size.get()
        
        if harga[code] > 0 and color and size:
            price = calculate_price(code, size)
            
            # Get the selected date from the DateEntry widget
            selected_date = transaction_date.get_date()
            timestamp = selected_date.strftime('%Y-%m-%d')
            
            transaction = {
                "timestamp": timestamp,
                "furniture": name,
                "color": colornames[color.index(color)],
                "size": size.capitalize(),
                "price": f"Rp. {price:,.0f}"
            }
            
            # Save transaction to file
            save_transaction_to_file(transaction)
            
            sentmsg.set(f"Your transaction is: {transaction['furniture']} ({transaction['size']} - {transaction['color']}) {transaction['price']}")
            statusmsg.set(f"Persediaan {name} ({code}) {harga[code]:,.0f}")
        else:
            if harga[code] <= 0:
                sentmsg.set(f"Sorry, stok {name} sudah habis!")
            else:
                sentmsg.set("Please pick the color and size.")

# Initial frame
for frame in (login_frame, welcome_frame, main_frame, furniture_management_frame, color_management_frame, size_management_frame):
    frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
# Start with login frame
show_frame(login_frame)

def calculate_total_price():
    """Calculate the total price of all transactions."""
    if not transactions:
            messagebox.showinfo("Total Price", "No transactions available.")
            return

    total = sum(
        int(trans["price"].replace("Rp. ", "").replace(",", ""))
        for trans in transactions
    )
    messagebox.showinfo("Total Price", f"The total price is: Rp. {total:,.0f}")

def open_transactions():
    """Open a new window to display transactions from file with date filtering."""
    # Read transactions from file
    transactions = read_transactions_from_file()
    
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions available.")
        return

    trans_window = Toplevel(root)
    trans_window.title("All Transactions")
    trans_window.geometry("800x600")  # Increased height for chart

    # Create main frame
    main_frame = Frame(trans_window)
    main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Create filter frame
    filter_frame = Frame(main_frame)
    filter_frame.pack(fill=X, pady=5)

    # Add date range filters
    Label(filter_frame, text="Start Date:").pack(side=LEFT, padx=5)
    start_cal = DateEntry(filter_frame, width=12)
    start_cal.pack(side=LEFT, padx=5)

    Label(filter_frame, text="End Date:").pack(side=LEFT, padx=5)
    end_cal = DateEntry(filter_frame, width=12)
    end_cal.pack(side=LEFT, padx=5)

    # Define Treeview columns
    columns = ("timestamp", "furniture", "color", "size", "price")

    # Create Treeview with scrollbar
    tree_frame = Frame(main_frame)
    tree_frame.pack(expand=True, fill=BOTH)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    tree.pack(side=LEFT, expand=True, fill=BOTH)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Define headings for each column
    tree.heading("timestamp", text="Timestamp")
    tree.heading("furniture", text="Furniture")
    tree.heading("color", text="Color")
    tree.heading("size", text="Size")
    tree.heading("price", text="Price")

    # Set column widths
    tree.column("timestamp", width=150)
    tree.column("furniture", width=150)
    tree.column("color", width=100)
    tree.column("size", width=100)
    tree.column("price", width=100)

    def apply_filter():
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        
        # Validate date range
        if end_date < start_date:
            messagebox.showerror("Invalid Date Range", "End date cannot be before start date")
            return
            
        # Filter transactions
        filtered_transactions = [
            t for t in transactions 
            if start_date <= datetime.strptime(t['timestamp'], '%Y-%m-%d').date() <= end_date
        ]
        
        if not filtered_transactions:
            messagebox.showinfo("No Transactions", 
                              f"No transactions found between {start_date} and {end_date}")
            return
            
        # Insert filtered transactions
        for trans in filtered_transactions:
            tree.insert("", "end", values=(
                trans["timestamp"],
                trans["furniture"],
                trans["color"],
                trans["size"],
                trans["price"]
            ))

        # Update total for filtered transactions
        calculate_total_price(filtered_transactions)
        visualize_transactions(filtered_transactions)  # Update chart

    def reset_filter():
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Reset calendar widgets to today
        today = date.today()
        start_cal.set_date(today)
        end_cal.set_date(today)
        
        # Show all transactions
        for trans in transactions:
            tree.insert("", "end", values=(
                trans["timestamp"],
                trans["furniture"],
                trans["color"],
                trans["size"],
                trans["price"]
            ))
        
        # Update total for all transactions
        calculate_total_price(transactions)
        visualize_transactions(transactions)  # Update chart

    def calculate_total_price(trans_list):
        total = 0
        for trans in trans_list:
            # Extract numeric value from price string (remove "Rp. " and ",")
            price_str = trans["price"].replace("Rp. ", "").replace(",", "")
            try:
                total += float(price_str)
            except ValueError:
                continue
        total_label.config(text=f"Total Price: Rp. {total:,.0f}")

    # Add filter buttons
    button_frame = Frame(main_frame)
    button_frame.pack(fill=X, pady=5)

    Button(button_frame, text="Apply Filter", command=apply_filter).pack(side=LEFT, padx=5)
    Button(button_frame, text="Reset Filter", command=reset_filter).pack(side=LEFT, padx=5)

    # Add total price label
    total_label = Label(main_frame, text="Total Price: Rp. 0", font=("Arial", 10, "bold"))
    total_label.pack(pady=10)

    # Create a frame for the chart
    chart_frame = Frame(main_frame)
    chart_frame.pack(expand=True, fill=BOTH)

    def visualize_transactions(trans_list):
        """
        Create a line chart visualization based on the provided transaction list.
        """
        # Convert to DataFrame
        df = pd.DataFrame(trans_list)
        
        # Check the columns in the DataFrame
        print("DataFrame columns:", df.columns)
        
        # Ensure the timestamp column exists
        if 'timestamp' not in df.columns:
            raise ValueError("DataFrame must contain a 'timestamp' column")
        
        # Print the first few entries to inspect the format
        print("Sample timestamps:", df['timestamp'].head())

        # Convert timestamp column to datetime with a specified format
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d', errors='coerce')
        except Exception as e:
            print("Error parsing dates:", e)

        # Check for NaT values after conversion
        if df['timestamp'].isnull().any():
            print("Some dates could not be parsed:", df[df['timestamp'].isnull()])

        # Extract month from timestamp
        df['month'] = df['timestamp'].dt.to_period('M')

        #extract day from timestamp 
        df['day'] = df['timestamp'].dt.to_period('D')

        # Convert the price column to numeric
        df['price'] = df['price'].replace("Rp. ", "", regex=True).replace(",", "", regex=True).astype(float)

        # Group by month and calculate average transaction
        monthly_avg = df.groupby('month')['price'].mean().reset_index()

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 4))

        # Plot line chart
        ax.plot(monthly_avg['month'].astype(str), monthly_avg['price'], marker='o')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Transaction (Rp)')
        ax.set_title('Monthly Average Transaction Amount')
        plt.xticks(rotation=0)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Clear previous chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # Embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill=BOTH)

        canvas.draw()
    # Initially display all transactions and chart
    reset_filter()
    
def save_transaction_to_file(transaction):
    """Save a single transaction to data_transaksi.txt"""
    try:
        with open('data_transaksi.txt', 'a') as file:
            # Convert transaction dict to a line of text
            line = f"{transaction['timestamp']}|{transaction['furniture']}|{transaction['color']}|{transaction['size']}|{transaction['price']}\n"
            file.write(line)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")

def read_transactions_from_file():
    """Read all transactions from data_transaksi.txt"""
    transactions = []
    try:
        with open('data_transaksi.txt', 'r') as file:
            for line in file:
                # Split line into components
                data = line.strip().split('|')
                if len(data) == 5:  # Ensure we have all required fields
                    transaction = {
                        "timestamp": data[0],
                        "furniture": data[1],
                        "color": data[2],
                        "size": data[3],
                        "price": data[4]
                    }
                    transactions.append(transaction)
    except FileNotFoundError:
        # Create file if it doesn't exist
        open('data_transaksi.txt', 'w').close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read transactions: {str(e)}")
    
    return transactions

def furniture_actions():
    """Provide a comprehensive furniture management dialog."""
    if not logged_in:
        messagebox.showerror("Access Denied", "You must log in first!")
        return

    # Create a dialog window for furniture actions
    furniture_action_window = Toplevel(root)
    furniture_action_window.title("Furniture Management")
    furniture_action_window.geometry("300x250")

    # Create buttons for different furniture actions
    Button(furniture_action_window, text="View Furniture", command=view_furniture).pack(pady=5)
    Button(furniture_action_window, text="Add Furniture", command=add_furniture).pack(pady=5)
    Button(furniture_action_window, text="Edit Furniture", command=edit_furniture).pack(pady=5)
    Button(furniture_action_window, text="Delete Furniture", command=open_delete_furniture).pack(pady=5)
  
def view_furniture():
    """Open the furniture view window."""
    furniture_window = Toplevel(root)
    furniture_window.title("Furniture List")
    furniture_window.geometry("500x300")

    columns = ("Code", "Name", "Price")
    tree = ttk.Treeview(furniture_window, columns=columns, show="headings")
    tree.heading("Code", text="Code")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")

    # Insert furniture data
    for i, name in enumerate(furniturenames):
        code = furniturecodes[i]
        price = harga.get(code, 0)
        tree.insert("", "end", values=(code, name, f"Rp. {price:,.0f}"))

    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def add_furniture():
    """Open the add furniture window."""
    add_window = Toplevel(root)
    add_window.title("Add New Furniture")
    add_window.geometry("300x200")

    furniture_name_var = StringVar()
    price_data_var = StringVar()

    Label(add_window, text="Furniture Name:").pack(pady=5)
    Entry(add_window, textvariable=furniture_name_var).pack(pady=5)

    Label(add_window, text="Price (Rp):").pack(pady=5)
    Entry(add_window, textvariable=price_data_var).pack(pady=5)

    def save_furniture():
        code = str(len(furniturecodes) + 1)
        name = furniture_name_var.get().strip()
        price = price_data_var.get().strip()

        if name and code.isdigit():
            furniturecodes.append(code)
            furniturenames.append(name)
            harga[code] = int(price)

            with open("data_furniture.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", f"Furniture '{name}' has been added!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "Please provide valid inputs.")

    Button(add_window, text="Save", command=save_furniture).pack(pady=10)

def edit_furniture():
    """Open the edit furniture window."""
    if not furniturenames:
        messagebox.showinfo("Edit Furniture", "No furniture to edit.")
        return

    edit_window = Toplevel(root)
    edit_window.title("Edit Furniture")
    edit_window.geometry("400x300")

    selected_furniture_var = StringVar()
    furniture_options = [f"{code}. {name}" for code, name in zip(furniturecodes, furniturenames)]
    selected_furniture_var.set(furniture_options[0])

    Label(edit_window, text="Select Furniture to Edit:").pack(pady=5)
    furniture_menu = OptionMenu(edit_window, selected_furniture_var, *furniture_options)
    furniture_menu.pack(pady=5)

    name_var = StringVar()
    price_var = StringVar()

    Label(edit_window, text="New Furniture Name:").pack(pady=5)
    Entry(edit_window, textvariable=name_var).pack(pady=5)

    Label(edit_window, text="New Price (Rp):").pack(pady=5)
    Entry(edit_window, textvariable=price_var).pack(pady=5)

    def save_furniture_changes():
        selected_item = selected_furniture_var.get()
        code = selected_item.split(".")[0]
        index = furniturecodes.index(code)

        new_name = name_var.get().strip()
        new_price = price_var.get().strip()

        if new_name and new_price.isdigit():
            furniturenames[index] = new_name
            harga[code]=int(new_price)

            with open("data_furniture.txt", "w") as file:
                for code, name,  in zip(furniturecodes, furniturenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", "Furniture updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid name.")

    Button(edit_window, text="Save Changes", command=save_furniture_changes).pack(pady=10)

def open_delete_furniture():
    """Open the delete furniture window."""
    if not furniturenames:
        messagebox.showinfo("Delete Furniture", "No furniture to delete.")
        return

    delete_window = Toplevel(root)
    delete_window.title("Delete Furniture")
    delete_window.geometry("400x200")

    selected_furniture_var = StringVar()
    furniture_options = [f"{code}. {name}" for code, name in zip(furniturecodes, furniturenames)]
    selected_furniture_var.set(furniture_options[0])

    Label(delete_window, text="Select Furniture to Delete:").pack(pady=10)
    furniture_menu = OptionMenu(delete_window, selected_furniture_var, *furniture_options)
    furniture_menu.pack(pady=10)

    def confirm_delete():
        selected_item = selected_furniture_var.get()
        code = selected_item.split(".")[0]
        index = furniturecodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete {furniturenames[index]}?"
        )
        if confirm:
            furniturenames.pop(index)
            furniturecodes.pop(index)
            del harga[code]

            save_furniture_data()
            with open("data_furniture.txt", "w") as file:
                for code, name in zip(furniturecodes, furniturenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "Furniture item deleted.")
            delete_window.destroy()

    Button(delete_window, text="Delete Furniture", command=confirm_delete).pack(pady=20)

def save_furniture_data():
    """Save furniture data to a text file."""
    with open("data_furniture.txt", "w") as file:
        for code, name in zip(furniturecodes, furniturenames):
            file.write(f"{code}:{name}:{harga.get(code, 0)}\n")

def load_furniture_data():
    """Load furniture data from a text file."""
    global furniturecodes, furniturenames, harga
    try:
        with open("data_furniture.txt", "r") as file:
            furniturecodes.clear()
            furniturenames.clear()
            harga.clear()
            
            for line in file:
                code, name, price = line.strip().split(":")
                furniturecodes.append(code)
                furniturenames.append(name)
                harga[code] = int(price)
    except FileNotFoundError:
        pass

def color_actions():
    """Provide a comprehensive color management dialog."""
    color_action_window = Toplevel(root)
    color_action_window.title("Color Management")
    color_action_window.geometry("300x250")

    Button(color_action_window, text="View Colors", command=view_color).pack(pady=5)
    Button(color_action_window, text="Add Color", command=add_color).pack(pady=5)
    Button(color_action_window, text="Edit Color", command=edit_color).pack(pady=5)
    Button(color_action_window, text="Delete Color", command=open_delete_color).pack(pady=5)

def view_color():
    """Open the color view window."""
    color_window = Toplevel(root)
    color_window.title("Color List")
    color_window.geometry("500x300")

    columns = ("Code", "Name")
    tree = ttk.Treeview(color_window, columns=columns, show="headings")
    tree.heading("Code", text="Code")
    tree.heading("Name", text="Name")

    for code, name in zip(colorcodes, colornames):
        tree.insert("", "end", values=(code, name))
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def add_color():
    """Open the add color window."""
    add_color_window = Toplevel(root)
    add_color_window.title("Add New Color")
    add_color_window.geometry("300x200")

    color_name_var = StringVar()

    Label(add_color_window, text="Color Name:").pack(pady=5)
    Entry(add_color_window, textvariable=color_name_var).pack(pady=5)

    def save_color():
        code = str(len(furniturecodes) + 1)
        name = color_name_var.get().strip()

        if name and code:
            colornames.append(name)
            colorcodes.append(code)

            with open("data_warna.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", f"Color '{name}' has been added!")
            add_color_window.destroy()
        else:
            messagebox.showerror("Error", "Please provide valid inputs.")

    Button(add_color_window, text="Save", command=save_color).pack(pady=10)

def edit_color():
    """Open the edit color window."""
    if not colornames:
        messagebox.showinfo("Edit Color", "No colors to edit.")
        return

    edit_window = Toplevel(root)
    edit_window.title("Edit Color")
    edit_window.geometry("400x300")

    selected_color_var = StringVar()
    color_options = [f"{code}. {name}" for code, name in zip(colorcodes, colornames)]
    selected_color_var.set(color_options[0])

    Label(edit_window, text="Select Color to Edit:").pack(pady=5)
    OptionMenu(edit_window, selected_color_var, *color_options).pack(pady=5)

    name_var = StringVar()

    Label(edit_window, text="New Color Name:").pack(pady=5)
    Entry(edit_window, textvariable=name_var).pack(pady=5)

    def save_color_changes():
        selected_option = selected_color_var.get()
        code = selected_option.split(".")[0]
        index = colorcodes.index(code)
        new_name = name_var.get().strip()

        if new_name:
            colornames[index] = new_name

            with open("data_warna.txt", "w") as file:
                for code, name in zip(colorcodes, colornames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", "Color updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid name.")

    Button(edit_window, text="Save Changes", command=save_color_changes).pack(pady=10)

def open_delete_color():
    """Open the delete color window."""
    if not colornames:
        messagebox.showinfo("Delete Color", "No colors to delete.")
        return

    delete_window = Toplevel(root)
    delete_window.title("Delete Color")
    delete_window.geometry("400x200")

    selected_color_var = StringVar()
    color_options = [f"{code}. {name}" for code, name in zip(colorcodes, colornames)]
    selected_color_var.set(color_options[0])

    Label(delete_window, text="Select Color to Delete:").pack(pady=10)
    OptionMenu(delete_window, selected_color_var, *color_options).pack(pady=10)

    def confirm_delete():
        selected_item = selected_color_var.get()
        code = selected_item.split(".")[0]
        index = colorcodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete {colornames[index]}?"
        )

        if confirm:
            colornames.pop(index)
            colorcodes.pop(index)

            save_color_data()
            with open("data_warna.txt", "w") as file:
                for code, name in zip(colorcodes, colornames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "Color item deleted.")
            delete_window.destroy()

    Button(delete_window, text="Delete Color", command=confirm_delete).pack(pady=20)

def save_color_data():
    """Save color data to a text file."""
    with open("data_warna.txt", "w") as file:
        for code, name in zip(colorcodes, colornames):
            file.write(f"{code}:{name}\n")

def load_color_data():
    """Load color data from a text file."""
    global colorcodes, colornames
    try:
        with open("data_warna.txt", "r") as file:
            colorcodes.clear()
            colornames.clear()
            
            for line in file:
                code, name = line.strip().split(":")
                colorcodes.append(code)
                colornames.append(name)
    except FileNotFoundError:
        pass

def size_actions():
    """Provide a comprehensive size management dialog."""
    size_action_window = Toplevel(root)
    size_action_window.title("Size Management")
    size_action_window.geometry("300x250")

    Button(size_action_window, text="View Size", command=view_size).pack(pady=5)
    Button(size_action_window, text="Add Size", command=add_size).pack(pady=5)
    Button(size_action_window, text="Edit Size", command=edit_size).pack(pady=5)
    Button(size_action_window, text="Delete Size", command=open_delete_size).pack(pady=5)

def view_size():
    """Open the size view window."""
    size_window = Toplevel(root)
    size_window.title("Size List")
    size_window.geometry("500x300")

    columns = ("Code", "Name")
    tree = ttk.Treeview(size_window, columns=columns, show="headings")
    tree.heading("Code", text="Code")
    tree.heading("Name", text="Name")
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    for code, name in zip(sizecodes, sizenames):
        tree.insert("", "end", values=(code, name))

def add_size():
    """Open the add size window."""
    add_size_window = Toplevel(root)
    add_size_window.title("Add New Size")
    add_size_window.geometry("300x200")

    size_code_var = StringVar()
    size_name_var = StringVar()

    Label(add_size_window, text="Size Code:").pack(pady=5)
    Entry(add_size_window, textvariable=size_code_var).pack(pady=5)

    Label(add_size_window, text="Display Name:").pack(pady=5)
    Entry(add_size_window, textvariable=size_name_var).pack(pady=5)

    def save_size():
        code = size_code_var.get().strip()
        name = size_name_var.get().strip()

        if code and name:
            sizecodes.append(code)
            sizenames.append(name)

            with open("data_ukuran.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", f"Size '{name}' has been added!")
            add_size_window.destroy()
        else:
            messagebox.showerror("Error", "Please provide valid inputs.")

    Button(add_size_window, text="Save", command=save_size).pack(pady=10)

def edit_size():
    """Open the edit size window."""
    if not sizenames:
        messagebox.showinfo("Edit Size", "No size to edit.")
        return

    edit_window = Toplevel(root)
    edit_window.title("Edit Size")
    edit_window.geometry("400x300")

    selected_size_var = StringVar()
    size_options = [f"{code}. {name}" for code, name in zip(sizecodes, sizenames)]
    selected_size_var.set(size_options[0])

    Label(edit_window, text="Select Size to Edit:").pack(pady=5)
    OptionMenu(edit_window, selected_size_var, *size_options).pack(pady=5)

    name_var = StringVar()
    Label(edit_window, text="New Size Name:").pack(pady=5)
    Entry(edit_window, textvariable=name_var).pack(pady=5)

    def save_changes():
        selected_option = selected_size_var.get()
        code = selected_option.split(".")[0]
        index = sizecodes.index(code)
        new_name = name_var.get().strip()

        if new_name:
            sizenames[index] = new_name

            with open("data_ukuran.txt", "w") as file:
                for code, name in zip(sizecodes, sizenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Success", "Size updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid name.")

    Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

def open_delete_size():
    """Open the delete size window."""
    if not sizenames:
        messagebox.showinfo("Delete Size", "No size to delete.")
        return

    delete_window = Toplevel(root)
    delete_window.title("Delete Size")
    delete_window.geometry("400x200")

    selected_size_var = StringVar()
    size_options = [f"{code}. {name}" for code, name in zip(sizecodes, sizenames)]
    selected_size_var.set(size_options[0])

    Label(delete_window, text="Select Size to Delete:").pack(pady=10)
    OptionMenu(delete_window, selected_size_var, *size_options).pack(pady=10)

    def confirm_delete():
        selected_option = selected_size_var.get()
        code = selected_option.split(".")[0]
        index = sizecodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete '{sizenames[index]}'?"
        )

        if confirm:
            del sizecodes[index]
            del sizenames[index]
            save_size_data()
            with open("data_ukuran.txt", "w") as file:
                for code, name in zip(sizecodes, sizenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "Size item deleted.")
            delete_window.destroy()

    Button(delete_window, text="Delete", command=confirm_delete).pack(pady=20)

def save_size_data():
    """Save size data to a text file."""
    with open("data_ukuran.txt", "w") as file:
        for code, name in zip(sizecodes, sizenames):
            file.write(f"{code}:{name}\n")

def load_size_data():
    """Load size data from a text file."""
    global sizecodes, sizenames
    try:
        with open("data_ukuran.txt", "r") as file:
            sizecodes.clear()
            sizenames.clear()
            
            for line in file:
                code, name = line.strip().split(":")
                sizecodes.append(code)
                sizenames.append(name)
    except FileNotFoundError:
        pass

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
        price_var.set(harga[furniture_code_var.get()])
        price_var.set(selected_transaction["price"])

    # Button to load data of selected transaction
    Button(edit_window, text="Load Data", command=load_selected_transaction).pack(pady=5)

    # Save changes made to the transaction
    def save_edited_transaction():
        try:
            index = int(selected_transaction_var.get().split(".")[0]) - 1
            edited_furniture_name = furniture_name_var.get()
            edited_code = furniture_code_var.get()
            edited_price = int(price_var.get())  

            # Update the transaction data
            transactions[index]["furniture"] = edited_furniture_name
            transactions[index]["price"] = edited_price

            # Update furniture database as well
            if edited_code in furniturecodes:
                furniturenames[furniturecodes.index(edited_code)] = edited_furniture_name
                harga[edited_code] = edited_price
            else:
                messagebox.showerror("Error", "Invalid furniture code.")

            messagebox.showinfo("Edit Successful", "Transaction has been successfully updated.")
            edit_window.destroy()  # Close the edit window after saving

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data for all fields.")

    Button(edit_window, text="Save Changes", command=save_edited_transaction).pack(pady=20)

# Usage: Attach the new edit_transaction function to the help menu.
    data_mastering_menu.add_command(label="Edit Transaction", command=edit_transaction)

def delete_transaction():
    if not transactions:
        messagebox.showinfo("Delete Transaction", "No transactions to delete.")
        return

    # Create a list of transaction options based on description
    transaction_options = [f"{i+1}. {t['furniture']} - {t['size']} - {t['color']} - {t['price']}" for i, t in enumerate(transactions)]
    
    # Open a dialog window to select the transaction you want to delete
    delete_window = Toplevel(root)
    delete_window.title("Delete Transaction")
    delete_window.geometry("400x200")

    Label(delete_window, text="Choose the transaction you want to delete:").pack(pady=10)
    
    selected_transaction_var = StringVar()
    selected_transaction_var.set(transaction_options[0])  # Default ke transaksi pertama

    # Dropdown menu to select the transaction
    transaction_menu = OptionMenu(delete_window, selected_transaction_var, *transaction_options)
    transaction_menu.pack(pady=10)

    # Function to delete the selected transaction
    def confirm_delete():
        selected_index = int(selected_transaction_var.get().split(".")[0]) - 1
        selected_transaction = transactions[selected_index]

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Are you sure you want to delete the transaction ini?\n{selected_transaction['furniture']} - {selected_transaction['size']} - {selected_transaction['color']} - {selected_transaction['price']}"
        )

        if confirm:
            transactions.pop(selected_index)  # Delete the selected transaction
            messagebox.showinfo("Delete Successful", "Transaksi berhasil dihapus.")
            delete_window.destroy()  # Close the dialog after the transaction is deleted
    Button(delete_window, text="Delete Transaction", command=confirm_delete).pack(pady=20)

# Function to open the Image Editor
def open_image_editor():
    def create_root():
        editor_root = Toplevel(root)  # Open in a new window
        editor_root.title("Image Editor")
        editor_root.maxsize(900, 600)
        editor_root.config(bg="blue")
        return editor_root

    def create_frames(editor_root):
        left_frame = Frame(editor_root, width=200, height=400, bg='white')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = Frame(editor_root, width=650, height=400, bg='white')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        return left_frame, right_frame

    def create_left_frame_content(left_frame):
        Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)
        original_image_label = Label(left_frame)
        original_image_label.grid(row=1, column=0, padx=5, pady=5)
        return original_image_label

    def create_toolbar(left_frame, editor_state):
        tool_bar = Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        Button(tool_bar, text="Select Image", command=lambda: load_image(editor_state)).grid(row=1, column=0, padx=5, pady=10)
        
    def create_right_frame_content(right_frame):
        edited_image_label = Label(right_frame)
        edited_image_label.grid(row=0, column=0, padx=5, pady=5)
        return edited_image_label

    def display_image(img, label):
        img.thumbnail((300, 300))  # Resize image to fit the label
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection

    def load_image(editor_state):
        # Add variable to track sequence number
        if 'image_counter' not in editor_state:
            editor_state['image_counter'] = 1

        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
        # Create a 'save' directory if it doesn't already exist
            os.makedirs('.\\simpan', exist_ok=True)
        
        # Create file name with sequence number
            save_path = f".\\simpan\\gambar_{editor_state['image_counter']}.jpeg"
        
            editor_state['image'] = Image.open(file_path)
            shutil.copy2(file_path, save_path)
            display_image(editor_state['image'], editor_state['original_image_label'])
        
        # Raise the counter for the next file
            editor_state['image_counter'] += 1

    def save_addtional_photo(editor_state):
        if 'image' not in editor_state:
            messagebox.showwarning("Warning", "Please load an image first.")
            return
    
    file_path= filedialog.asksaveasfilename(
        defaultextension=".jpeg",
        filetypes=[("JPEG files", ".jpeg"), ("PNG files", ".png"), ("All files", ".")],
        initialdir=".\\simpan"
    )

    if file_path:
        try:
            os.makedirs(os.path.dirname(file_path),exist_ok=True)

            editor_state['image'].save(file_path)
            messagebox.showinfo("Success", f"Image saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    # Main Image Editor Function
    editor_root = create_root()

    # Create frames
    left_frame, right_frame = create_frames(editor_root)

    # Create left frame content
    original_image_label = create_left_frame_content(left_frame)

    # Create right frame content
    edited_image_label = create_right_frame_content(right_frame)

    # Define application state
    editor_state = {
        'image': None,
        'edited_image': None,
        'original_image_label': original_image_label,
        'edited_image_label': edited_image_label
    }

    # Create toolbar
    create_toolbar(left_frame, editor_state)

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
lbox.bind('<<ListboxSelect>>', showPrice)
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
file_menu.add_command(label="Open Image Editor", command=open_image_editor)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Data mastering Menu
data_mastering_menu = Menu(menubar, tearoff=0)
data_mastering_menu.add_command(label="Furniture", command= furniture_actions)
data_mastering_menu.add_command(label="Color", command= color_actions)
data_mastering_menu.add_command(label="Size", command= size_actions)  
data_mastering_menu.add_command(label="Delete Transaction", command=delete_transaction)
menubar.add_cascade(label="Data Mastering", menu=data_mastering_menu)

# Attach the menu bar to the root window
root.config(menu=menubar)

# Show the login frame initially
show_frame(login_frame)

# Start the GUI loop
root.mainloop()
