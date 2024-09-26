def baca_file(nama_file):
    try:
        with open(nama_file, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        return None

def parse_array(data):
    #misah berdasarkan koma
    if ',' in data:
        array = [item.strip() for item in data.split(',')]
    else:
        #misahin berdasarkan baris baru
        array = [item.strip() for item in data.splitlines() if item.strip()]
    return array
