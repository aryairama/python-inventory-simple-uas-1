import sqlite3


def tableUser():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user (  
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,  
        email TEXT UNIQUE NOT NULL,  
        password TEXT NOT NULL,
        role TEXT CHECK(role IN("staff","admin")) DEFAULT "staff"
        )"""
    )
    conn.commit()
    conn.close()


def tableBarang():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS barang (  
        id_barang INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_sparepart TEXT NOT NULL,
        kode_sparepart TEXT NOT NULL,
        stok INTEGER DEFAULT 0,
        harga DECIMAL(10,2) NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


def tableTransaksi():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS transaksi (  
        id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL,
        id_barang INTEGER NOT NULL,
        jenis_transaksi TEXT CHECK(jenis_transaksi IN("masuk","keluar")) NOT NULL,
        jumlah INTEGER NOT NULL,
        total_harga DECIMAL(10,2) NOT NULL,
        tanggal_transaksi DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES  user(user_id),
        FOREIGN KEY (id_barang) REFERENCES  barang (id_barang)
        )"""
    )
    conn.commit()
    conn.close()


tableUser()
tableBarang()
tableTransaksi()
