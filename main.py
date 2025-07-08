from datetime import datetime,timedelta

users = {}
books = {}
borrowed_books = {}

def getPassword():
    while True:
        password = input("Enter your password : ")
        if len(password)>=8:
            return password
        else:
            print("Password must be at least 8 characters. Try again.")

def createAccount():
    username = input("\nEnter your username : ")
    if username in users:
        print("\nUsername already exists!")
        return
    password = getPassword()
    role = input("Enter your role (Admin/User) : ")
    users[username] = {'password' : password, 'role' : role}
    print("\nAccount created successfully!")

def login():
    username = input("\nEnter your username : ")
    password = getPassword()
    if username in users and users[username]['password']==password:
        print("Login Successful!")
        if users[username]['role'].lower()=='admin':
            adminMenu()
        else:
            userMenu(username)
    else:
        print("\nInvalid username or password")
        return False

def forgotPassword():
    username = input("\nEnter your username : ")
    if username in users:
        new_password = getPassword()
        users[username]['password'] = new_password
        print("Password reset successful!")
    else:
        print("Username not found!")

def adminMenu():
    while True:
        print("""
            ----------ADMIN MENU----------
            1- Add Book
            2- Delete Book
            3- Update Book
            4- View List of Books
            5- View List of Users
            6- View Borrowing History
            7- Manage Fines
            8- Logout """)
        try:
            choice = int(input("\nEnter your choice : "))
        except ValueError:
            print("Invalid Input!")
            continue

        if choice == 1:
            addBook()
        elif choice == 2:
            deleteBook()
        elif choice == 3:
            updateBook()
        elif choice == 4:
            viewBooks()
        elif choice == 5:
            viewUsers()
        elif choice == 6:
            view_BorrowingHistory()
        elif choice == 7:
            manageFines()
        elif choice ==8:
            print("\nSuccessfully Logged Out...")
            break
        else:
            print("Invalid choice!")
    
def addBook():
    bookId = input("\nEnter Book ID : ")
    if bookId in books:
        print("Book Id already exists!")
        return
    title = input("Enter Book Title : ")
    author = input("Enter Author Name : ")
    try : 
        quantity = int(input("Enter stock quantity : "))
    except ValueError:
        print("Invalid Input!")
        return
    books[bookId] = {'title' : title, 'author' : author, 'quantity' : quantity}
    print(f"\nBook {title} added successfully!")

def deleteBook():
    book_id = input("\nEnter Book Id to delete : ")
    if book_id in books:
        del books[book_id]
        print("Book {title} successfully deleted!")
    else:
        print("Book not found!")

def updateBook():
    book_id = input("\nEnter Book Id to update : ")
    if book_id in books:
        newTitle = input("Enter new title : ")
        newAuthor = input("Enter new author : ")
        try:
            newQuantity = int(input("Enter new stock quantity : "))
        except ValueError:
            print("Invalid Input!")
            return
        books[book_id] = {'title' : newTitle, 'author' : newAuthor, 'quantity' : newQuantity}
        print("\nBook updated successfully!")
    else:
        print("Book not found!")

def viewBooks():
    if not books:
        print("\nNo books available!")
    else:
        print("\nPrinting List of books...")
        for key,value in books.items():
            print("\nBook Id :",key,"\nBook Title :",value['title'],"\nAuthor Name :",value['author'], "\nStock Quantity :",value['quantity'])

def viewUsers():
    if not users:
        print("No users registered!")
    else:
        print("\nPrinting List of users...")
        for key,value in users.items():
            print(f"\nUsername : {key}  \nRole : {value['role']}")

def view_BorrowingHistory():
    if not borrowed_books:
        print("\nNo borrowing history available.")
        return
    
    print("\n-------- Borrowing History --------")
    for username, records in borrowed_books.items():
        print(f"\nUser: {username}")
        for book in records:
            print(f"  Book ID    : {book['Book Id']}")
            print(f"  Title      : {book['Title']}")
            print(f"  Issue Date : {book['Issue Date']}")
            print(f"  Due Date   : {book['Due Date']}")

def  manageFines():
    today = datetime.today().date()
    finePerDay = 5
    hasFine = False

    for record,username in borrowed_books.items():
        for book in record:
            due = book['Due Date']
            if today>due:
                late_days = (today-due).days
                fine = late_days*finePerDay
                print(f"{username} | {book['Title']} | Due: {due} | Late: {late_days} days | Fine: ₹{fine}")
                hasFine = True
    if not hasFine:
        print("\nNo overdue books. No fines.")


def userMenu(username):
    while True:
        print("""
            ----------USER MENU----------
            1- View Books
            2- Borrow Book
            3- Return Book
            4- View Borrowed Books
            5- Logout""")
        
        try:
            choice = int(input("\nEnter your choice : "))
        except ValueError:
            print("Invalid input!")
            continue

        if choice == 1:
            viewBooks()
        elif choice == 2:
            borrowBook(username)
        elif choice == 3:
            returnBook(username)
        elif choice == 4:
            view_borrowedBooks(username)
        elif choice == 5:
            print("\nSuccessfully Logged Out...")
            break
        else:
            print("Invalid choice!")

def borrowBook(username):
    book_id = input("\nEnter Book Id to borrow : ")

    if book_id not in books:
        print("Book Id does not exists!")
        return
    
    elif books[book_id]['quantity']==0:
        print(f"Book {books[book_id]['title']} is out of stock!")
        return
    else:
        books[book_id]['quantity']-=1

        issue_date = datetime.today().date()
        due_date = issue_date + timedelta(days = 14)

        borrow_record = {
            'Book Id' : book_id,
            'Title' : books[book_id]['title'],
            'Issue Date' : issue_date,
            'Due Date' : due_date
        }

        if username in borrowed_books:
            borrowed_books[username].append(borrow_record)
        else:
            borrowed_books[username] = [borrow_record]

    print(f"{username} has borrowed {books[book_id]['title']}")
    print(f"Issue Date : {borrow_record['Issue Date']}, due Date : {borrow_record['Due Date']}")

def returnBook(username):
    if username not in borrowed_books:
        print("You have no borrowed books.")
        return
    
    for record in borrowed_books[username]:
        print(f"\nBook ID : {record['Book Id']} \nTitle : {record['Title']}")

    book_id = input("\nEnter Book Id to return : ")

    for record in borrowed_books[username]:
        if record['Book Id']==book_id:
            borrowed_books[username].remove(record)
            books[book_id]['quantity']+=1
            print(f"{record['Title']} has been returned successfully")

print("You have not borrowed this book.")

def view_borrowedBooks(username):
    if username not in borrowed_books:
        print(f"{username} has not borrowed any books.")        
        return
    
    print(f"\nBooks borrowed by {username}:")
    for book in borrowed_books[username]:
        print(f"\nBook Id : {book['Book Id']}")
        print(f"Title : {book['Title']}")
        print(f"Issue Date : {book['Issue Date']}")
        print(f"Due Date : {book['Due Date']}")


if __name__ == "__main__":
    while True:
        print("""
            ----------Welcome to Library Management System----------
            1- Create Account
            2- Login
            3- Forgot password
            4- Exit """)
        
        choice = int(input("\nEnter your choice : "))

        if choice==1:
            createAccount()
        elif choice==2:
            login()
        elif choice==3:
            forgotPassword()
        elif choice==4:
            exit()
        else:
            print("Invalid Choice")
        