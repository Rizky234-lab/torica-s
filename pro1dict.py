# line untuk membaca file dictionary 
def read_dict_file(filename):
    dict_data = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                # meminta format key:value
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    dict_data[key.strip()] = value.strip()
                else:
                    print(f"Nama: {line.strip()}")
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file dictionary: {e}")
    return dict_data
