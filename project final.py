import datetime
from tabulate import tabulate
import art
import pyfiglet
import colorama
from colorama import Fore, Back
from termcolor import colored
colorama.init(autoreset=True)

def signUP():
    global GID
    mycur.execute('select * from guests')
    data = mycur.fetchall()
    if data == []:
        GID = 0  # if it is the first entry into table
    else:
        mycur.execute('select max(GID) from guests')
        dat = mycur.fetchall()
        for i in dat:
            GID = i[0]
    GID = GID + 1
    print('Your Guest ID is:', GID, '\nPlease note that this is your username.')
    Gname = input("Enter Your Name: ")
    while True:
        aadhar_no = int(input("Enter Your Aadhaar Number: "))
        if len(str(aadhar_no)) != 12:  # ensuring aadhaar no is 12 digits long
            print("Please make sure that your Aadhaar number is of 12 digits.")
        else:
            break
    address = input("Enter Address: ")
    while True:
        ph_no = input("Enter Phone Number: ")
        if len(ph_no) != 10:  # ensuring phone no is 10 digits long
            print("Please make sure your phone number is of 10 digits.")
        else:
            mycur.execute('select ph_no from guests')
            dat = mycur.fetchall()
            for i in dat:
                if ph_no in i:
                    print('There is already an account registered with this number.')
                    ph_no = input('Please enter another number:')
                    break
            break
    q2 = 'insert into guests values("%s","%s",%s,"%s","%s")' % (GID, Gname, aadhar_no, address, ph_no)
    mycur.execute(q2)
    mycon.commit()


def signIN():
    q1 = 'select GID from guests'
    mycur.execute(q1)
    data = mycur.fetchall()
    tid = ()
    for rec in data:
        tid += rec
    tphno = ()
    q2 = 'select ph_no from guests'
    mycur.execute(q2)
    data = mycur.fetchall()
    for rec in data:
        tphno += rec
    n = len(tid)
    d1 = {}
    for i in range(n):
        d1 = dict(zip(tid, tphno))  # creating dict with GID as keys and phone no as values
    print(d1)
    global GID  # GID is global as long as the same customer is logged in, ie, throughout this program
    while True:
        while True:
            GID = int(input('Enter your guest id: '))
            if type(GID) != int:
                print("Make sure to enter your correct Guest ID.")
            else:
                break
        ph_no = input('Enter your phone number: ')
        if GID not in d1.keys():
            print('Please sign up first.')
            signUP()
            break
        elif d1[GID] == ph_no:  # ensuring the phone no matches with the GID
            print('Logged in successfully.')
            break
        else:
            print('Incorrect phone number info.\nTry again.')


def modify_g():  # modifying guest details function
    while True:
        print('*What would you like to modify?')
        print('1.',colored('Name','yellow'))
        print('2.',colored('Aadhaar Number','blue'))
        print('3.',colored('Address','magenta'))
        print('4.',colored('Phone Number','cyan'))
        print('5.',colored('Go Back To Guest details','red'))
        ch = int(input('==> '))
        if ch == 1:
            name = input('Enter new name:')
            q = 'UPDATE guests set Gname="%s" where GID="%s"' % (name, GID)
            mycur.execute(q)
            mycon.commit()
            print("Your name has been changed.")
        elif ch == 2:
            while True:
                aadhar = int(input('Enter updated Aadhaar no:'))
                if len(str(aadhar)) != 12:
                    print("Make sure your Aadhaar number is of 12 digits.")
                else:
                    break
            q = 'UPDATE guests set aadhaar_no="%s" where GID="%s"' % (aadhar, GID)
            mycur.execute(q)
            mycon.commit()
            print("Your Aadhaar number has been updated.")
        elif ch == 3:
            address = input('Enter updated address:')
            q = 'UPDATE guests set address="%s" where GID="%s"' % (address, GID)
            mycur.execute(q)
            mycon.commit()
            print('Your address has been updated.')
        elif ch == 4:
            while True:
                ph_no = input('Enter updated phone number: ')
                if len(ph_no) != 10:
                    print("Make sure your phone number is of 10 digits.")
                else:
                    break
            q = 'UPDATE guests set ph_no="%s" where GID="%s"' % (ph_no, GID)
            mycur.execute(q)
            mycon.commit()
        elif ch == 5:
            break
        else:
            print("Please enter a valid option.")


def g_details():
    while True:
        print('\n*GUEST DETAILS')
        print('1.',colored('View Details','magenta'))
        print('2.', colored('Modify Details','green'))
        print('3.', colored('Go back to Main Menu','red'))
        gst_choice = input("==>")
        if gst_choice == '1':
            mycur.execute("use hotel")
            mycur.execute("select * from guests where GID=%s" % (GID))
            g_data = mycur.fetchall()
            print(tabulate(g_data, headers=['Guest-id', 'Guest Name', 'Aadhaar no.', 'Address', 'Phone no.'],
                           tablefmt='psql'))  # printing the guests details in a tabular form
        elif gst_choice == '2':
            modify_g()
        elif gst_choice == '3':
            break
        else:
            print('Enter a valid option.')


def booking_details():
    while True:

        print('\n*BOOKINGS')
        print('1.',colored('Add a new booking','magenta'))
        print('2.',colored('View my bookings','blue'))
        print('3.',colored('Cancel a booking','yellow'))
        print('4.',colored('Go back to Main Menu','red'))
        book_choice =input("==> ")

        if book_choice == '1':
            mycur.execute('select * from bookings')
            data = mycur.fetchall()
            if data == []:
                BID = 99    # the booking ID starts from 100
            else:
                mycur.execute('select max(BID) from bookings')
                dat = mycur.fetchall()
                for i in dat:
                    BID = i[0]
            BID = BID + 1    # further BIDs getting increased

            print('Our hotel offers a collection of rooms to choose from. The specifics are given below:')
            try:
                check__in = input('Enter check-in date (YYYY-MM-DD):')
                check_in = datetime.date(int(check__in[0:4]), int(check__in[5:7]), int(check__in[8:]))  #converting to datetime format
                check__out = input('Enter check-out date (YYYY-MM-DD):')
                check_out = datetime.date(int(check__out[0:4]), int(check__out[5:7]), int(check__out[8:]))
            except ValueError:
                print('Please enter valid dates')
                check__in = input('Enter check-in date (YYYY-MM-DD):')
                check_in = datetime.date(int(check__in[0:4]), int(check__in[5:7]), int(check__in[8:]))
                check__out = input('Enter check-out date (YYYY-MM-DD):')
                check_out = datetime.date(int(check__out[0:4]), int(check__out[5:7]), int(check__out[8:]))

            n = 1
            lst = []
            rid_dict = {}
            R = []
            mycur.execute("select distinct type, costPD from rooms where availability='Y'")
            r_data = mycur.fetchall()
            mycur.execute("select check_in, check_out, RID from bookings")
            b_data = mycur.fetchall()
            mycur.execute("select RID, type from rooms where availability='Y'")
            rno_data = mycur.fetchall()
            dt = dict(rno_data)

            for b in b_data:
                if check_in <= b[0] <= check_out or check_in <= b[1] <= check_out:  # checking if room is occupied in the given duration
                    R.append(b[2])  # R- list containing RIDs of bookings having same duration of stay as the selected dates

            for r in r_data:
                mycur.execute('select b.RID, r.type from bookings b, rooms r where b.RID=r.RID and type="%s"' % (r[0]))
                mycur.fetchall()
                if mycur.rowcount < 5:  # ensuring that not all 5 rooms of the same type are already booked for same dates
                    lst.append((n, r[0], r[1]))
                    n += 1

            for i in dt:
                if i not in R:
                    rid_dict[i] = dt[i]

            if lst == []:
                print('Sorry, there are no rooms available for the selected dates.')
            else:
                print("Available rooms are: ")
                print(tabulate(lst, headers=['Sl. no.', 'Room Type', 'Cost Per Night'], tablefmt='psql'))
                try:
                    room = int(input("Enter the choice of room\n==> "))  #accepting type of room from user
                except ValueError:
                    room=int(input("Please enter a valid serial number for choice of room==>"))
                for i in lst:
                    if i[0] == room:  #selecting Room ID for selected type of room
                        Type = i[1]
                        for i in rid_dict:
                            if rid_dict[i] == Type:
                                RID = i      #assigning Room ID
                                break
                        else:
                            break

                        print(colored('Your booking was successful ✨','green'))
                        lst1=[(BID,RID,Type,check__in+' to '+check__out)]
                        print('Your room-', RID, 'with Booking ID-', BID, 'has been booked from', check__in, 'to',check__out)
                        print(tabulate(lst1, headers=['Booking ID', 'Room ID','Room Type','Duration'], tablefmt='psql'))
                        mycur.execute('select curdate()')
                        data = mycur.fetchone()
                        if data[0] == check_in:
                            mycur.execute('update rooms set availability="N" where RID="%s"' % (RID))
                            mycon.commit()    # updating the availabilty of the rooms depending on the check in and check out date
                        if data[0] == check_out:
                            mycur.execute('update rooms set availability="Y" where RID="%s"' % (RID))
                            mycon.commit()
                        q = "insert into bookings values(%s,%s,'%s','%s','%s')" % (BID, GID, RID, check_in, check_out)
                        mycur.execute(q)
                        mycon.commit()
                        break
                else:
                    print('Invalid serial number entered. Please restart booking process.')

        elif book_choice == '2':
            mycur.execute("use hotel")
            mycur.execute("select * from bookings where GID=%s" % (GID))
            b_data = mycur.fetchall()
            print(tabulate(b_data, headers=['Booking-id', 'Guest-id', 'Room-id', 'Check-in date', 'Check-out date'],
                           tablefmt='psql'))  # printing the bookings table in a tabular form
            print()

        elif book_choice == '3':
            try:
                del_book = int(input("Enter the Booking ID of the booking you want to cancel\n==>"))
            except:
                del_book=int(input("Please make sure you enter your Booking ID correctly.\n==>"))
            ch = input('Are you sure you want to proceed? (y/n): ')
            if ch == 'y':
                q5 = "DELETE FROM bookings WHERE BID= '%s'" % (del_book)  # cancelling booking
                mycur.execute(q5)
                mycon.commit()
                print('Your booking has been cancelled.')
            print()

        elif book_choice == '4':
            break

        else:
            print("Please enter a valid option.")


def rooms_info():  # all rooms in the hotel
    print()
    print('''Room services are available 24 hours. Complimentary WiFi is available in all rooms.
Luxurious and elegant, all the air-conditioned guestrooms enjoy beautiful garden views. 
A flat-screen TV, personal safe and tea/coffee facilities are included. 
En suite bathrooms come with hot-water showers and Ayurvedic toiletries.''')
    colors = ['red','red', 'yellow', 'green', 'cyan', 'blue', 'magenta','red','yellow','green','cyan','cyan','blue']
    for color, n in zip(colors, '🌟 Deluxe room'):
        print(colored(n, color), end="")
    print('''
    This spacious room offers one double bed and a couch.
    2 people
    Rs. 6050 per night
    ''')
    colors = ['cyan','red','red', 'yellow', 'green', 'cyan', 'blue', 'magenta','red','yellow','green','cyan']
    for color, n in zip(colors,'🌟 Mini Suite'):
        print(colored(n, color), end='')
    print('''
    This suite offers a double bed along with a sofa and a minibar.
    2 people
    Rs. 6200 per night
    ''')
    colors = ['green','red', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red','yellow','green','cyan','blue','magenta','red','yellow','green']
    for color, n in zip(colors,'🌟 Grand Twin Room'):
        print(colored(n, color), end='')
    print('''
    This family room offers two double beds in two adjacent connected rooms. It also features a comfortable sofa.
    5 people
    Rs.7000 per night
    ''')
    colors = ['yellow', 'red', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red', 'yellow', 'green', 'cyan','blue', 'magenta', 'red']
    for color, n in zip(colors, '🌟 Veranda Suite'):
        print(colored(n, color), end='')
    print('''
    This suite features a veranda displaying beautiful garden or city views. It offers one double bed and one single bed.
    3 people
    Rs. 7500 per night
    ''')
    colors = ['magenta','magenta', 'red', 'yellow', 'green', 'cyan', 'blue','blue', 'magenta', 'red', 'yellow', 'green', 'cyan','cyan','magenta', 'red', 'yellow','green','cyan']
    for color, n in zip(colors, '🌟 Grand Royal Suite'):
        print(colored(n, color), end="")
    print('''
    This luxurious and royal suite comes with one double bed, a separate lounge, a private jacuzzi and a minibar.
    2 people
    Rs.9999 per night''')
    print()


import mysql.connector as mysql  # connecting to mysql

mycon = mysql.connect(host='localhost', user='root', passwd='dpsbn')
if mycon.is_connected() == False:
    print('Error in connecting to SQL')
else:
    mycur = mycon.cursor()
    mycur.execute('create database if not exists hotel')  # hotel database created
    mycur.execute('use hotel')
    q1 = 'create table if not exists guests(GID int primary key , Gname varchar(30) not null, aadhaar_no char(12) unique, address varchar(50) not null, ph_no varchar(10) unique not null)'
    mycur.execute(q1)  # creating guest table

    # creating room table
    # Veranda suite, deluxe room, grand executive suite, mini suite, grand twin room
    # if table exists, do not execute this as it gives primary key error
    mycur.execute('show tables')
    tables = mycur.fetchall()
    l = tuple()
    for i in range(len(tables)):
        l = l + tables[i]  # l is a tuple containing table names
    if 'rooms' not in l:
        q2 = "create table if not exists rooms(RID char(2) primary key , type varchar(30) not null, costPD int not null, availability char(1) default('Y'))"
        mycur.execute(q2)
        a = 'A0'  # adding rooms to the rooms table with different room IDs
        for i in range(5):
            a = 'A' + str(int(a[1]) + 1)
            b = 'Deluxe Room'
            c = 6050
            mycur.execute("insert into rooms(RID, type, costPD) values('%s','%s',%s)" % (a, b, c))
            mycon.commit()

        a = 'B0'
        for i in range(5):
            a = 'B' + str(int(a[1]) + 1)
            b = 'Mini Suite'
            c = 6200
            mycur.execute("insert into rooms(RID, type, costPD) values('%s','%s',%s)" % (a, b, c))
            mycon.commit()

        a = 'C0'
        for i in range(5):
            a = 'C' + str(int(a[1]) + 1)
            b = 'Grand Twin Room'
            c = 7000
            mycur.execute("insert into rooms(RID, type, costPD) values('%s','%s',%s)" % (a, b, c))
            mycon.commit()

        a = 'D0'
        for i in range(5):
            a = 'D' + str(int(a[1]) + 1)
            b = 'Veranda Suite'
            c = 7500
            mycur.execute("insert into rooms(RID, type, costPD) values('%s','%s',%s)" % (a, b, c))
            mycon.commit()

        a = 'E0'
        for i in range(5):
            a = 'E' + str(int(a[1]) + 1)
            b = 'Grand Royal Suite'
            c = 9999
            mycur.execute("insert into rooms(RID, type, costPD) values('%s','%s',%s)" % (a, b, c))
            mycon.commit()

    q2 = "create table if not exists bookings(BID int primary key, GID int, RID char(2), check_in date not null, check_out date not null, foreign key(GID) references guests(GID), foreign key(RID) references rooms(RID))"
    mycur.execute(q2)  # creating bookings table

name='HOTEL     JAYARIA'
a=art.text2art(name,font='big',chr_ignore=True)
t = Fore.LIGHTWHITE_EX+Back.CYAN +a
print(t)
colors= ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
for n in range(len(colors)):
    for color in colors:
        print(" " * n, end='')
        print(colored('X', color), end="")
    print()



fobj = open('About.txt', 'w+')  # creating and opening text file for writing and reading
abt = '''ABOUT: Award-winning gardens with century-old rain-trees are featured throughout Hotel Jayaria, a 5-star property on the prestigious Mahatma Gandhi Road. 
Personal butlers and room service are available 24 hours. Complimentary WiFi is available in all rooms.
Jayaria features a rooftop swimming pool, an arcade, a convention hall, pampering spa treatments and a gym. We offer complimentary breakfast, laundery services and 24/7 house-keeping services.
Luxurious and elegant, all the air-conditioned guestrooms enjoy beautiful garden views. 
Located in the heart of the Bengaluru city, the hotel is within 2 km from M.G. Road, Brigade Road and Commercial Street. It is a 30-minute drive from Cantonment Railway Station and a 1-hour 30-minute drive from Bangalore Airport.'''
fobj.write(abt)  # writing into text file
fobj.seek(0)
print(fobj.read())  # printing file content
print('*' * 30)

import mysql.connector as mysql

mycon = mysql.connect(host='localhost', user='root', passwd='dpsbn')
if mycon.is_connected() == False:
    print('Error in connecting to SQL')
else:
    mycur = mycon.cursor()
    mycur.execute('create database if not exists hotel')  # hotel database created
    mycur.execute('use hotel')
    while True:
        print('1.',colored('Create a new account', 'green'))
        print('2.',colored('Already have an existing account?','blue'))
        ch=input('==>')
        if ch == '1':
            signUP()
            break
        elif ch == '2':
            signIN()
            break
        else:
            print("Please enter a valid option.")

    while True:
        print('*'*30)
        result = pyfiglet.figlet_format("HOTEL JAYARIA", font="digital")
        print(result)
        print('* What would you like to do today?')
        print('1.',colored('Manage Guest Details','magenta'))
        print('2.',colored('View All Hotel Rooms','blue'))
        print('3.',colored('Manage Bookings','yellow'))
        print('4.',colored('Exit','red'))
        ch=input('==>')
        if ch == '1':
            g_details()
        elif ch == '2':
            rooms_info()
        elif ch == '3':
            booking_details()
        elif ch == '4':
            colors = ['yellow', 'red', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red', 'yellow', 'green',
                      'cyan', 'blue', 'magenta', 'red','yellow', 'red', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red', 'yellow', 'green',
                      'cyan', 'blue', 'magenta', 'red','yellow', 'red', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red', 'yellow', 'green',
                      'cyan', 'blue']
            for color, n in zip(colors, 'Thank you! Have a nice stay!! Visit again ✨'):
                print(colored(n, color),end='')
            break
        else:
            print("Please enter a valid option.")