import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", passwd="", autocommit=True)
c = con.cursor(buffered=True)  # without a buffered cursor, the results are lazily loaded
c.execute("create database if not exists library_db")
c.execute("use library_db")
c.execute("create table if not exists books (b_id varchar(5) primary key,b_name varchar(50), author varchar(50), available varchar(5) Default 'yes')")
c.execute(
    "create table if not exists issue_details(b_id varchar(5), student_id varchar(10), student_Name varchar(50) Not null,foreign key(b_id) references books(b_id))")


def add_book():
    bid = input("Enter BOOK ID : ")
    title = input("Enter BOOK Name : ")
    author = input("Author name : ")
    data = (bid, title, author)
    sql = 'insert into books(b_id,b_name,author) values(%s,%s,%s)'
    c.execute(sql, data)
    print("Data Entered Successfully for book id", bid)


def delete_book():
    bid = input("Enter BOOK ID : ")
    c.execute("delete from books where b_id= %s", (bid,))
    display_books()


def issue_book():
    s_name = input("Enter your Name : ")
    s_id = input("Enter Reg No : ")
    book = input("Enter Book name : ")
    c.execute("select b_id from books where b_name = '" + book + "' and available='YES'")
    book_id = c.fetchone()
    bid = book_id[0]
    print(bid)
    a = "insert into issue_details values(%s,%s,%s)"
    data = (bid, s_id, s_name)
    c.execute(a, data)
    c.execute("update books set available='no' where b_id='"+bid+" '")
    print(book, " book issued to ", s_name)


def return_book():
    name = input("Enter your Name : ")
    bid = input("Enter book id : ")
    c.execute("update books set available='yes' where b_id='" + bid + "'")
    c.execute("delete from issue_details where b_id = %s", (bid,))
    print("book id ", bid, "book returned by ", name)


def display_books():
    sql = "select * from books"
    c.execute(sql)
    my_result = c.fetchall()
    print("Book ID\t Book title\t\tAuthor\tAvailable")
    for i in my_result:
        print(i[0], "\t", i[1], "  \t", i[2], "\t", i[3])


def select_book():
    book = input('enter the name of book')
    sql = "select * from books where b_name= '" + book + "'"
    c.execute(sql)
    my_result = c.fetchall()
    print("Book ID\t Book title\t\tAuthor\tAvailable")
    for i in my_result:
        print(i[0], "\t", i[1], "\t", i[2], "\t", i[3])


def display_issued_books():
    c.execute("select issue_details. *, books.b_name from issue_details, books where issue_details.b_id = books.b_id")
    my_result = c.fetchall()
    print("list of issued books:")
    print("Book_id  book_name  Reg_no  Student_Name")
    for i in my_result:
        print(i[0], "  ", i[3], "  ", i[1], "  ", i[2])


user_name = input("Enter username : ")
ps = input("Enter Password : ")
if user_name == 'admin' and ps == 'library123':
    print('Welcome Admin')
    while True:
        print(""" TRINITY LIBRARY MANAGEMENT SYSTEM
        1. Add book   2. Issue book   3. Return book   4.Display books  5.Delete book 6.Exit """)
        ch = input("Enter your choice : ")
        if ch == '1':
            add_book()
        elif ch == '2':
            issue_book()
        elif ch == '3':
            return_book()
        elif ch == '4':
            print("1. All books   2. Issued books  3.Particular book")
            choice = int(input("choose any one"))
            if choice == 1:
                display_books()
            elif choice == 2:
                display_issued_books()
            elif choice == 3:
                select_book()
            else:
                print('wrong choice')
        elif ch == '5':
            delete_book()
        else:
            break
else:
    print("Wrong username or Password,try again")
