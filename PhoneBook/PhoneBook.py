import psycopg2
import csv

def setup_conn():
    dbname = "postgres" #input("Please enter the name of dbname: ") 
    user = "postgres"#input("Please enter the name of user: ") #
    password = "wwweeemmm"#input("Please enter the password: ") #www......
    host = "localhost" #input("Please enter the name of host: ") #localhost
    port = "5432" #input("Please enter the port: ") #5432
    return psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
    )
while True:
    try: 
        conn = setup_conn()
        break
    except Exception: 
        print("There are some mistakes in your data. Please check it and try again")
cur = conn.cursor()

cur.execute(f"CREATE TABLE IF NOT EXISTS PhoneBook (id SERIAL PRIMARY KEY, name TEXT, phone VARCHAR(11));")
conn.commit()

def read_from_csv():
    with open("PhoneBook.csv", "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for i in reader:
            try:
                cur.execute("CALL inserting(%s, %s);", (i[0], i[1]))
                conn.commit()
            except Exception: print("Format: \"(NAME) (PHONE NUMBER(11 digits))\"")



def read_from_powershell():
    while True:
        name_num = input("Start to input name and phone number with space. If you want to stop you should write \"STOP\":").split()
        if name_num==["STOP"]: break
        elif len(name_num) != 2 or not name_num[1].isdigit() or len(name_num[1]) != 11:
            print("Please do not forget about format - \'(NAME) (PHONE NUMBER(11 digits))\'")
            continue
        #try:
        cur.execute("CALL inserting(%s, %s);", (name_num[0], name_num[1]))
        conn.commit()
        #Exception: print("Format: \"(NAME) (PHONE NUMBER(11 digits))\"")


def change_user_phone():
    name = input("Please, enter the name of user: ")
    new_number = input("Please, enter new phone number: ")
    try:
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE name = %s;", (new_number, name))
        conn.commit()
    except Exception: print("There is no such user's name")

def change_user_name():
    number = input("Please, enter phone number: ")
    new_name = input("Please, enter the new name of user: ")
    try:
        cur.execute("UPDATE PhoneBook SET name = %s WHERE phone = %s;", (new_name, number))
        conn.commit()
    except Exception: print("There is no such phone number")

def filter_by_aplhabetic_order():
    cur.execute("SELECT * FROM PhoneBook;")
    name_phone = cur.fetchall()
    name_phone.sort(key = lambda x: x[1].lower())
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in name_phone:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")

def filter_by_reverse_aplhabetic_order():
    cur.execute("SELECT * FROM PhoneBook;")
    name_phone = cur.fetchall()
    name_phone.sort(key = lambda x: x[1].lower(), reverse = True)
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in name_phone:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")
    
def filter_by_phone_num():
    cur.execute("SELECT * FROM PhoneBook;")
    name_phone = cur.fetchall()
    name_phone.sort(key = lambda x: x[2])
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in name_phone:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")

def filter_by_phone_num_reverse():
    cur.execute("SELECT * FROM PhoneBook;")
    name_phone = cur.fetchall()
    name_phone.sort(key = lambda x: x[2], reverse=True)
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in name_phone:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")

def delete_the_data_by_username():
    name = input("Please input the username that you want to delete: ")
    cur.execute("CALL deleting(%s)", (name, ))
    conn.commit()

def delete_the_data_by_phone_num():
    phone_num = input("Please input the phone number that you want to delete: ")
    cur.execute("CALL deleting(%s)", (phone_num, ))
    conn.commit()

def filter_by_pattern():
    pattern = '%' + input("Please input the pattern that yoy want to find in names or in numbers: ") + '%'
    cur.execute("SELECT * FROM filter_by_pattern(%s);", (pattern,))
    conn.commit()
    name_phone = cur.fetchall()
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in name_phone:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")
def inserting_by_list():
    name_list = input("Please enter names of users by \",\": ").split(', ') 
    print(name_list)
    num_list = input("Please enter phone numbers of users by \",\": ").split(', ') 
    cur.execute("CALL inserting_by_list(%s, %s);", (name_list, num_list))
    conn.commit()
def querying_data():
    limit = int(input("Enter the limit of the data: "))
    offset = int(input("Enter the number of rows that should be skipped: "))
    cur.execute("SELECT * FROM querying_data(%s, %s)", (limit, offset))
    conn.commit()
    data = cur.fetchall()
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in data:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")
def show_data_from_table():
    cur.execute("SELECT * FROM phonebook")
    conn.commit()
    data = cur.fetchall()
    print(f"{'ID':<8}|{'NAME':<20}|{'PHONE':<15}")
    print("_" * 40)
    for row in data:
        print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15}")

while True:
    print("""Menu
1  - Read information from CSV file
2  - Read information from PowerShell
3  - Change user's phone number
4  - Change user's name
5  - Filter by alphabetic order
6  - Filter by reverse alphabetic order
7  - Filter by phone number
8  - Filter by phone number (reverse)
9  - Delete by username
10 - Delete by phone number
11 - Filter by pattern
12 - Insert many new users by list
13 - Query data with LIMIT and OFFSET
14 - Show data from table
0  - Exit""")
    command = input()
    if command == "1":
        read_from_csv()

    elif command == "2":
        read_from_powershell()
    elif command == "3":
        change_user_phone()
    elif command == "4":
        change_user_name()
    elif command == "5":
        filter_by_aplhabetic_order()
    elif command == "6":
        filter_by_reverse_aplhabetic_order()
    elif command == "7":
        filter_by_phone_num()
    elif command == "8":
        filter_by_phone_num_reverse()
    elif command == "9":
        delete_the_data_by_username()
    elif command =="10":
        delete_the_data_by_phone_num()
    elif command =="11":
        filter_by_pattern()
    elif command == "12":
        inserting_by_list()
    elif command == "13":
        querying_data()
    elif command == "14":
        show_data_from_table()
    elif command == "0":
        break
    else: print("Please enter the given numbers")


cur.close()
conn.close()         


