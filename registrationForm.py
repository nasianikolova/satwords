from tkinter import * 
from tkinter import messagebox
from dbrequests import DBRequests

window = Tk()
window.title('Personal Registration Form')
window.geometry('540x640')
window.resizable(0,0)


def backbutton():
    window.withdraw()
    import login
    login.window.deiconify()

def submit():
    if firstnameEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter your First name')

    elif lastnameEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter your Last name')
    
    elif emailEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter your Email')
    
    elif usernameEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter your Username')

    elif passwordEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter your password')

    elif confirmpasswordEntry.get() == '':
        messagebox.showerror('Alert', 'Please confirm your password')

    elif passwordEntry.get() != confirmpasswordEntry.get():
        messagebox.showerror('Alert', 'Password do not match')

    else :
        dbrequests = DBRequests()
        dbrequests.insertUser(firstnameEntry.get(), lastnameEntry.get(), emailEntry.get(), usernameEntry.get(), passwordEntry.get())                
        messagebox.showinfo('Success', 'User Registered Successfully!')
            

firstname = StringVar()
lastname = StringVar()
email = StringVar()
username = StringVar()
password = StringVar()
confirmpassword = StringVar()

frame = Frame(window, width=610, height=640, bg='#4F93B8', bd=8)
frame.place(x=0, y=0)

heading = Label(frame, text="Personal Registration Form", fg='white', bg='#4F93B8', font=('Calibri', 28, 'bold'))
heading.place(x=90, y=3)

firstname = Label(frame, text='First Name:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
firstname.place(x=10, y=70)

firstnameEntry = Entry(frame, width=30, borderwidth=2,)
firstnameEntry.place(x=240, y=70)

lastname = Label(frame, text='Last Name:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
lastname.place(x=10, y=110)

lastnameEntry = Entry(frame, width=30, borderwidth=2,)
lastnameEntry.place(x=240, y=110)

email = Label(frame, text='Email:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
email.place(x=10, y=150)

emailEntry = Entry(frame, width=30, borderwidth=2,)
emailEntry.place(x=240, y=150)

username = Label(frame, text='Username:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
username.place(x=10, y=190)

usernameEntry = Entry(frame, width=30, borderwidth=2,)
usernameEntry.place(x=240, y=190)

password = Label(frame, text='Password:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
password.place(x=10, y=230)

passwordEntry = Entry(frame, width=30, borderwidth=2,)
passwordEntry.place(x=240, y=230)

confirmpassword = Label(frame, text='Confirm Password:', fg='white', bg='#4F93B8', font=('Calibri', 15, 'bold'))
confirmpassword.place(x=10, y=270)

confirmpasswordEntry = Entry(frame, width=30, borderwidth=2,)
confirmpasswordEntry.place(x=240, y=275)

submitbtn = Button(frame, text='Submit', bg='#7f7fff', width=15, borderwidth=5, height=2, border=2, font=('Calibri', 16, 'bold'), command = submit)
submitbtn.place(x=220, y=400)

bckbtn = Button(frame, text='<<', width=15, border=2, height=2, cursor='hand2', fg='white', bg='#4F93B8', command=backbutton)
bckbtn.place(x=0, y=550)

window.mainloop()