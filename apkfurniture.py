import os

class Furniture:
    def _init_(self, nama_barang, warna, ukuran):
        self.nama_barang = nama_barang 
        self.warna = warna
        self.ukuran = ukuran

class FurnitureManager:
    def _init_(self, file_name):
        self.file_name = file_name
        self.data = self.baca_data()

    def baca_data(self):
        try:
            with open(self.file_name, 'r') as file:
                data = file.readlines()
                furniture_list = []
                for line in data[1:]:
                    nama_barang, warna, ukuran = line.strip().split(',')
                    furniture_list.append(Furniture(nama_barang, warna, ukuran))
                return furniture_list
        except FileNotFoundError:
            return []


def tambah_data(self, nama_barang, warna, ukuran):
        new_furniture = Furniture(nama_barang, warna, ukuran)
        self.data.append(new_furniture)
        self.tulis_data()

    def hapus_data(self, nama_barang):
        for furniture in self.data:
            if furniture.nama_barang == nama_barang:
                self.data.remove(furniture)
                self.tulis_data()
                print(f"Data {nama_barang} berhasil dihapus.")
                return
        print(f"Data {nama_barang} tidak ditemukan.")

    def edit_data(self, nama_barang, warna=None, ukuran=None):
        for furniture in self.data:
            if furniture.nama_barang == nama_barang:
                if warna:
                    furniture.warna = warna
                if ukuran:
                    furniture.ukuran = ukuran
                self.tulis_data()
                print(f"Data {nama_barang} berhasil diedit.")
                return
        print(f"Data {nama_barang} tidak ditemukan.")

    def tulis_data(self):
        with open(self.file_name, 'w') as file:
            file.write("Nama Barang,Warna,Ukuran\n")
            for furniture in self.data:
                file.write(f"{furniture.nama_barang},{furniture.warna},{furniture.ukuran}\n")

