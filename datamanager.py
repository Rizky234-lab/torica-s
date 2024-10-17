from fungsi import  Warna, Ukuran, furniture

class DataManager:
    def __init__(self):
        self.warna = Warna()
        self.ukuran = Ukuran()
        self.furniture = furniture()

    def get_data_object(self, data_type):
        if data_type == 'warna':
            return self.warna
        elif data_type == 'ukuran':
            return self.ukuran
        elif data_type == 'furniture':
            return self.furniture
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def list_data(self, data_type):
        data_object = self.get_data_object(data_type)
        if data_type == 'warna':
            return data_object.list_warna()
        elif data_type == 'ukuran':
            return data_object.list_ukuran()
        elif data_type == 'furniture':
            return data_object.list_furniture()

    def delete_data(self, data_type, item_id):
        data_object = self.get_data_object(data_type)
        if data_type == 'warna':
            return data_object.hapus_warna(item_id)
        elif data_type == 'ukuran':
            return data_object.hapus_ukuran(item_id)
        elif data_type == 'furniture':
            return data_object.hapus_furniture(item_id)


    def tambah_warna(self, warna_baru):
        return self.warna.tambah_warna(warna_baru)
        
    def tambah_ukuran(self, ukuran_baru):
        return self.ukuran.tambah_ukuran(ukuran_baru)
        
    def tambah_furniturel(self, nama_furniture, id_ukuran, id_warna):
        return self.furniture.tambah_furniture(nama_furniture, id_ukuran, id_warna)
    
    def tambah_transaksi(self, transaksi_data):
        # transaksi_data should be in the format "id_furniture_banyak_barang_tanggal"
        return self.transaksi.tambah_transaksi(transaksi_data)
    
    
