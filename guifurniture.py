from tkinter import *
from tkinter import messagebox

app = Tk()
app.title('TORICA FURNITURE STORE')

# Variable
items = [
    {'name': 'Lampu', 'price': 300000, 'color': 'Putih', 'size': 'Medium', 'quantity': 0},
    {'name': 'Meja', 'price': 450000, 'color': 'Coklat', 'size': 'Besar', 'quantity': 0},
    {'name': 'Kursi', 'price': 200000, 'color': 'Hitam', 'size': 'Kecil', 'quantity': 0},
    {'name': 'Lemari', 'price': 1500000, 'color': 'Biru', 'size': 'Besar', 'quantity': 0}
]

cart = []  # List yang ada di data
selected_item = StringVar()
selected_price = StringVar()
selected_color = StringVar()
selected_size = StringVar()
quantity_var = StringVar(value='0')
tekstotal = StringVar(value='0')

# Fungsi untuk menghitung total beli 
def totalbeli():
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    tekstotal.set(str(total))

# Fungsi untuk memilih item dari list
def select_item(event):
    selected = item_listbox.curselection()
    if selected:
        index = selected[0]
        selected_item.set(items[index]['name'])
        selected_price.set(items[index]['price'])
        selected_color.set(items[index]['color'])
        selected_size.set(items[index]['size'])
        quantity_var.set(str(items[index]['quantity']))  # Show current quantity

# Function to add selected item with the specified quantity to the cart
def add_item():
    quantity = int(quantity_var.get())
    selected = item_listbox.curselection()
    if selected:
        index = selected[0]
        if quantity > 0:
            items[index]['quantity'] += quantity
            totalbeli()
            update_item_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid quantity")
    else:
        messagebox.showwarning("Selection Error", "Please select an item")

# Fungsi untuk menambah barang yang di pilih ke keranjang 
def add_to_cart():
    selected = item_listbox.curselection()
    if selected:
        index = selected[0]
        quantity = int(quantity_var.get())
        if quantity > 0:
            cart.append({'name': items[index]['name'], 'price': items[index]['price'], 'quantity': quantity})
            messagebox.showinfo("Success", f"Added {quantity} {items[index]['name']} to cart.")
            update_cart_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid quantity")
    else:
        messagebox.showwarning("Selection Error", "Please select an item")

# Fungsi untuk update item di list display 
def update_item_list():
    for widget in item_list_frame.winfo_children():
        widget.destroy()
    
    for item in items:
        Label(item_list_frame, text=f"{item['name']} - Rp. {item['price']} - Color: {item['color']} - Size: {item['size']} - Quantity: {item['quantity']}", bg='darkblue', fg='white').pack(anchor='w')

# Fungsi untuk update display keranjang 
def update_cart_list():
    for widget in cart_list_frame.winfo_children():
        widget.destroy()
    
    for item in cart:
        Label(cart_list_frame, text=f"{item['name']} - Rp. {item['price']} - Quantity: {item['quantity']}", bg='darkblue', fg='white').pack(anchor='w')

# Function to edit the quantity of the selected item
def edit_item():
    quantity = int(quantity_var.get())
    selected = item_listbox.curselection()
    if selected:
        index = selected[0]
        if quantity >= 0:  # Allow setting to zero or more
            items[index]['quantity'] = quantity
            totalbeli()
            update_item_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid quantity")
    else:
        messagebox.showwarning("Selection Error", "Please select an item")

# Function to clear input fields
def clear():
    selected_item.set('')
    selected_price.set('')
    selected_color.set('')
    selected_size.set('')
    quantity_var.set('0')
    for widget in item_list_frame.winfo_children():
        widget.destroy()
    tekstotal.set('0')
    for item in items:
        item['quantity'] = 0  # Reset quantities to zero
    cart.clear()  # Clear the cart

app.geometry('750x600')
app.configure(bg='darkblue')

