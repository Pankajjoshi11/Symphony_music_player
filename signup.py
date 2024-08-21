from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def clear():
    emailEntry.delete(0,END)
    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    confirmEntry.delete(0,END)
    check.set(0)

def connect_database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error','All fields are required')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error','Password Mismatch')
    elif check.get() == 0:
        messagebox.showerror('Error', 'PLease accept terms and conditions')
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='jmatheworden27')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Database connectivity issue, please try again')
            return
        try:
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)
            query = 'create table data(id int auto_increment primary key not null, email varchar(50), username varchar(100), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')

        query = 'select * from data where username=%s'
        mycursor.execute(query,(usernameEntry.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Username Already exists')
        else:
            query = 'insert into data(email,username,password) values(%s,%s,%s)'
            mycursor.execute(query,(emailEntry.get(),usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success','Registration is successful')
            clear()
            signup_window.destroy()
            import signinpage

def login_page():
    signup_window.destroy()
    import signinpage


signup_window = Tk()
signup_window.title('Signup Page')
signup_window.resizable(False,False)

background = ImageTk.PhotoImage(file='bg1.jpg')

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window,bg='light cyan')
frame.place(x=488, y=90)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 23, 'bold'),bg='light cyan',fg='steel blue')
heading.grid(row=0, column=0, padx=3, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 15, 'bold'),bg='light cyan')
emailLabel.grid(row=1, column=0, sticky='w', padx=30, pady=(0,0))

emailEntry = Entry(frame, width=28, font=('Microsoft Yahei UI Light', 15, 'bold'), bg='light blue1')
emailEntry.grid(row=2, column=0, sticky='w', padx=32)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 15, 'bold'),bg='light cyan')
usernameLabel.grid(row=3, column=0, sticky='w', padx=30, pady=(10,0))

usernameEntry = Entry(frame, width=28, font=('Microsoft Yahei UI Light', 15, 'bold'), bg='light blue1')
usernameEntry.grid(row=4, column=0, sticky='w', padx=32)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 15, 'bold'),bg='light cyan')
passwordLabel.grid(row=5, column=0, sticky='w', padx=30, pady=(10,0))

passwordEntry = Entry(frame, width=28, font=('Microsoft Yahei UI Light', 15, 'bold'), bg='light blue1')
passwordEntry.grid(row=6, column=0, sticky='w', padx=32)

confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 15, 'bold'),bg='light cyan')
confirmLabel.grid(row=7, column=0, sticky='w', padx=30, pady=(10,0))

confirmEntry = Entry(frame, width=28, font=('Microsoft Yahei UI Light', 15, 'bold'), bg='light blue1')
confirmEntry.grid(row=8, column=0, sticky='w', padx=32)

check = IntVar()
termsandconditions = Checkbutton(frame, text='I agree to the terms and conditions', font=('Microsoft Yahei UI Light', 13, 'bold'),bg='light cyan',activebackground='light cyan',cursor='hand2',variable = check)
termsandconditions.grid(row=9, column=0, sticky='w',padx=24,pady=5)

signupButton = Button(frame, text='Signup', font=('Open Sans', 16, 'bold'), bd=0, bg='light blue1', activebackground='light cyan',width=25,command=connect_database)
signupButton.grid(row=10, column=0, sticky='w', padx=40)

alreadyaccount = Label(frame, text="Don't have an account?", font=('Open Sans', 9, 'bold'), bg='light cyan')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=25, pady=11)

loginButton = Button(frame,text='Log In', font=('Open Sans',9,'bold underline'),bg='light cyan',activebackground='light cyan',cursor='hand2',bd=0,width=24, command=login_page)
loginButton.place(x=265,y=445)


signup_window.mainloop()