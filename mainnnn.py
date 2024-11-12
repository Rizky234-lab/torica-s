from fungsi import Warna, Ukuran, Furniture, Transaksi

def main():
    # Create instances of the classes
    warna_handler = Warna()
    ukuran_handler = Ukuran()
    furniture_handler = Furniture()
    transaksi_handler = Transaksi()

    # Main loop for the application
    while True:
        print("\n==== Menu Utama ====")
        print("1. View Data")
        print("2. Add New Data")
        print("3. Delete Data")
        print("4. Add New Transaction")
        print("5. Delete Transaction")
        print("6. View Transaction")
        print("7. Exit")
        pilihan = input("Pilih opsi (1/2/3/4/5/6): ")

        if pilihan == '1':
            print("\n1. Lihat Data Warna")
            print("2. Lihat Data Ukuran")
            print("3. Lihat Data Furniture")
            pilihan_lihat = input("Pilihan: ")
            if pilihan_lihat == '1':
                data_dict = warna_handler.list_warna()
                print("\nData Warna yang dibaca adalah Dictionary:")
                print(data_dict)
            elif pilihan_lihat == '2':
                data_dict = ukuran_handler.list_ukuran()
                print("\nData Ukuran yang dibaca adalah Dictionary:")
                print(data_dict)
            elif pilihan_lihat == '3':
                data_dict = furniture_handler.list_furniture()
                print("\nData Furniture yang dibaca adalah Dictionary:")
                print(data_dict)
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '2':  # Add new data
            print("\nPilih File yang ingin ditambah: ")
            print("1. Data Warna")
            print("2. Data Ukuran")
            print("3. Data Furniture")
            pilihan_tambah = input("Pilihan: ")
            if pilihan_tambah == '1':
                new_data = input("Masukkan warna baru: ")
                warna_handler.tambah_warna(new_data)
                print(f"Warna '{new_data}' berhasil ditambahkan.")
            elif pilihan_tambah == '2':
                new_data = input("Masukkan ukuran baru: ")
                ukuran_handler.tambah_ukuran(new_data)
                print(f"Ukuran '{new_data}' berhasil ditambahkan.")
            elif pilihan_tambah == '3':
                new_data = input("Masukkan furniture baru: ")
                furniture_handler.tambah_furniture(new_data)
                print(f"Furniture '{new_data}' berhasil ditambahkan.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '3':  # Delete data
            print("\nPilih File yang ingin dihapus: ")
            print("1. Data Warna")
            print("2. Data Ukuran")
            print("3. Data Furniture")
            pilihan_hapus = input("Pilihan: ")
            if pilihan_hapus == '1':
                id_hapus = input("Masukkan ID warna yang akan dihapus: ")
                if warna_handler.hapus_warna(id_hapus):
                    print(f"Data warna dengan ID '{id_hapus}' berhasil dihapus.")
                else:
                    print(f"ID warna '{id_hapus}' tidak ditemukan.")
            elif pilihan_hapus == '2':
                id_hapus = input("Masukkan ID ukuran yang akan dihapus: ")
                if ukuran_handler.hapus_ukuran(id_hapus):
                    print(f"Data ukuran dengan ID '{id_hapus}' berhasil dihapus.")
                else:
                    print(f"ID ukuran '{id_hapus}' tidak ditemukan.")
            elif pilihan_hapus == '3':
                id_hapus = input("Masukkan ID furniture yang akan dihapus: ")
                if furniture_handler.hapus_furniture(id_hapus):
                    print(f"Data furniture dengan ID '{id_hapus}' berhasil dihapus.")
                else:
                    print(f"ID furniture '{id_hapus}' tidak ditemukan.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '4':  # Add new transaction
            print("\nTambah Data Transaksi: ")
            data_furniture = input("Masukkan ID furniture: ")
            jumlah = input("Masukkan jumlah: ")
            harga = input("Masukkan harga: ")
            try:
                transaksi_id = transaksi_handler.tambah_transaksi(data_furniture, jumlah, harga)
                print(f"Transaksi baru berhasil ditambahkan dengan ID: {transaksi_id}")
            except ValueError as e:
                print(e)


        elif pilihan == '5':  # Delete transaction
            print("\nPilih File yang ingin dihapus: ")
            print("1. ID Transaksi")
            pilihan_hapus = input("Pilihan: ")
            if pilihan_hapus == '1':
                id_hapus = input("Masukkan ID yang akan dihapus: ")
                if furniture_handler.hapus_furniture(id_hapus):
                    print(f"Data transaksi dengan ID '{id_hapus}' berhasil dihapus.")
                else:
                    print(f"ID transaksi '{id_hapus}' tidak ditemukan.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '6':  # View transactions
            print("\nData Transaksi:")
            data_dict = transaksi_handler.list_transaksi()
            for data_transaksi, transaksi in data_dict.items():
                print(f"{data_transaksi}: {transaksi}")

        elif pilihan == '7':  # Exit
            print("Terima kasih telah menggunakan aplikasi!")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()
