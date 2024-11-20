import os
from pathlib import Path
from datetime import datetime


class FileHandler:
    def __init__(self, directory=None):
        self.current_directory = directory or os.path.dirname(os.path.abspath(__file__))

    def bacafile(self, nama_file):
        """Membaca file dan mengembalikan isinya sebagai string. Jika file tidak ditemukan, mengembalikan None."""
        file_path = Path(self.current_directory) / nama_file
        try:
            with open(str(file_path), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def editfile(self, nama_file, data, mode='w'):
        """Menulis data ke file dengan mode tertentu (default: 'w')."""
        file_path = Path(self.current_directory) / nama_file
        with open(str(file_path), mode) as file:
            file.write(data)


class DataItem:
    def __init__(self, file_name, jenis_data, file_handler=None):
        self.file_name = file_name
        self.jenis_data = jenis_data
        self.file_handler = file_handler or FileHandler()

    def parse_dictionary(self, data):
        """Mengonversi data teks ke dictionary, mengabaikan baris pertama (header)."""
        dict_result = {}
        lines = data.splitlines()
        for line in lines[1:]:  # Abaikan header
            if ':' in line:
                key, value = line.split(':', 1)
                dict_result[key.strip()] = value.strip()
        return dict_result

    def _tulis_kembali_data(self, data_dict):
        """Menulis ulang data dari dictionary ke file dengan format 'Data: Value'."""
        content = f"DATA_{self.jenis_data.upper()}\n"
        content += "\n".join(f"{data_key}:{data_value}" for data_key, data_value in data_dict.items())
        self.file_handler.editfile(self.file_name, content)


class Warna(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_warna.txt', 'warna', file_handler)

    def list_warna(self):
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_warna(self, warna):
        data_dict = self.list_warna()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = warna
        self._tulis_kembali_data(data_dict)
        return new_key

    def hapus_warna(self, data_key):
        data_dict = self.list_warna()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_warna(self, data_key):
        data_dict = self.list_warna()
        if data_key in data_dict:
            new_warna = input(f"Enter new color for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_warna
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Ukuran(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_ukuran.txt', 'ukuran', file_handler)
    
    def list_ukuran(self):
        """Return all size data from file"""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_ukuran(self, ukuran):
        """Add new size"""
        data_dict = self.list_ukuran()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = ukuran
        self._tulis_kembali_data(data_dict)
        return new_key
    
    def hapus_ukuran(self, data_key):
        """Delete size by ID"""
        data_dict = self.list_ukuran()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False 
    
    def edit_ukuran(self, data_key):
        data_dict = self.list_ukuran()
        if data_key in data_dict:
            new_ukuran = input(f"Enter new size for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_ukuran
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Furniture(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_furniture.txt', 'furniture', file_handler)
    
    def list_furniture(self):
        """Return all furniture data from file"""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_furniture(self, furniture):
        """Add new furniture item"""
        data_dict = self.list_furniture()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = furniture
        self._tulis_kembali_data(data_dict)
        return new_key
    
    def hapus_furniture(self, data_key):
        """Delete furniture by ID"""
        data_dict = self.list_furniture()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_furniture(self, data_key):
        data_dict = self.list_furniture()
        if data_key in data_dict:
            new_furniture = input(f"Enter new furniture for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_furniture
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Transaction(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_transaksi.txt', 'transaksi', file_handler)

    def list_transaksi(self):
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_transaksi(self, furniture_key, jumlah, harga):
        data_dict = self.list_transaksi()
        new_key = str(max((int(k) for k in data_dict.keys() if k.isdigit()), default=0) + 1)
        data_dict[new_key] = f"Furniture Key: {furniture_key}, Jumlah: {jumlah}, Harga: {harga}"
        self._tulis_kembali_data(data_dict)
        return new_key


class DateTimeHandler:
    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_date(date_str, current_format="%Y-%m-%d", desired_format="%d-%m-%Y"):
        date_obj = datetime.strptime(date_str, current_format)
        return date_obj.strftime(desired_format)
