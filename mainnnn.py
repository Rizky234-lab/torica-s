from fungsi import Warna, Ukuran, Furniture, Transaction, datetime

def main():
    # Create instances of the classes
    warna_handler = Warna()
    ukuran_handler = Ukuran()
    furniture_handler = Furniture()
    transaksi_handler = Transaction()

    # Initialize a list to store transactions
    transactions = []

    # Main loop for the application
    while True:
        print("\n (∩˃o˂∩)★")
        print(" Torica Furniture Store .•*¨*•.¸¸♪=")
        print("1. View Data")
        print("2. Add New Data")
        print("3. Delete Data")
        print("4. Edit Data")
        print("5. Add New Transaction")
        print("6. Delete Transaction")
        print("7. View Transaction")
        print("8. Exit")
        pilihan = input("Enter your choice (1-8): ")

        if pilihan == '1':  # View data
            print("\n=== View Data ===")
            print("1. View Color Data")
            print("2. View Size Data")
            print("3. View Furniture Data")
            pilihan_lihat = input("Enter your choice (1-3): ")
            if pilihan_lihat == '1':
                    data_dict = warna_handler.list_warna()
                    print("\nColor Data:")
                    print(data_dict)
                
            elif pilihan_lihat == '2':
                    data_dict = ukuran_handler.list_ukuran()
                    print("\nSize Data:")
                    print(data_dict)

            elif pilihan_lihat == '3':
                    data_dict = furniture_handler.list_furniture()
                    print(data_dict)
            else:
                    print("Invalid choice.")

        elif pilihan == '2':  # Add new data
            print("\n=== Add New Data ===")
            print("1. Add Color")
            print("2. Add Size")
            print("3. Add Furniture")
            pilihan_tambah = input("Enter your choice (1-3): ")
        
            if pilihan_tambah == '1':
                    new_data= input("Enter new color: ")
                    warna_handler.tambah_warna(new_data)
                    print(f"Color '{new_data}' has been successfully added.")
                
            elif pilihan_tambah == '2':
                    new_data = input("Enter new size: ")
                    ukuran_handler.tambah_ukuran(new_data)
                    print(f"Size '{new_data}' has been successfully added.")
                
            elif pilihan_tambah == '3':
                    new_data = input("Enter new furniture: ")
                    furniture_handler.tambah_furniture(new_data)
                    print(f"Furniture '{new_data}' has been successfully added.")
                
            else:
                    print("Invalid choice.")

        elif pilihan == '3':  # Delete data
            print("\n Delete Data -ˋˏ✄┈┈┈┈")
            print("1. Delete Color")
            print("2. Delete Size")
            print("3. Delete Furniture")
            pilihan_hapus = input("Enter your choice (1-3): ")

            if pilihan_hapus == '1':
                    id_hapus = input("Enter Color ID to delete: ")
                    if warna_handler.hapus_warna(id_hapus):
                        print(f"Color with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Color ID '{id_hapus}' not found.")
                
            elif pilihan_hapus == '2':
                    id_hapus = input("Enter Size ID to delete: ")
                    if ukuran_handler.hapus_ukuran(id_hapus):
                        print(f"Size with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Size ID '{id_hapus}' not found.")
                
            elif pilihan_hapus == '3':
                    id_hapus = input("Enter Furniture ID to delete: ")
                    if furniture_handler.hapus_furniture(id_hapus):
                        print(f"Furniture with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Furniture ID '{id_hapus}' not found.")
                
            else:
                    print("Invalid choice.")
        
        elif pilihan == '4':  # Edit Data
            print("\n=== Edit Data ===")
            print("1. Edit Color")
            print("2. Edit Size")
            print("3. Edit Furniture")
            pilihan_edit = input("Enter your choice (1-3): ")

            if pilihan_edit == '1':
                    id_edit = input("Enter Color ID to edit: ")
                    if warna_handler.edit_warna(id_edit):
                        print(f"Color with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Color ID '{id_edit}' not found.")
                
            elif pilihan_edit == '2':
                    id_edit = input("Enter Size ID to edit: ")
                    if ukuran_handler.edit_ukuran(id_edit):
                        print(f"Size with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Size ID '{id_edit}' not found.")
                
            elif pilihan_edit == '3':
                    id_edit = input("Enter Furniture ID to edit: ")
                    if furniture_handler. edit_furniture(id_edit):
                        print(f"Furniture with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Furniture ID '{id_edit}' not found.")
                
            else:
                    print("Invalid choice.")
           
        elif pilihan == '5':  # Add new transaction
            print("\n=== Add New Transaction ===")
            furniture_name = input("Add the furniture: ")
            furniture_code = input("Add the code furniture: ")
            selected_color = input("Add the color: ")
            selected_size = input("Add the size: ")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
                # Changed this line to pass only 3 arguments (plus self makes 4)
            transaksi_id = transaksi_handler.tambah_transaksi(furniture_name, selected_color, selected_size)

            new_transaction = {
                    "timestamp": timestamp,
                    "furniture": furniture_name,
                    "color": selected_color,
                    "size": selected_size,
                    "id": transaksi_id  # Store the ID returned from database
                    }
            transactions.append(new_transaction)
            print(f"Transaction successfully added: {new_transaction}")
            
        
        elif pilihan == '6':  # Delete transaction
            print("\n=== Delete Transaction ===")
            if transactions:
                print("Available Transactions:")
                for idx, trans in enumerate(transactions):
                    print(f"{idx}. {trans}")
                
                try:
                    index = int(input("Enter transaction index to delete: "))
                    if 0 <= index < len(transactions):
                        deleted_transaction = transactions.pop(index)
                        print(f"Transaction successfully deleted: {deleted_transaction}")
                    else:
                        print("Invalid transaction index.")
                except ValueError:
                    print("Please enter a valid index number.")
            else:
                print("No transactions available.")

        elif pilihan == '7':  # View transactions
            print("\n=== Transaction History ===")
            if transactions:
                for idx, transaction in enumerate(transactions):
                    print(f"\nTransaction {idx}:")
                    print(f"ID: {transaction['id']}")
                    print(f"Timestamp: {transaction['timestamp']}")
                    print(f"Furniture: {transaction['furniture']}")
                    print(f"Color: {transaction['color']}")
                    print(f"Size: {transaction['size']}")
            else:
                print("No transactions available.")

        elif pilihan == '8':  # Exit
            print("\nThank you for visiting our store ♪¸¸.•*¨*•.!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
