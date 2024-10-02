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
