import sqlite3


def goodsFind(value, field="id_barang"):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    query = f"SELECT id_barang, nama_sparepart, kode_sparepart, stok, harga FROM barang WHERE {field} = ?"
    cursor.execute(query, (value,))
    goods = cursor.fetchone()
    conn.close()
    return goods


def goodsTransactionExist(idGoods):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_barang FROM transaksi WHERE id_barang = ?",
        (idGoods,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def createGoods():
    from migration import tableBarang
    from auth import validatorNumber

    tableBarang()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    name = input("Masukkan nama barang/sparepart: ")
    kode = input("Masukkan kode barang/sparepart: ")
    stok = validatorNumber(
        "float", "Masukkan stok barang: ", "Stok harus berupa angka", ""
    )
    harga = validatorNumber(
        "float", "Masukkan harga barang: ", "Harga harus berupa angka", ""
    )
    cursor.execute(
        "INSERT INTO barang (nama_sparepart, kode_sparepart, stok, harga) VALUES (?, ?, ?, ?)",
        (name, kode, stok, harga),
    )
    conn.commit()
    conn.close()


def readGoods():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_barang, nama_sparepart, kode_sparepart, stok, harga FROM barang"
    )
    rows = cursor.fetchall()
    print("\n" + "List Barang")
    print(
        f"{'ID Barang':<10} {'Nama barang':<15} {'Kode Barang':<15} {'Stok Barang':<15} {'Harga':<15}"
    )
    for row in rows:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<15} {row[3]:<15} {row[4]:<15}")
    conn.close()


def updateGoods():
    from auth import validatorNumber

    readGoods()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idGoods = input("Masukkan ID Barang yang ingin di edit: ")
    if not goodsFind(idGoods):
        print(f"ID Barang `{idGoods}` tidak ditemukan")
        return updateGoods()
    name = input("Masukkan nama barang/sparepart: ")
    kode = input("Masukkan kode barang/sparepart: ")
    stok = validatorNumber(
        "float", "Masukkan stok barang: ", "Stok harus berupa angka", ""
    )
    harga = validatorNumber(
        "float", "Masukkan harga barang: ", "Harga harus berupa angka", ""
    )
    cursor.execute(
        "UPDATE barang SET nama_sparepart = ?, kode_sparepart = ?, stok = ?, harga = ? WHERE id_barang = ?",
        (name, kode, stok, harga, idGoods),
    )
    conn.commit()
    conn.close()
    readGoods()


def deleteGoods():
    readGoods()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idGoods = input("Masukkan ID Barang yang ingin di hapus: ")
    if not goodsFind(idGoods):
        print(f"ID Barang `{idGoods}` tidak ditemukan")
        return deleteGoods()
    elif goodsTransactionExist(idGoods):
        print(f"ID Barang '{idGoods}' memiliki transaksi dan tidak bisa dihapus")
        return deleteGoods()
    cursor.execute("DELETE FROM barang WHERE id_barang = ?", (idGoods,))
    conn.commit()
    conn.close()
    readGoods()


def updateStockGoods():
    from auth import validatorNumber

    readGoods()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idGoods = input("Masukkan ID Barang yang ingin di ubah stoknya: ")
    if not goodsFind(idGoods):
        print(f"ID Barang `{idGoods}` tidak ditemukan")
        return updateStockGoods()
    stok = validatorNumber(
        "float", "Masukkan stok barang: ", "Stok harus berupa angka", ""
    )
    cursor.execute(
        "UPDATE barang SET stok = ? WHERE id_barang = ?",
        (stok, idGoods),
    )
    conn.commit()
    conn.close()
    readGoods()


def goodsMenu():
    from index import index

    print("\n" + "=" * 10 + "Menu Barang" + "=" * 10)
    print("1. Tambah data barang")
    print("2. Lihat data barang")
    print("3. Edit data barang")
    print("4. Hapus data barang")
    print("5. Update stok barang")
    print("6. Menu Utama")
    choice = input("Masukkan pilihan: ")
    if choice == "1":
        createGoods()
        goodsMenu()
    elif choice == "2":
        readGoods()
        goodsMenu()
    elif choice == "3":
        updateGoods()
        goodsMenu()
    elif choice == "4":
        deleteGoods()
        goodsMenu()
    elif choice == "5":
        updateStockGoods()
        goodsMenu()
    elif choice == "6":
        index()
    else:
        goodsMenu()
