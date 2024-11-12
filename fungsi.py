import os
from pathlib import Path

class FileHandler:
    def __init__(self, directory=None):
        self.current_directory = directory or os.path.dirname(os.path.abspath(__file__))

    def bacafile(self, nama_file):
        """Membaca file dan mengembalikan isinya sebagai string. Jika file tidak ditemukan, mengembalikan None."""
        file_path = Path(self.current_directory) / nama_file
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def editfile(self, nama_file, data, mode='w'):
        """Menulis data ke file dengan mode tertentu (default: 'w')."""
        file_path = Path(self.current_directory) / nama_file
        with open(file_path, mode) as file:
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
        """Mengembalikan dictionary daftar warna dari file."""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_warna(self, warna):
        """Menambahkan warna baru ke file dan mengembalikan kunci (key)-nya."""
        data_dict = self.list_warna()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = warna
        self._tulis_kembali_data(data_dict)
        return new_key

    def hapus_warna(self, data_key):
        """Menghapus warna berdasarkan kunci (key) dan mengembalikan True jika berhasil."""
        data_dict = self.list_warna()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False


class Ukuran(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_ukuran.txt', 'ukuran', file_handler)

    def list_ukuran(self):
        """Mengembalikan dictionary daftar ukuran dari file."""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_ukuran(self, ukuran):
        """Menambahkan ukuran baru ke file dan mengembalikan kunci (key)-nya."""
        data_dict = self.list_ukuran()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = ukuran
        self._tulis_kembali_data(data_dict)
        return new_key

    def hapus_ukuran(self, data_key):
        """Menghapus ukuran berdasarkan kunci (key) dan mengembalikan True jika berhasil."""
        data_dict = self.list_ukuran()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False


class Furniture(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_furniture.txt', 'furniture', file_handler)

    def list_furniture(self):
        """Mengembalikan dictionary daftar furniture dari file."""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_furniture(self, furniture): 
        """Menambahkan furniture baru ke file dan mengembalikan kunci (key)-nya."""
        data_dict = self.list_furniture()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = furniture
        self._tulis_kembali_data(data_dict)
        return new_key

    def hapus_furniture(self, data_key): 
        """Menghapus furniture berdasarkan kunci (key) dan mengembalikan True jika berhasil.""" 
        data_dict = self.list_furniture()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False



class Transaksi(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_transaksi.txt', 'transaksi', file_handler)

    def list_transaksi(self):
        """Mengembalikan dictionary daftar transaksi dari file."""
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_transaksi(self, furniture_key, jumlah, harga):
        """Menambahkan transaksi baru dan mengembalikan kunci (key)-nya."""
        data_dict = self.list_transaksi()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = f"Furniture Key: {furniture_key}, Jumlah: {jumlah}, Harga: {harga}"
        self._tulis_kembali_data(data_dict)
        return new_key
