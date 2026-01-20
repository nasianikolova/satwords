from tkinter import * 
from dbrequests import DBRequests
from tkinter import messagebox
from user import User



window = Tk()
window.title('Login Page')
window.resizable(0, 0)
window.geometry('490x240+200+200')



def newone():
    window.withdraw()
    import registrationForm
    registrationForm.window.deiconify()


def Login():
    dbrequests = DBRequests()
    credentials = dbrequests.authenticateUser(emailEntry.get(), passwordEntry.get())  
    if len(credentials) != 0:
        for x in credentials:
            username = x[0]
            firstname = x[1]
            lastname = x[2]
            print(firstname + " " + lastname)
            user = User()
            user.set_connectedUser(username)

        messagebox.showinfo('Success', 'User Authenticated Successfully!')
        window.destroy()
        import words as words
    else:
        messagebox.showinfo('Failure', 'Authentication Failed!')

frame = Frame(window, width=700, height=400, bg='#4F93B8')
frame.place(x=10, y=0)

emailLabel = Label(frame, text='Email:', fg='white', compound=LEFT, bg='#4F93B8', font=('Calibri', 14, 'bold'))
emailLabel.grid(row=1, column=0, pady=20, padx=3)

passwordLabel = Label(frame, text='Password:', fg='white', compound=LEFT, bg='#4F93B8', font=('Calibri', 14, 'bold'))
passwordLabel.grid(row=3, column=0, pady=10, padx=3)

emailEntry = Entry(frame, width=39, bd=3)
emailEntry.grid(row=1, column=2, columnspan=2, padx=57)

passwordEntry = Entry(frame, width=39, show='*', bd=3)
passwordEntry.grid(row=3, column=2, columnspan=2, padx=57)

loginbtn = Button(frame, text='Login', bg='#7f7fff', pady=10, width=23, fg='white', font=('Calibri', 9, 'bold'), cursor='hand2', border=0, borderwidth=5, command = Login)
loginbtn.grid(row=9, columnspan=5, column=2, pady=30)

donthaveaccountLabel = Label(frame, text='Dont have an account?', fg='white', bg='#4F93B8', padx=4, font=('Calibri', 9, 'bold'))
donthaveaccountLabel.place(y=170)

createnewaccount = Button(frame, width=15, text='Create one', border=0, bg='white', cursor='hand2', fg='#4F93B8', font=('Calibri', 8, 'bold'), command=newone)
createnewaccount.place(x=10, y=199)


window.mainloop()
