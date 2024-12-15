def index():
    from auth import isAuth, login, getRole, logout
    from user import userMenu
    from barang import goodsMenu
    from transaksi import transactionMenu

    if isAuth():
        print("\n" + "=" * 10 + "Menu Utama" + "=" * 10)
        print("1.Barang")
        print("2.Transaksi")
        print("3.User") if getRole() == "admin" else None
        print("0.Logout")
        choice = input("Masukkan pilihan: ")
        if choice == "1":
            goodsMenu()
        elif choice == "2":
            transactionMenu()
        elif choice == "3" and getRole() == "admin":
            userMenu()
        elif choice == "0":
            logout()
        else:
            index()
    else:
        login()


if __name__ == "__main__":
    index()
