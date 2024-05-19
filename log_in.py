# =============================================================
#   Project Title: Hospital Management System
#   Page Description: Login Page
#   Author: Aritra Paul
#   Date: 19/04/2024
# ==============================================================

# Import necessary modules
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3

# Create the class that handled the Login feature of the system

class Login:
    def __init__(self,root,hname="Hospital Management System",parent=None,prof= "admin"):

        '''The constructor accept 4 arguments 1st- root name ,2nd- name of the hospital, 3rd- parent window name, 4th- profession of the employee and it contain all display elements'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        self.parent=parent # Parent window name
        self.profession_var=prof # Profession of the employee who wants to loogged in

        # Window configurations
        self.root.title("Login - {}".format(self.hname)) # set the title
        self.root.geometry("500x300+530+220") # Set the window width, height and position
        self.root.wm_iconbitmap("../images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature

        self.root.focus_force()

        # -----------------  Varibles -------------------

        self.id_var= StringVar()
        self.password_var= StringVar()

        ### ================ Login ======================

        # Now to manage all features I divide the whole window into two sections named as Left & Right Frames.

        # The Left frame contain a image and the Right frame contain  a form to take the informations (id, password) from the employee.

        ## ================ Left Frame ====================

        left_frame= Frame(self.root,background="white")
        left_frame.place(x=0,y=0,width=255,height=300)

        self.left_img=Image.open("../images/doc_p2.png")
        self.left_img=self.left_img.resize((210,200))
        self.left_img=ImageTk.PhotoImage(self.left_img)
        left_img_label=Label(self.root,image= self.left_img,background="white")
        left_img_label.place(x=10,y=40)

        ## ================== Right Frame ==================

        right_frame= Frame(self.root,pady=10,padx=5)
        right_frame.place(x=262,y=0,width=245,height=300)

        Label(right_frame,text="Login",font=("arial",15,'bold'),fg="#14213d",justify='center',pady=10).grid(row=0,column=0,columnspan=2)

        Label(right_frame,text="",font=("arial",10,'bold')).grid(row=1,column=0,sticky=W)
        id_label=Label(right_frame,text="Employee Id",font=("arial",10,'bold'))
        id_label.grid(row=3,column=0,sticky=W)
        id_entry=Entry(right_frame,textvariable=self.id_var,font=("arial",10),width=17)
        id_entry.grid(row=3,column=1,padx=5,pady=6)

        password_label=Label(right_frame,text="Password",font=("arial",10,'bold'))
        password_label.grid(row=4,column=0,sticky=W)
        password_entry=Entry(right_frame,textvariable=self.password_var,font=("arial",10),width=17)
        password_entry.grid(row=4,column=1,padx=5,pady=6)

        login_btn= Button(right_frame,text="Login",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.login)
        login_btn.grid(row=5,column=1,pady=30,sticky=E)

    def login(self):

        ''' Check the id, password if valid then open the desired window (i.e. Admin window, Receptionsist window etc.)'''

        # Check any input field empty or not
        if self.id_var.get()=="" or self.password_var.get()=="":
            messagebox.showerror("Login failure!!","All fields must be filled",parent=self.root)
        # If both the field have values then match those values 
        else:
            con=sqlite3.connect(database="hms1.db")
            cur=con.cursor()
            try:
                cur.execute("select * from employees where id=? and password=?",(self.id_var.get(),self.password_var.get()))
                row=cur.fetchone()
                # if no employee found
                if row==None:
                    messagebox.showerror("Login Erro",f"Invalid User!! Check ID and Password",parent=self.root)
                # otherwise
                else:
                    # Match the profession to restrict access
                    if self.profession_var=='admin' and row[6]=="Admin":
                        from administration import Admin
                        self.new_win=Toplevel(self.parent)
                        self.new_obj=Admin(self.new_win,self.hname,self.parent,row)
                        if self.parent!=None:
                            self.parent.iconify()
                            self.root.destroy()
                    elif self.profession_var=='receptionist' and row[6]=="Receptinist":
                        from receptionist import RPT
                        self.new_win=Toplevel(self.parent)
                        self.new_obj=RPT(self.new_win,self.hname,self.parent,row)
                        if self.parent!=None:
                            self.parent.iconify()
                            self.root.destroy()
                    elif self.profession_var=='accountant' and row[6]=="Accountant":
                        from accountant import Acc
                        self.new_win=Toplevel(self.parent)
                        self.new_obj=Acc(self.new_win,self.hname,self.parent,row)
                        if self.parent!=None:
                            self.parent.iconify()
                            self.root.destroy()
                    else:
                        messagebox.showerror("Access Denied","This type of user cannot access this feature",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-04",f"Error due to {str(exp)}",parent=self.root)
            con.close()

# Main function
if __name__=='__main__':
    root=Tk()
    obj=Login(root,"Hopeview Medical Center")   # Create the object of dashboard class HMS
    root.mainloop()