import sqlite3


def userCredentialExist(email, password):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, id_user, role FROM user WHERE email = ? AND password = ?",
        (
            email,
            password,
        ),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def userFind(value, field="id_user"):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    query = f"SELECT id_user, email, role FROM user WHERE {field} = ?"
    cursor.execute(query, (value,))
    user = cursor.fetchone()
    conn.close()
    return user


def userTransactionExist(idUser):
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_user FROM transaksi WHERE id_user = ?",
        (idUser,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def convertRole(numberRole):
    if numberRole == "1":
        return "admin"
    return "staff"


def createUser():
    from migration import tableUser

    tableUser()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    email = input("Masukkan Email user: ")
    if userFind(email, "email"):
        print("Email Sudah digunakan")
        return createUser()
    role = input("Pilih Role User (1.Admin,2.Staff): ")
    password = input("Masukkan Password user: ")
    role = convertRole(role)
    cursor.execute(
        "INSERT INTO user (email, role, password) VALUES (?, ?, ?)",
        (email, role, password),
    )
    conn.commit()
    conn.close()


def readUser():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_user, email, role FROM user")
    rows = cursor.fetchall()
    print("\n" + "List User")
    print(f"{'ID User':<10} {'Email':<15} {'Role':<15}")
    for row in rows:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<15}")
    conn.close()


def updateUser():
    readUser()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idUser = input("Masukkan ID User yang ingin di edit: ")
    if not userFind(idUser):
        print(f"ID User '{idUser}' tidak ditemukan")
        return updateUser()
    email = input("Masukkan Email user: ")
    if userFind(email, "email"):
        print("Email Sudah digunakan")
        return updateUser()
    role = input("Pilih Role User (1.Admin,2.Staff): ")
    password = input("Masukkan Password user: ")
    role = convertRole(role)
    cursor.execute(
        "UPDATE user SET email = ?, role = ?, password = ? WHERE id_user = ?",
        (email, role, password, idUser),
    )
    conn.commit()
    conn.close()
    readUser()


def deleteUser():
    readUser()
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    idUser = input("Masukkan ID User yang ingin di hapus: ")
    if not userFind(idUser):
        print(f"ID User '{idUser}' tidak ditemukan")
        return deleteUser()
    elif userTransactionExist(idUser):
        print(f"ID User '{idUser}' memiliki transaksi dan tidak bisa dihapus")
        return deleteUser()
    cursor.execute("DELETE FROM user WHERE id_user = ?", (idUser,))
    conn.commit()
    conn.close()
    readUser()


def userMenu():
    from index import index

    print("\n" + "=" * 10 + "Menu User" + "=" * 10)
    print("1. Tambah data user")
    print("2. Lihat data user")
    print("3. Edit data user")
    print("4. Hapus data user")
    print("5. Menu Utama")
    choice = input("Masukkan pilihan: ")
    if choice == "1":
        createUser()
        userMenu()
    elif choice == "2":
        readUser()
        userMenu()
    elif choice == "3":
        updateUser()
        userMenu()
    elif choice == "4":
        deleteUser()
        userMenu()
    elif choice == "5":
        index()
    else:
        userMenu()
