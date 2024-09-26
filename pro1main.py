# line untuk meminta input file dari pengguna
def request_file():
    while True:
        filename = input("Masukkan nama file (dengan txt atau csv): ")
        if os.path.exists(filename):
            return filename
        else:
            print(f"File {filename} tidak ditemukan. coba lagi pak.")

# fungsi utama
def main():
    print("Aplikasi Pembaca File: Array/Dictionary")

    # meminta nama file dari pengguna
    filename = request_file()
    # meminta pengguna untuk memilih format file (array atau dictionary)
    while True:
        file_format = input("Masukkan format file (array/dictionary): ").strip().lower()

        if file_format == 'array':
            array_data = read_array_file(filename)
            print("Isi file dalam format Array:")
            print(array_data)
            break
        elif file_format == 'dictionary':
            dict_data = read_dict_file(filename)
            print("Isi file dalam format Dictionary:")
            for key, value in dict_data.items():
                print(f"{key}: {value}")
            break
        else:
            print("Format tidak dikenali. Silakan masukkan 'array' atau 'dictionary'.")

# menjalankan program
if _name_ == "_main_":
    main()
