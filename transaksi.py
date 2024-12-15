import sqlite3
import datetime


def transactionFind(value, field="id_transaksi"):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    query = f"SELECT id_barang, jumlah, id_user, id_transaksi, jenis_transaksi FROM transaksi WHERE {field} = ?"
    cursor.execute(query, (value,))
    transaction = cursor.fetchone()
    conn.close()
    return transaction


def convertTransaction(numberTypeTransaction):
    if numberTypeTransaction == "1":
        return "masuk"
    return "keluar"


def createTransaction():
    from migration import tableTransaksi
    from barang import readGoods, goodsFind, updateStockGoods
    from auth import validatorNumber, getCredential

    tableTransaksi()
    readGoods()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idGoods = input("Masukkan ID Barang untuk transaksi: ")
    goods = goodsFind(idGoods)
    if not goods:
        print(f"ID Barang `{idGoods}` tidak ditemukan")
        return createTransaction()
    typeTransaction = input("masukan jenis transaksi (1.masuk, 2.keluar): ")
    typeTransaction = convertTransaction(typeTransaction)
    countGoods = 0
    while True:
        countGoods = validatorNumber(
            "int",
            f"masukan jumlah barang (stok: {goods[3]}): ",
            "Jumlah barang harus berupa angka bulat",
            "",
        )
        if countGoods > goods[3] and typeTransaction == "keluar":
            continue
        else:
            break
    priceGosds = validatorNumber(
        "float",
        f"masukkan harga barang (harga barang: {goods[4]}, default harga barang yang dipilih): ",
        "Harga barang harus berupa angka",
        "",
        True,
    )
    if priceGosds == "":
        priceGosds = goods[4]
    remainder = (
        countGoods + goods[3] if typeTransaction == "masuk" else goods[3] - countGoods
    )
    cursor.execute(
        "INSERT INTO transaksi (id_user, id_barang, jenis_transaksi, jumlah, harga_satuan, tanggal_transaksi) VALUES (?, ?, ?, ?, ?, ?)",
        (
            getCredential().get("id_user"),
            idGoods,
            typeTransaction,
            countGoods,
            priceGosds,
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
        ),
    )
    cursor.execute(
        "UPDATE barang SET stok = ? WHERE id_barang = ?",
        (
            remainder,
            idGoods,
        ),
    )
    conn.commit()
    conn.close()


def readTransaction():
    from auth import getCredential

    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    query = f"""
        SELECT barang.nama_sparepart,barang.kode_sparepart,user.email, 
        transaksi.jenis_transaksi,transaksi.harga_satuan,transaksi.jumlah,
        transaksi.tanggal_transaksi, transaksi.id_transaksi
        FROM transaksi JOIN user ON user.id_user = transaksi.id_user 
        JOIN barang ON barang.id_barang = transaksi.id_barang { 'WHERE user.id_user = ?' if getCredential().get('role') != 'admin' else ''}
        """
    if getCredential().get("role") != "admin":
        cursor.execute(
            query,
            (getCredential().get("id_user"),),
        )
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    print("\n" + "List Transaksi")
    print(
        f"{'ID Transaksi':<20} {'Nama Sparepart':<20} {'Kode Sparepart':<20} {'Email PIC':<20} {'Aksi':<20} {'Harga Satuan':<20} {'Jumlah Barang':<20} {'Total':<20} {'Waktu Transaksi'}"
    )
    for row in rows:
        print(
            f"{row[7]:<20} {row[0]:<20} {row[1]:<20} {row[2]:<20} {row[3]:<20} {row[4]:<20} {row[5]:<20} {(row[5]*row[4]):<20} {datetime.datetime.fromisoformat(row[6]).strftime('%Y-%m-%d %H:%M:%S')}"
        )
    conn.close()


def updateTransaction():
    from barang import goodsFind
    from auth import validatorNumber

    readTransaction()

    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idTransaction = input("Masukkan ID Transaksi yang ingin di edit: ")
    transaction = transactionFind(idTransaction)
    if not transaction:
        print(f"ID Transaksi `{idTransaction}` tidak ditemukan")
        return updateTransaction()
    typeTransaction = input("masukan jenis transaksi (1.masuk, 2.keluar): ")
    typeTransaction = convertTransaction(typeTransaction)
    goods = goodsFind(transaction[0])
    latestCountGoods = (
        goods[3] + transaction[1]
        if typeTransaction == "keluar"
        else goods[3] - transaction[1]
    )
    countGoods = 0
    while True:
        countGoods = validatorNumber(
            "int",
            f"masukan jumlah barang (stok: {latestCountGoods}): ",
            "Jumlah barang harus berupa angka bulat",
            "",
        )
        if countGoods > latestCountGoods and typeTransaction == "keluar":
            continue
        else:
            break
    priceGosds = validatorNumber(
        "float",
        f"masukkan harga barang (harga barang: {goods[4]}, default harga barang yang dipilih): ",
        "Harga barang harus berupa angka",
        "",
        True,
    )
    if priceGosds == "":
        priceGosds = goods[4]
    remainder = (
        countGoods + latestCountGoods
        if typeTransaction == "masuk"
        else latestCountGoods - countGoods
    )
    cursor.execute(
        "UPDATE transaksi set jenis_transaksi = ?, jumlah = ?, harga_satuan = ? WHERE id_transaksi = ?",
        (
            typeTransaction,
            countGoods,
            priceGosds,
            transaction[3],
        ),
    )
    cursor.execute(
        "UPDATE barang SET stok = ? WHERE id_barang = ?",
        (
            remainder,
            transaction[0],
        ),
    )
    conn.commit()
    conn.close()
    readTransaction()


def deleteTransaction():
    from barang import goodsFind

    readTransaction()

    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idTransaction = input("Masukkan ID Transaksi yang ingin di hapus: ")
    transaction = transactionFind(idTransaction)
    if not transaction:
        print(f"ID Transaksi `{idTransaction}` tidak ditemukan")
        return deleteTransaction()
    goods = goodsFind(transaction[0])
    latestCountGoods = (
        goods[3] + transaction[1]
        if transaction[4] == "keluar"
        else goods[3] - transaction[1]
    )
    cursor.execute("DELETE FROM transaksi WHERE id_transaksi = ?", (transaction[3],))
    cursor.execute(
        "UPDATE barang SET stok = ? WHERE id_barang = ?",
        (
            latestCountGoods,
            transaction[0],
        ),
    )
    conn.commit()
    conn.close()
    readTransaction()


def transactionMenu():
    from index import index

    print("\n" + "=" * 10 + "Menu Barang" + "=" * 10)
    print("1. Tambah data transaksi")
    print("2. Lihat data transaksi")
    print("3. Edit data transaksi")
    print("4. Hapus data transaksi")
    print("5. Menu Utama")
    choice = input("Masukkan pilihan: ")
    if choice == "1":
        createTransaction()
        transactionMenu()
    elif choice == "2":
        readTransaction()
        transactionMenu()
    elif choice == "3":
        updateTransaction()
        transactionMenu()
    elif choice == "4":
        deleteTransaction()
        transactionMenu()
    elif choice == "5":
        index()
    else:
        transactionMenu()
