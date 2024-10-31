import os
from pathlib import Path

class FileHandler:
    def bacafile(self, nama_file):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = Path(current_directory) / nama_file
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def editfile(self, nama_file, data, mode='w'):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = Path(current_directory) / nama_file
        with open(file_path, mode) as file:
            file.write(data)

class DataItem:
    def __init__(self, file_name, jenis_data):
        self.file_name = file_name
        self.jenis_data = jenis_data
        self.file_handler = FileHandler()

    def parse_dictionary(self, data):
        dict_result = {}
        lines = data.splitlines()
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                dict_result[key.strip()] = value.strip()
        return dict_result

    def _tulis_kembali_data(self, data_dict):
        content = f"ID_{self.jenis_data.upper()}\n"
        content += "\n".join(f"{id_item}:{info_item}" for id_item, info_item in data_dict.items())
        self.file_handler.editfile(self.file_name, content)

class Warna(DataItem):
    def __init__(self):
        super().__init__('idwarna.txt', 'warna')

    def list_warna(self):
        return self.parse_dictionary(self.file_handler.bacafile(self.file_name) or "")

    def tambah_warna(self, warna):
        data_dict = self.list_warna()
        new_id = str(max(map(int, data_dict.keys() or [0])) + 1)
        data_dict[new_id] = warna
        self._tulis_kembali_data(data_dict)
        return new_id

    def hapus_warna(self, id_warna):
        data_dict = self.list_warna()
        if id_warna in data_dict:
            del data_dict[id_warna]
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Ukuran(DataItem):
    def __init__(self):
        super().__init__('idukuran.txt', 'ukuran')

    def list_ukuran(self):
        return self.parse_dictionary(self.file_handler.bacafile(self.file_name) or "")

    def tambah_ukuran(self, ukuran):
        data_dict = self.list_ukuran()
        new_id = str(max(map(int, data_dict.keys() or [0])) + 1)
        data_dict[new_id] = ukuran
        self._tulis_kembali_data(data_dict)
        return new_id

    def hapus_ukuran(self, id_ukuran):
        data_dict = self.list_ukuran()
        if id_ukuran in data_dict:
            del data_dict[id_ukuran]
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Furniture(DataItem):
    def __init__(self):
        super().__init__('idfurniture.txt', 'furniture')
        self.data_warna = Warna()
        self.data_ukuran = Ukuran()

    def list_furniture(self):
        return self.parse_dictionary(self.file_handler.bacafile(self.file_name) or "")

    def tambah_furniture(self, id_ukuran, id_warna):
        warna_dict = self.data_warna.list_warna()
        ukuran_dict = self.data_ukuran.list_ukuran()

        if id_ukuran not in ukuran_dict:
            raise ValueError("Nomor ukuran tidak valid.")
        if id_warna not in warna_dict:
            raise ValueError("Nomor warna tidak valid.")

        ukuran = ukuran_dict[id_ukuran]
        warna = warna_dict[id_warna]
        furniture_data = self.list_furniture()
        new_id = str(max(map(int, furniture_data.keys() or [0])) + 1)
        furniture_data[new_id] = f"{ukuran} {warna}"

        self._tulis_kembali_data(furniture_data)
        return f"{new_id}: {ukuran} {warna}"

    def hapus_furniture(self, id_furniture):
        data_dict = self.list_furniture()
        if id_furniture in data_dict:
            del data_dict[id_furniture]
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Transaksi(DataItem):
    def __init__(self):
        super().__init__('idtransaksi.txt', 'transaksi')

    def list_transaksi(self):
        return self.parse_dictionary(self.file_handler.bacafile(self.file_name) or "")

    def tambah_transaksi(self, id_furniture, jumlah, harga):
        data_dict = self.list_transaksi()
        new_id = str(max(map(int, data_dict.keys() or [0])) + 1)
        data_dict[new_id] = f"Furniture ID: {id_furniture}, Jumlah: {jumlah}, Harga: {harga}"
        self._tulis_kembali_data(data_dict)
        return new_id
