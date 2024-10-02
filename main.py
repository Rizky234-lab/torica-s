from pel import baca_file, parse_array, parse_dictionary

def main():
    while True:
        nama_file = input("Masukkan nama file txt/csv: ")
        isi_file = baca_file(nama_file)
        if isi_file is not None:
            if '=>' in isi_file or ':' in isi_file:
                #ini Dictionary
                data_dict = parse_dictionary(isi_file)
                print("\nData yang dibaca adalah Dictionary:")
                print(data_dict)
            else:
                #ini Array
                data_array = parse_array(isi_file)
                print("\nData yang dibaca adalah Array:")
                print(data_array)
        else:
            print(f"File '{nama_file}' tidak ditemukan.coba lagi.\n")
        
        #tanyakan masukkan lagi / tidak
        pilihan = input("\nApakah Anda ingin memasukkan file lain? (y/n): ").lower()
        if pilihan != 'y':
            print("Terima kasih telah menggunakan aplikasi!")
            break


if __name__ == "__main__":
    main()
