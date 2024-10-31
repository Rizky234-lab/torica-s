def main():
    while True:
        print("\n=== Menu ===")
        print("1. Manage Furniture")
        print("2. Manage Warna")
        print("3. Manage Ukuran")
        print("4. Manage Transaksi")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            manage_furniture()
        elif choice == '2':
            manage_warna()
        elif choice == '3':
            manage_ukuran()
        elif choice == '4':
            transaksi()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def manage_furniture():
    furniture_manager = id_furniture()
    
    while True:
        print("\n=== Manage Furniture ===")
        print("1. List Furniture")
        print("2. Add Furniture")
        print("3. Delete Furniture")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            furniture_list = furniture_manager.list_furniture()
            furniture_manager.tampilkan_data(furniture_list)
        elif choice == '2':
            id_ukuran = input("Enter ukuran ID: ")
            id_warna = input("Enter warna ID: ")
            try:
                result = furniture_manager.tambah_furniture(id_ukuran, id_warna)
                print(f"Furniture added: {result}")
            except ValueError as e:
                print(e)
        elif choice == '3':
            id_furniture = input("Enter furniture ID to delete: ")
            if furniture_manager.hapus_furniture(id_furniture):
                print("Furniture deleted.")
            else:
                print("Furniture ID not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_warna():
    warna_manager = id_warna()

    while True:
        print("\n=== Manage Warna ===")
        print("1. List Warna")
        print("2. Add Warna")
        print("3. Delete Warna")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            warna_list = warna_manager.list_warna()
            warna_manager.tampilkan_data(warna_list)
        elif choice == '2':
            warna = input("Enter warna: ")
            new_id = warna_manager.tambah_warna(warna)
            print(f"Warna added with ID: {new_id}")
        elif choice == '3':
            id_warna = input("Enter warna ID to delete: ")
            if warna_manager.hapus_warna(id_warna):
                print("Warna deleted.")
            else:
                print("Warna ID not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_ukuran():
    ukuran_manager = id_ukuran()

    while True:
        print("\n=== Manage Ukuran ===")
        print("1. List Ukuran")
        print("2. Add Ukuran")
        print("3. Delete Ukuran")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            ukuran_list = ukuran_manager.list_ukuran()
            ukuran_manager.tampilkan_data(ukuran_list)
        elif choice == '2':
            ukuran = input("Enter ukuran: ")
            new_id = ukuran_manager.tambah_ukuran(ukuran)
            print(f"Ukuran added with ID: {new_id}")
        elif choice == '3':
            id_ukuran = input("Enter ukuran ID to delete: ")
            if ukuran_manager.hapus_ukuran(id_ukuran):
                print("Ukuran deleted.")
            else:
                print("Ukuran ID not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def transaksi():
    transaksi = id_transaksi()

    while True:
        print("\n=== Manage Transaksi ===")
        print("1. List Transaksi")
        print("2. Add Transaksi")
        print("3. Delete Transaksi")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            transaksi_list = transaksi.list_transaksi()
            transaksi.tampilkan_data(transaksi_list)
        elif choice == '2':
            id_furniture = input("Enter furniture ID: ")
            jumlah = int(input("Enter quantity: "))
            try:
                result = transaksi_list(id_furniture, jumlah)
                print(result)
            except ValueError as e:
                print(e)
        elif choice == '3':
            id_transaksi = input("Enter transaction ID to delete: ")
            if transaksi.hapus_transaksi(id_transaksi):
                print("Transaction deleted.")
            else:
                print("Transaction ID not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
