def commands():

    starting_command = starting_command_check(starting_menu(), number_of_commands=5)

    if starting_command is '1':

        print("\nYou want to add new record.\n"
              "There is an example of filling the fields below.\n"
              "\n"
              "Name and surname: Ivan Ivanov\n"
              "Date of birth (optional): dd mm yyyy\n"
              "(If you don't want to add date of birth, press Enter)\n"
              "Phone number: 8XXXXXXXXXX\n")

        print(add_to_phone_book("phone_book", check_name_surname(enter_name_surname())))

    elif starting_command is '2':
        change_record("phone_book")

    elif starting_command is '3':
        delete_record("phone_book")

    elif starting_command is '4':
        print(find_record("phone_book"))

    elif starting_command is '5':
        print(*show_phone_book("phone_book"))


def starting_menu():

    print("\nHello! How would you like to use the phone book? \n"
          "Please choose the number of operation from the list below: \n"
          "\n"
          "1. Add new record. \n"
          "2. Change an existing record. \n"
          "3. Delete a record. \n"
          "4. Find a record. \n"
          "5. Show all the records from the phone book. \n"
          "\n")

    starting_command = input("Please enter the number: ")

    return starting_command


def starting_command_check(starting_command, number_of_commands):

    while not starting_command:
        print("\nThere is no command. Please try again.")
        starting_command = starting_menu()
        starting_command_check(starting_command, number_of_commands=5)

    while starting_command:

        if starting_command.isdigit():

            while not 0 < int(starting_command) <= number_of_commands:
                print("\nThere is no command with such a number. Please try again.")
                starting_command_check(starting_menu(), number_of_commands=5)

            else:
                return starting_command

        else:
            print("\nThe command is incorrect. Please try again.")
            starting_command = starting_menu()
            starting_command_check(starting_command, number_of_commands=5)


def enter_name_surname():
    name_surname = input("Name and surname: ")
    return name_surname.split()


def check_name_surname(name_surname):

    while len(name_surname) is not 2:

        print("You should enter name and surname only. Please try again. Example: Ivan Ivanov")
        name_surname = enter_name_surname()

    name, surname = name_surname[0], name_surname[1]

    def check_layout():

        latin_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for letter_n in name:
            if letter_n not in latin_alphabet:
                return False

        for letter_s in surname:
            if letter_s not in latin_alphabet:
                return False

    while check_layout():
        print("Name and surname should contain latin letters only. Please try again."
              "Example: Ivan Ivanov")
        name_surname = enter_name_surname()
        check_name_surname(name_surname)

    correct_name, correct_surname = name.capitalize(), surname.capitalize()
    correct_name_surname = (correct_name, correct_surname,)
    return correct_name_surname


def enter_birth_date():
    birth_date = input("Date of birth (optional): ")
    return birth_date.split()


def check_birth_date(birth_date):
    from datetime import date

    if not birth_date:
        return "-"

    while len(birth_date) is not 3:
        print("Date of birth should contain day, month and year only. "
              "Please try again. Example: dd mm yyyy")
        birth_date = enter_birth_date()

    for number in birth_date:
        while not number.isdigit():
            print("You should use numbers only. Please try again. Example: dd mm yyyy")
            birth_date = enter_birth_date()

    birth_date = list(map(int, birth_date))
    day, month, year = birth_date[0], birth_date[1], birth_date[2]

    try:
        if date(year, month, day):
            return "{0}/{1}/{2}".format(day, month, year)

    except ValueError:
        print("This date doesn't exist. Please try again. Example: dd mm yyyy")
        check_birth_date(birth_date)


def enter_phone_number():
    phone_number = input('Phone number: ')
    return phone_number


def check_phone_number(phone_number):

    while len(phone_number) is not 11 or phone_number[0] is not '8':
        print("Phone number is incorrect! Please try again. Example: 8XXXXXXXXXX")
        phone_number = enter_phone_number()

    return phone_number


def record_is_in_phone_book(file, correct_name_surname):

    name_surname_to_check = correct_name_surname[0] + '_' + correct_name_surname[1]

    with open(file) as phone_book_file:
        for line in phone_book_file:
            if name_surname_to_check in line:
                return name_surname_to_check


def add_to_phone_book(file, correct_name_surname):

    new_record = list()

    if record_is_in_phone_book(file, correct_name_surname):
        return "The record already exists."

    new_record.append(correct_name_surname[0])
    new_record.append(correct_name_surname[1])
    birth_date = check_birth_date(enter_birth_date())
    new_record.append(birth_date)

    phone_number = check_phone_number(enter_phone_number())
    new_record.append(phone_number)

    with open(file, "a") as phone_book_file:
        phone_book_file.write('{}_{} {} {} \n'.format(*new_record))

    return "\nThe record is added."


def show_phone_book(file):
    with open(file) as phone_book_file:
        phone_book = phone_book_file.readlines()
    return phone_book


def find_record(file):

    s = enter_name_surname()
    name_surname = s[0].capitalize() + '_' + s[1].capitalize()

    with open(file) as phone_book_file:

        for line in phone_book_file:
            if name_surname in line:
                return line

        return "There is no such a record in the phone book."


def converting_phone_book_to_list(file):

    phone_book = list()

    with open(file) as phone_book_file:
        for line in phone_book_file:
            phone_book.append(line)

    return phone_book


def delete_record(file):

    print("You want to delete a record.")
    name_surname_to_delete = record_is_in_phone_book(file,
                                                     check_name_surname(enter_name_surname()))

    if name_surname_to_delete:

        phone_book = converting_phone_book_to_list(file)

        for record in phone_book:
            if name_surname_to_delete in record:
                phone_book.remove(record)
                print("The record is deleted.")

        with open(file, "w") as phone_book_file:
            for line in phone_book:
                phone_book_file.write(line)

    else:
        print("There is no such a record in a phone book.")


def change_record(file):

    print("What record do you want to change? Please enter name and surname below.\n")
    name_surname_to_change = record_is_in_phone_book(file, check_name_surname(enter_name_surname()))

    def prepare_to_change():

        if name_surname_to_change:

            print("What do you want to change? Choose the number below.\n"
                  "1. Name/surname\n"
                  "2. Date of birth\n"
                  "3. Phone number\n")

            number_of_change = input("Enter the number: ")
            starting_command_check(number_of_change, number_of_commands=3)

            return number_of_change

    def performing_change(number_of_change):

        phone_book = converting_phone_book_to_list(file)

        for record in phone_book:
            if name_surname_to_change in record:
                record_to_change = record.split()

                if number_of_change is '1':
                    record_to_change[0] = '{}_{} '.format(*check_name_surname(enter_name_surname()))

                elif number_of_change is '2':
                    record_to_change[1] = check_birth_date(enter_birth_date())

                elif number_of_change is '3':
                    record_to_change[2] = check_phone_number(enter_phone_number())

                with open(file, "r") as phone_book_file:
                    phone_book = phone_book_file.read()

                new_phone_book = phone_book.replace(record, "{} \n ".format(' '.join(record_to_change)))

                with open(file, "w") as phone_book_file:
                    phone_book_file.write(new_phone_book)

                print("The record is changed.")

    performing_change(prepare_to_change())


commands()
