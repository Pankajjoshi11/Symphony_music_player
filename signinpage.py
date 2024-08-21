from tkinter import messagebox
import pymysql
from tkinter import *
from PIL import ImageTk
import mysql.connector

#functionality Part
def open_main():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jmatheworden27",
        database="userdata"
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Retrieve the username and password entered by the user
    username = usernameEntry.get()
    password = passwordEntry.get()

    # Query the database to retrieve the user's information based on the entered username
    query = "SELECT * FROM data WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        # If the user exists, verify the password
        if user[3] == password:
            print("Login successful")
            login_window.destroy()
            import main1
        else:
            messagebox.showerror('Error','Password Mismatch')
            
    else:
        messagebox.showerror('Error','User not found')
        print("User not found")

    # Close the cursor and database connection
    cursor.close()
    conn.close()
    


def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file='closeeye1.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye1.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)
def user_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0, END)

#GUI part
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0,0)
login_window.title('Login Page')
bgImage = ImageTk.PhotoImage(file='bg1.jpg')

bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0,y=0)

heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'),bg='light cyan',fg='steel blue')
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25,font=('Microsoft Yahei UI Light', 16, 'bold'),bd=0)
usernameEntry.place(x=540,y=200)
usernameEntry.insert(0,'Username')

usernameEntry.bind('<FocusIn>', user_enter)

frame1 = Frame(login_window,width=325, height=2,bg='steel blue')
frame1.place(x=540,y=230)

passwordEntry = Entry(login_window, width=25,font=('Microsoft Yahei UI Light', 16, 'bold'),bd=0)
passwordEntry.place(x=540,y=260)
passwordEntry.insert(0,'Password')

passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(login_window,width=325, height=2,bg='steel blue')
frame2.place(x=540,y=290)

openeye = PhotoImage(file='openeye1.png')
eyeButton = Button(login_window, image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=840, y=260)

forgetButton = Button(login_window, text='Forgot Password?',bd=0,bg='light cyan',activebackground='light cyan',cursor='hand2',font=('Microsoft Yahei UI Light', 11, 'bold'))
forgetButton.place(x=720, y=305)

loginButton = Button(login_window,text='Login', font=('Open Sans',16,'bold'),bg='light blue1',activebackground='light blue1',cursor='hand2',bd=0,width=24,command=open_main)
loginButton.place(x=540,y=350)

orLabel = Label(login_window,text='------------------------OR-----------------------',font=('Open Sans',18),bg='light cyan',width=22)
orLabel.place(x=540,y=415)

signupLabel = Label(login_window,text="Don't have an account?",font=('Open Sans',13,'bold'),bg='light cyan',width=22)
signupLabel.place(x=520,y=480)

newaccountButton = Button(login_window,text='Create new one', font=('Open Sans',9,'bold underline'),bg='light cyan',activebackground='light cyan',activeforeground='blue',cursor='hand2',bd=0, command=signup_page)
newaccountButton.place(x=758,y=480)

login_window.mainloop()

