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

def parse_dictionary(data):
    dict_result = {}
    
    if '=>' in data:
        pairs = data.split(',')
    elif ':' in data:
        pairs = data.split(';')
    else:
        pairs = []
    
    for pair in pairs:
        if '=>' in pair:
            key, value = pair.split('=>')
        elif ':' in pair:
            key, value = pair.split(':')
        else:
            continue
        dict_result[key.strip()] = value.strip()
    return dict_result
