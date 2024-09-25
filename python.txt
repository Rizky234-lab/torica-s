import os

# line untuk membaca file array (list)
def read_array_file(filename):
    array_data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # setiap baris dianggap sebagai komponen array
                array_data.append(line.strip())
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file array: {e}")
    return array_data
