credential = {"id_user": "", "email": "", "role": ""}


def getRole():
    return credential.get("role")


def getCredential():
    return credential


def isAuth():
    if (
        credential.get("id_user") != ""
        and credential.get("email") != ""
        and credential.get("role") != ""
    ):
        return True
    return False


def setAuth(id_user, email, role):
    global credential
    credential.update({"id_user": id_user, "email": email, "role": role})


def login():
    from user import userCredentialExist
    from index import index

    print("\n" + "=" * 10 + "login" + "=" * 10)
    email = input("Masukkan Email: ")
    password = input("Masukkan Password: ")
    user = userCredentialExist(email, password)
    if user:
        setAuth(user[1], user[0], user[2])
        print("\n" * 10)
        index()
    else:
        print("\nPassword/Email yang anda masukkan salah")
        login()


def logout():
    from index import index

    setAuth("", "", "")
    index()


def validatorNumber(type, textInput, textError, textSaparator):
    while True:
        try:
            if type == "int":
                return int(input(textInput))
            elif type == "float":
                return float(input(textInput))
        except ValueError:
            print(textError)
            if textSaparator:
                print(textSaparator)
            continue
