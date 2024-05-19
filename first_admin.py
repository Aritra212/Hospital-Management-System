# =============================================================
#   Project Title: Hospital Management System
#   Page Description: Add First Admin Page (If database is empty)
#   Author: Aritra Paul
#   Date: 19/04/2024
# ==============================================================

# Import necessary modules
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
import time
from reusable_function import id_generator

# Create the class that handled the Create First Admin window of the HMS system
class Create_Admin:

    def __init__(self,root,hname="Hospital Management System",parent=None):

        '''The constructor accept two arguments 1st- root name ,2nd- name of the hospital and it contain all display elements'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        self.parent=parent # Parent window name

        # Window configurations
        self.root.title("Create Admin - {}".format(self.hname)) # set the title
        self.root.geometry("400x520+530+220") # Set the window width, height and position
        self.root.wm_iconbitmap("../images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature

        self.root.focus_force()

        # Call add_admin() function to display the input fields
        self.add_admin()

    def add_admin(self):

        ''' Manage the output of the Add Admin form '''

        # -------------- local variables --------------------
        name_var= StringVar()
        guardian_name_var= StringVar()
        dob_var= StringVar()
        gender_var= StringVar()
        jdate_var= StringVar()
        profession_var= StringVar(value='Admin')
        department_var= StringVar(value='Management')
        post_var= StringVar()
        salary_var= StringVar()
        contact_var= StringVar()
        email_var= StringVar()
        password_var= StringVar()

        # create a list of the variables to share wiht other functions easily
        val_list=[name_var,guardian_name_var,dob_var,gender_var,jdate_var,profession_var,department_var,post_var,salary_var,contact_var,email_var,password_var]

        ### =============== Add Admin Form ===================

        Label(self.root,text="Create Admin ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw',padx=10,pady=5) 

        # To make the frame scrollable we need to use canvas becuse we can't make a frame scrollable in TK but canvas can have the scrollable property and we can also add a frame within a canvas.

        # So the logic is - First make a frame("canvas_container") within the root to contain the canvas("mycanvas"). Then create a canvas("mycanvas") within the frame "canvas_container" and make it scrollable afterthat create another frame named 'scrollable_frame1' within the cavas("mycanvas").

        canvas_container= Frame(self.root)  # Create the first frame
        canvas_container.pack(side=LEFT,anchor='nw')

        mycanvas= Canvas(canvas_container,width=343,height=450) # Create the canvas within the first frame
        mycanvas.pack(side=LEFT,pady=5,padx=15)

        # make the canvas scrollable
        y_scrollbar=Scrollbar(canvas_container, orient='vertical')
        y_scrollbar.pack(side=RIGHT, fill=Y)
        y_scrollbar.config(command=mycanvas.yview)

        mycanvas.configure(yscrollcommand=y_scrollbar.set)
        mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))

        # Create the second frame within the canvas
        scrollable_frame1= Frame(mycanvas)
        mycanvas.create_window((0,0),window=scrollable_frame1,anchor='nw')

        # Add fields into the second frame
        name_label=Label(scrollable_frame1,text="Employee's Name*",font=("arial",10,'bold'))
        name_label.grid(row=2,column=0,pady=6,sticky=W)
        name_entry=Entry(scrollable_frame1,textvariable=name_var,font=("arial",12))
        name_entry.grid(row=2,column=1,padx=5,pady=6)

        guardian_label=Label(scrollable_frame1,text="Guardian's Name*",font=("arial",10,'bold'))
        guardian_label.grid(row=3,column=0,pady=6,sticky=W)
        guardian_entry=Entry(scrollable_frame1,textvariable=guardian_name_var,font=("arial",12))
        guardian_entry.grid(row=3,column=1,padx=5,pady=6)

        dob_label=Label(scrollable_frame1,text="D.O.B*",font=("arial",10,'bold'))
        dob_label.grid(row=4,column=0,pady=6,sticky=W)
        dob_entry=Entry(scrollable_frame1,textvariable=dob_var,font=("arial",12))
        dob_entry.grid(row=4,column=1,padx=5,pady=6)

        gender_label=Label(scrollable_frame1,text="Select Gender",font=("arial",10,'bold'))
        gender_label.grid(row=5,column=0,pady=6,sticky=W)
        gender_combo=ttk.Combobox(scrollable_frame1,textvariable=gender_var,font=("arial",12),state='readonly',width=18)
        gender_combo['values']=('male','female','other')
        gender_combo.grid(row=5,column=1,padx=5,pady=6)

        # Get the date
        date_=time.strftime("%d-%m-%Y")
        # set the date
        jdate_var.set(date_)
        jdate_label=Label(scrollable_frame1,text="Joining Date",font=("arial",10,'bold'))
        jdate_label.grid(row=6,column=0,pady=6,sticky=W)
        jdate_entry=Entry(scrollable_frame1,textvariable=jdate_var,font=("arial",12))
        jdate_entry.grid(row=6,column=1,padx=5,pady=6)

        profession_label=Label(scrollable_frame1,text="Profession",font=("arial",10,'bold'))
        profession_label.grid(row=7,column=0,pady=6,sticky=W)
        profession_entry=Entry(scrollable_frame1,textvariable=profession_var,font=("arial",12),state='readonly')
        profession_entry.grid(row=7,column=1,padx=5,pady=6)

        department_label=Label(scrollable_frame1,text="Select Department*",font=("arial",10,'bold'))
        department_label.grid(row=8,column=0,pady=6,sticky=W)
        department_entry=Entry(scrollable_frame1,textvariable=department_var,font=("arial",12),state='readonly')
        department_entry.grid(row=8,column=1,padx=5,pady=6)
        
        post_label=Label(scrollable_frame1,text="Post",font=("arial",10,'bold'))
        post_label.grid(row=9,column=0,pady=6,sticky=W)
        post_entry=Entry(scrollable_frame1,textvariable=post_var,font=("arial",12))
        post_entry.grid(row=9,column=1,padx=5,pady=6)

        salary_label=Label(scrollable_frame1,text="Salary",font=("arial",10,'bold'))
        salary_label.grid(row=10,column=0,pady=6,sticky=W)
        salary_entry=Entry(scrollable_frame1,textvariable=salary_var,font=("arial",12))
        salary_entry.grid(row=10,column=1,padx=5,pady=6)


        contact_label=Label(scrollable_frame1,text="Mobile No.*",font=("arial",10,'bold'))
        contact_label.grid(row=11,column=0,pady=6,sticky=W)
        contact_entry=Entry(scrollable_frame1,textvariable=contact_var,font=("arial",12))
        contact_entry.grid(row=11,column=1,padx=5,pady=6)

        email_label=Label(scrollable_frame1,text="Email*",font=("arial",10,'bold'))
        email_label.grid(row=12,column=0,pady=6,sticky=W)
        email_entry=Entry(scrollable_frame1,textvariable=email_var,font=("arial",12))
        email_entry.grid(row=12,column=1,padx=5,pady=6)

        address_label=Label(scrollable_frame1,text="Address",font=("arial",10,'bold'))
        address_label.grid(row=13,column=0,pady=7,sticky=W)
        address_text=Text(scrollable_frame1,font=("arial",12),width=20,height=3)
        address_text.grid(row=13,column=1,padx=5,pady=6)

        password_label=Label(scrollable_frame1,text="Password*",font=("arial",10,'bold'))
        password_label.grid(row=14,column=0,pady=6,sticky=W)
        password_entry=Entry(scrollable_frame1,textvariable=password_var,font=("arial",12))
        password_entry.grid(row=14,column=1,padx=5,pady=6)

        clear_btn= Button(scrollable_frame1,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields(val_list,address_text))
        clear_btn.grid(row=15,column=1,padx=20,pady=10,sticky=W)

        save_btn= Button(scrollable_frame1,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.save_admin(val_list,address_text))
        save_btn.grid(row=15,column=1,padx=20,pady=10,sticky=E)

    def save_admin(self,values,addr):
        '''Used to add admin to the database. Take two arguments 1st- A list of values to be cleared, 2nd- address text.
        
        address text treated separately becuase Text has different syntax'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        # add address to the list
        val_list.append(addr.get("1.0",END))

        # remember the order of the values in the list here it is as follows-
        # val_list=[name,guardian name,dob, gender,joining date,profession,department,post,salary,contact,email,password,address]

        try:

            # Check the '*' marked fields is empty or not
            if val_list[0]=="" or val_list[1]=="" or val_list[2]=="" or val_list[6]=="" or val_list[9]=="" or val_list[10]=="" or val_list[11]=="":
                messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
            else:
                con=sqlite3.connect(database="hms1.db")
                cur=con.cursor()

                # Check the employees table to restrict duplicate entry
                cur.execute("select * from  employees where name=? and dob=? and guardian_name=?",(val_list[0],val_list[1],val_list[2]))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error",f"{val_list[0]} is already exist change name or other details to add new employee",parent=self.root)

                # otherwise add the admin data to the database
                else:
                    # generate ID for the Admin
                    n_id,err=id_generator('employees')
                    if err!='': 
                        messagebox.showerror("Error-05",f"Error due to {str(err)}",parent=self.root)
                    else:
                        cur.execute("insert into employees(id,name,guardian_name,dob,gender,joining_date,profession,department,post,salary,mobile,email,address,password) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
                            n_id,
                            val_list[0],
                            val_list[1],
                            val_list[2],
                            val_list[3],
                            val_list[4],
                            val_list[5],
                            val_list[6],
                            val_list[7],
                            val_list[8],
                            val_list[9],
                            val_list[10],
                            val_list[12],
                            val_list[11]
                        ))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Sucess!!","employee {}(id: {}) added to database sucessfully...".format(val_list[0],n_id),parent=self.root)

                        # call the login function
                        self.log_in(n_id,val_list[11])
        except Exception as exp:
            messagebox.showerror("Error-06",f"Error due to {str(exp)}",parent=self.root)

    def log_in(self,eid,password):

        ''' Redirect to the Administration page'''

        try:
            con=sqlite3.connect(database="hms1.db")
            cur=con.cursor()

            cur.execute("select * from employees where id=? and password=?",(eid,password))
            row=cur.fetchone()

            # import the Admin class
            from administration import Admin
            self.new_win=Toplevel(self.parent)
            self.new_obj=Admin(self.new_win,self.hname,self.parent,row)
            if self.parent!=None:
                self.parent.iconify() # Minimize the parent window
                self.root.destroy() # Destroy the first_admin window

            con.close()
        except Exception as exp:
            messagebox.showerror("Error-07",f"Error due to {str(exp)}",parent=self.root)
    
    def clear_fields(self,values,addr=''):

        '''Used to clear input fields. Take two arguments 1st- A list of values to be cleared, 2nd- address text.
        
        address text treated separately becuase Text has no method set(), we need to use delete() method to remove the text'''

        for value in values:
            value.set('')
        if addr!='':
            addr.delete('1.0',END)
    

# Main function
if __name__=='__main__':
    root=Tk()
    obj=Create_Admin(root,"Hopeview Medical Center")   # Create the object of the class Create_Admin
    root.mainloop()
