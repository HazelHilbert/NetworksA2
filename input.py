def input_address():
    valid = False
    while not valid:
        id_input = input("Enter address: ")
        if len(id_input) == 4:
            try:
                address = bytes.fromhex(id_input)
                valid = True
            except:
                print("Invalid ID: enter 4 char string representing a 2 byte hexadecimal number")
                continue
        else:
            print("Invalid ID: enter 4 char string representing a 2 byte hexadecimal number")
    return address