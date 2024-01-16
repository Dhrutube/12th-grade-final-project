import mysql.connector as mys   #module used
mycon = mys.connect(host = "localhost", user = "root", passwd = "D@hruv13", database = "sleeptracker")   #establishing connection
mycursor = mycon.cursor()   #creating cursor object

#function used to verify password
def pwd_check():
    id_ = int(input("\nEnter user ID : "))
    pwd = input("Enter password: ")
    q = "select * from users where userid = {}".format (id_)
    mycursor.execute(q)
    rec = mycursor.fetchone()   #taking a record of user to verify password
    if rec[1] != pwd:
        return False, None   #None included because all functions make use of chk[0], the return variable used for pwd_check() 
    else:
        return True, id_   #returning id since following functions require it
#chk[0] is used in all functions in if: clause since pwd_check returns (True, id_) or (False, None) tuple

#function for a user to view their records
def viewuser():
    chk = pwd_check()
    if chk[0]:
        q = "select * from users where userid = {}".format (chk[1])   #fetching record of user with id specified
        mycursor.execute(q)
        rec = mycursor.fetchone()
        print(f"\nUser ID = {rec[0]}")
        print(f"Name = {rec[2]}")
        print(f"Age = {rec[3]}")
    else:
        print("wrong password!")

#function for adding a new user to the database        
def adduser():
    pwd = input("\nSet password: ")
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    q = "insert into users(password, name, age) values('{}', '{}', {})".format (pwd, name, age)
    mycursor.execute(q)
    mycon.commit()   #updating actual database
    q1 = "select * from users"
    mycursor.execute(q1)
    id_retr = mycursor.fetchall()   #to display user data
    id_ = id_retr[-1][0]
    print("\nYour profile:")
    print(f"ID: {id_}")
    print(f"Name: {name}")
    print(f"Age: {age}")

def modifyuser():
    print("\n1. name\n2. age")
    chg = int(input("Enter data to be changed: "))
    #for changing name of user
    if chg == 1:
        chk = pwd_check()
        if chk[0]:            
            nname = input("Enter updated name: ")
            q = "update users set name = '{}' where userid = {}".format (nname, chk[1])
            mycursor.execute(q)
        else:
            print("wrong password!")
    #for changing age of user
    elif chg == 2:
        chk = pwd_check()
        if chk[0]:
            nage = int(input("Enter updated age: "))
            q = "update users set age = {} where userid = {}".format (nage, chk[1])
            mycursor.execute(q)
        else:
            print("wrong password!")
    else:
        print("invalid input, try again")
    mycon.commit()   #updating actual database
    
def addsleep():
    chk = pwd_check()
    if chk[0]:
        hr = int(input("Enter hours slept : "))
        qlt = int(input("Enter quality of sleep(1-10) : "))
        w = "select week(now())"
        mycursor.execute(w)
        wnt = mycursor.fetchone()   #week number record
        wn = wnt[0]   #week number
        d = "select weekday(now())"
        mycursor.execute(d)
        dyt = mycursor.fetchone()   #day number record
        dy = dyt[0]   #day number
        #0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday
        q = "insert into tracker values({}, {}, {}, {}, {})".format (wn, chk[1], dy, hr, qlt)
        mycursor.execute(q)
        mycon.commit()   #updating actual database
    else:
        print("wrong password!")
    
def viewsleep():
    chk = pwd_check()
    if chk[0]:
        day = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}   #since daynumber if stored int type
        q = "select * from tracker where userid = {}".format (chk[1])
        mycursor.execute(q)
        sleepdata = mycursor.fetchall()   #all sleep entries of user till date
        if sleepdata:
            for rec in sleepdata:
                print(f"\nweekno = {rec[0]}")
                print(f"day = {day[rec[2]]}")
                print(f"hours = {rec[3]}")
                print(f"quality = {rec[4]}")
        else:
            print("no data to be displayed")
    else:
        print("wrong password!")

#for all functions related to data of users
def usermenu():
    print("\n1. View user\n2. Add user\n3. Modify user\n4. Main menu")
    uopt = int(input("Enter choice number : "))
    if uopt == 1:
        viewuser()
    elif uopt == 2:
        adduser()
    elif uopt == 3:
        modifyuser()
    elif uopt == 4:
        return

#for all functions related to a specific user's sleep data
def trackermenu():
    print("\n1. Add sleep data\n2. View sleep data\n3. Main menu")
    topt = int(input("Enter choice number : "))
    if topt == 1:
        addsleep()
    if topt == 2:
        viewsleep()
    elif topt == 3:
        return

#to view sleep report of a specific user
def reportmenu():
    chk = pwd_check()
    if chk[0]:
        q1 = "select age from users where userid = {}".format (chk[1])
        mycursor.execute(q1)
        aget = mycursor.fetchone()
        age = aget[0]
        q2 = "select avg(hours), avg(quality) from tracker where userid = {}".format (chk[1])
        mycursor.execute(q2)
        recs = mycursor.fetchone()
        avghr = recs[0]
        avgq = recs[1]
        print(f"Your average sleep quality reported: {avgq}")
        if age < 1:
            print("\nYour ideal sleep range = 13-16 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 13:
                print("Result: Undersleeping")
            elif avghr > 16:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif 1 <= age <= 2:
            print("Your ideal sleep range = 11-14 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 11:
                print("Result: Undersleeping")
            elif avghr > 14:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif 3 <= age <= 5:
            print("Your ideal sleep range = 10-13 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 10:
                print("Result: Undersleeping")
            elif avghr > 13:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif 6 <= age <= 13:
            print("Your ideal sleep range = 9-11 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 9:
                print("Result: Undersleeping")
            elif avghr > 11:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif 14 <= age <= 17:
            print("Your ideal sleep range = 8-10 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 8:
                print("Result: Undersleeping")
            elif avghr > 10:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif 18 <= age <= 64:
            print("Your ideal sleep range = 7-9 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 7:
                print("Result: Undersleeping")
            elif avghr > 9:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
        elif age >= 65:
            print("Your ideal sleep range = 7-8 hours")
            print(f"Your average sleep per night = {avghr}")
            if avghr < 7:
                print("Result: Undersleeping")
            elif avghr > 8:
                print("Result: Oversleeping")
            else:
                print("Result: Healthy amount of sleep")
    else:
        print("wrong password!")
    
#mainmenu, to access all sub-functions
print("Welcome to SleepTracker!")
while True:
    print("\n1. User Management\n2. Tracker\n3. Reports\n4. Exit")
    opt = int(input("Enter choice number : "))
    if opt == 1:
        usermenu()
    elif opt == 2:
        trackermenu()
    elif opt == 3:
        reportmenu()
    elif opt == 4:   #terminating program
        print("\nThank you for using SleepTracker!")
        print("Credits:\nDhruv Sehgal\nRushil Saini\nNikunj Rai Juneja")
        break
