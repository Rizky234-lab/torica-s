from importfurniture import baca_file, delete_data, add_data

def main():
    manager = ('data_furniture.txt')
    while True:
        print("Menu:")
        print("1. Tambah Data Furniture")
        print("2. Hapus Data Furniture")
        print("3. Edit Data Furniture")
        print("4. Tampilkan Data Furniture")
        print("5. Keluar")
        
        pilihan = input("Masukkan pilihan: ")
        
        if pilihan == "1":
            nama_barang = input("Masukkan nama barang: ")
            warna = input("Masukkan warna: ")
            ukuran = input("Masukkan ukuran: ")
            manager.tambah_data(nama_barang, warna, ukuran)
        elif pilihan == "2":
            nama_barang = input("Masukkan nama barang yang ingin dihapus: ")
            manager.hapus_data(nama_barang)
        elif pilihan == "3":
            nama_barang = input("Masukkan nama barang yang ingin diedit: ")
            warna = input("Masukkan warna baru (kosongkan jika tidak ingin diedit): ")
            ukuran = input("Masukkan ukuran baru (kosongkan jika tidak ingin diedit): ")
            manager.edit_data(nama_barang, warna or None, ukuran or None)
        elif pilihan == "4":
            manager.tampilkan_data()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
