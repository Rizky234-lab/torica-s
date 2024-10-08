from datetime import datetime

class Furniture:
    def __init__(self, name, size, quantity, color, price):
        self.name = name
        self.size = size  # in cm
        self.quantity = quantity
        self.color = color
        self.price = price  # harga per item

    def info(self):
        return f"{self.name} - Ukuran {self.size} cm - {self.quantity} pieces - {self.color} - Rp {self.price}"

    def get_total_price(self, count):
        return self.price * count


def add_furniture(name, size, quantity, color, price):
    new_furniture = Furniture(name, size, quantity, color, price)
    furnitures.append(new_furniture)
    print(f"{name} berhasil ditambahkan!")


def edit_furniture(index, name, size, quantity, color, price):
    if 0 <= index < len(furnitures):
        furnitures[index].name = name
        furnitures[index].size = size
        furnitures[index].quantity = quantity
        furnitures[index].color = color
        furnitures[index].price = price
        print(f"Furniture dengan kode {index} berhasil diubah!")
    else:
        print("Kode furniture tidak valid.")


def delete_furniture(index):
    if 0 <= index < len(furnitures):
        deleted_item = furnitures.pop(index)
        print(f"{deleted_item.name} berhasil dihapus!")
    else:
        print("Kode furniture tidak valid.")


furniture1 = Furniture('kursi', 50, 2, 'Brown', 150000)
furniture2 = Furniture('sofa', 200, 3, 'Red', 2000000)
furniture3 = Furniture('meja', 150, 4, 'Black', 750000)

furnitures = [furniture1, furniture2, furniture3]

print("Selamat datang di Torica toko furniture terpercaya")

while True:
    print('List barang yang ada di toko kami:')
    for index, furniture in enumerate(furnitures):
        print(f"{index}. {furniture.info()}")

    print('--------------------')
    print('1. Tambah furniture')
    print('2. Edit furniture')
    print('3. Hapus furniture')
    print('4. Order furniture')
    print('5. Keluar')
    choice = input("Masukkan pilihan (1-5): ")

    if choice == '1':
        # Tambah furniture
        name = input("Masukkan nama furniture: ")
        size = int(input("Masukkan ukuran furniture (cm): "))
        quantity = int(input("Masukkan jumlah furniture: "))
        color = input("Masukkan warna furniture: ")
        price = int(input("Masukkan harga per item (Rp): "))
        add_furniture(name, size, quantity, color, price)

    elif choice == '2':
        # Edit furniture
        try:
            edit_index = int(input("Masukkan kode furniture yang ingin diubah: "))
            name = input("Masukkan nama baru furniture: ")
            size = int(input("Masukkan ukuran baru furniture (cm): "))
            quantity = int(input("Masukkan jumlah baru furniture: "))
            color = input("Masukkan warna baru furniture: ")
            price = int(input("Masukkan harga baru per item (Rp): "))
            edit_furniture(edit_index, name, size, quantity, color, price)
        except ValueError:
            print("Input tidak valid.")

    elif choice == '3':
        # Hapus furniture
        try:
            delete_index = int(input("Masukkan kode furniture yang ingin dihapus: "))
            delete_furniture(delete_index)
        except ValueError:
            print("Input tidak valid.")

    elif choice == '4':
        # Order furniture
        while True:
            try:
                furniture_order = int(input('Masukkan kode furniture yang anda inginkan: '))
                if furniture_order < 0 or furniture_order >= len(furnitures):
                    print("Kode furniture tidak ada. Mohon ulangi kembali.")
                    continue
                break
            except ValueError:
                print("Kode furniture tidak ada. Mohon ulangi kembali.")

        selected_furniture = furnitures[furniture_order]

        while True:
            try:
                count = int(input('Masukkan jumlah paket yang diinginkan: '))
                if count < 1:
                    print("Pemesanan minimal adalah 1 paket")
                    continue
                break
            except ValueError:
                print("Mohon hanya masukkan angka.")

        result = selected_furniture.get_total_price(count)

        print('--------------------')

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string)

        print(f'Total harga adalah Rp {result}')

        print('''
        Terima kasih sudah berbelanja.
        Selamat datang kembali.
        ''')

        print('--------------------')

        def writeHistory(date, total):
            text = date + "\n" + "Total harga adalah Rp " + str(total) + "\n\n"
            with open('history.txt', 'at') as file:
                file.write(text)

        writeHistory(dt_string, result)

    elif choice == '5':
        print("Terima kasih, sampai jumpa belanja lagi ya di toko kami!")
        break

    else:
        print("Pilihan tidak valid. Mohon ulangi kembali.")
