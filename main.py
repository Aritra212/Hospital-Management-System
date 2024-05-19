# =============================================================
#   Project Title: Hospital Management System
#   Page Description: Dashboad Page
#   Author: Aritra Paul
#   Date: 19/04/2024
# ==============================================================

# Import necessary modules
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import time
import sqlite3

# Create the class that handled the dashbord of the system

class HMS:
    
    def __init__(self,root,hname="Hospital Management System"):

        '''The constructor accept two arguments 1st- root name ,2nd- name of the hospital and it contain all display elements'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        
        # Window configurations
        self.root.title("Dashboard - {}".format(self.hname)) # set the title
        self.root.geometry("1350x700+100+70") # Set the window width, height and position
        self.root.wm_iconbitmap("../images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature

        ### =============== Title Bar ===================
        self.title_icon=Image.open("../images/hms_logo1.png")
        self.title_icon=self.title_icon.resize((50,50))
        self.title_icon=ImageTk.PhotoImage(self.title_icon)
        title=Label(self.root,text=self.hname, image= self.title_icon,compound=LEFT,font=("arial black",20),bg="#2b2d42",fg="#edf2f4",padx=10)
        title.place(x=0,y=0,relwidth=1,height=70)

        ### ================ Sub Title Bar ================
        self.sub_title=Label(self.root,text="Welcome to {} \t\t Date: DD-MM-YYY \t\t Time: HH:MM:SS".format(self.hname),font=("Cooper Std Black",13,"bold"),bg="#ef233c",fg="#ffffff")
        self.sub_title.place(x=0,y=70,relwidth=1,height=30)

        self.update_date_time() # Handle the date and the clock

        ### ================ Dashboard ======================

        # Now to manage all features I divide the whole window into two sections named as Left & Right Frames.

        # The Left frame contain the Login buttons and the Right frame contain the informations of the hospital.

        ## ================ Left Frame ====================
        left_frame=Frame(self.root,bd=2,relief=RIDGE,bg="#e5e5e5")
        left_frame.place(x=0,y=100,width=400,height=595)

        # ----------------- Login Buttons -----------------

        # Button for Receptionist Login
        res_btn=Button(left_frame,text="Receptionist Login",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",18),pady=15,cursor="hand2",command= lambda: self.login_window("receptionist"))
        res_btn.pack(fill=X,pady=10)

        # Button for Administration Login
        admin_btn=Button(left_frame,text="Administration Login",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",18),pady=15,cursor="hand2",command=lambda: self.login_window("admin"))
        admin_btn.pack(fill=X,pady=10)

        # Button for Accountant Login
        acc_btn=Button(left_frame,text="Accountant Login",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",18),pady=15,cursor="hand2",command=lambda: self.login_window("accountant"))
        acc_btn.pack(fill=X,pady=10)

        # Place the Hospital's Logo , Image size 450x450
        self.name_logo=Image.open("../images/hms_name_logo.png")
        self.name_logo=self.name_logo.resize((450,450))
        self.name_logo=ImageTk.PhotoImage(self.name_logo)
        lbl_name_logo=Label(left_frame,image=self.name_logo,bg="#e5e5e5")
        lbl_name_logo.pack(side=BOTTOM,fill=X)

        ## ================== Right Frame =================
        right_frame=Frame(self.root)
        right_frame.place(x=400,y=100,width=950,height=595)

        # This frame further divided into two sub section 1st- Basic Info (contain the basic information of the hospital) and 2nd- Today's Info (Holds the number of staffs and beds available today )

        # All the information shown in this section is managed by the function update_basic_info() and update_today_info()

        # ------------------- Basic Info -------------------
        basic_info=LabelFrame(right_frame,text="Basic Informations",font=("Cooper Std Black",9),bd=2,relief=RIDGE,bg="#e5e5e5",padx=10,pady=15)
        basic_info.place(x=60,y=20,width=400,height=300)

        self.total_beds= Label(basic_info,text="No. of Total Beds: \t--",font=("arial",10),bg="#e5e5e5")
        self.total_beds.grid(row=0,column=0,sticky=W)
        self.gen_bed = Label(basic_info,text="No. of Beds(Gen) : --",font=("arial",10),bg="#e5e5e5")
        self.gen_bed.grid(row=1,column=0,sticky=W)
        self.icu_bed = Label(basic_info,text="No. of Beds(ICU) : \t--",font=("arial",10),bg="#e5e5e5")
        self.icu_bed.grid(row=2,column=0,sticky=W)
        self.ot_bed = Label(basic_info,text="No. of Beds(OT) : \t--",font=("arial",10),bg="#e5e5e5")
        self.ot_bed.grid(row=3,column=0,sticky=W)
        Label(basic_info,text="",font=("arial",10),bg="#e5e5e5").grid(row=4,column=0,sticky=W)
        self.total_staff = Label(basic_info,text="No. of Total Staff : \t--",font=("arial",10),bg="#e5e5e5")
        self.total_staff.grid(row=5,column=0,sticky=W)
        self.doc = Label(basic_info,text="No. of Doctors : \t--",font=("arial",10),bg="#e5e5e5")
        self.doc.grid(row=6,column=0,sticky=W)
        self.nurse = Label(basic_info,text="No. of Nurses : \t--",font=("arial",10),bg="#e5e5e5")
        self.nurse.grid(row=7,column=0,sticky=W)

        # -------------------- Today's Info -------------------------
        today_info=LabelFrame(right_frame,text="Today's Informations",font=("Cooper Std Black",9),bd=2,relief=RIDGE,bg="#e5e5e5",padx=10,pady=15)
        today_info.place(x=490,y=20,width=400,height=300)

        self.total_beds_avl= Label(today_info,text="No. of total available Beds : \t--",font=("arial",10),bg="#e5e5e5")
        self.total_beds_avl.grid(row=0,column=0,sticky=W)
        self.gen_bed_avl = Label(today_info,text="No. of available Beds(Gen) :  --",font=("arial",10),bg="#e5e5e5")
        self.gen_bed_avl.grid(row=1,column=0,sticky=W)
        self.icu_bed_avl = Label(today_info,text="No. of available Beds(ICU) : \t--",font=("arial",10),bg="#e5e5e5")
        self.icu_bed_avl.grid(row=2,column=0,sticky=W)
        self.ot_bed_avl = Label(today_info,text="No. of available Beds(OT) : \t--",font=("arial",10),bg="#e5e5e5")
        self.ot_bed_avl.grid(row=3,column=0,sticky=W)
        Label(today_info,text="",font=("arial",10),bg="#e5e5e5").grid(row=4,column=0,sticky=W)
        self.total_staff_avl = Label(today_info,text="No. of total available Staff : \t--",font=("arial",10),bg="#e5e5e5")
        self.total_staff_avl.grid(row=5,column=0,sticky=W)
        self.doc_avl = Label(today_info,text="No. of available Doctors : \t--",font=("arial",10),bg="#e5e5e5")
        self.doc_avl.grid(row=6,column=0,sticky=W)
        self.nurse_avl = Label(today_info,text="No. of available Nurses : \t--",font=("arial",10),bg="#e5e5e5")
        self.nurse_avl.grid(row=7,column=0,sticky=W)

        # ------------------------------------------------------- 

        # Check the database empty or not.
        # If empty open a new window to crate the first admin by using the function first_admin()

        chk_null=True # Used to control the checking block. We just need to activate the check block once when the app start and then the block diactivated by using this varible

        if(chk_null):
            con=sqlite3.connect(database="./hms1.db")
            cur=con.cursor()
            try:
                cur.execute("select COUNT(id) from employees")
                tmp,= cur.fetchone()

                # In the employees table of the databse the first row is reserved hence the variable tmp should contain atleast two rows if it has any previously created admin

                if(tmp<2):
                    messagebox.showinfo("Admin Not Created","Create one Admin First to explore other features")
                    self.first_admin()

            except Exception as exp:
                messagebox.showerror("Error-01",f"Error due to {str(exp)}",parent=self.root)
            con.close()
            chk_null=False #deactivate the block

        #------------------------------------------------------
        
        #  call the functions to update the infomations
        self.update_today_info()
        self.update_basic_info()

    def update_date_time(self):
        ''' Update the date and the clock according to the time of system.'''

        time_= time.strftime("%I:%M:%S %p")
        date_= time.strftime("%d-%m-%Y")
        self.sub_title.config(text=f"Welcome to {self.hname} \t\t Date: {date_} \t\t Time: {time_}")
        self.sub_title.after(1000,self.update_date_time) # continuously invoke the fnction after a second

    def update_basic_info(self):
        ''' Update the Basic Info section with the information getting from the database'''

        con=sqlite3.connect(database="./hms1.db")
        cur=con.cursor()

        try:
            cur.execute("select COUNT(id) from bed")
            tmp,= cur.fetchone()
            self.total_beds.config(text=f"No. of Total Beds: \t{tmp}")

            cur.execute("select COUNT(id) from bed where category='General'")
            tmp,= cur.fetchone()
            self.gen_bed.config(text=f"No. of Beds(Gen) : {tmp}")

            cur.execute("select COUNT(id) from bed where category='ICU'")
            tmp,= cur.fetchone()
            self.icu_bed.config(text=f"No. of Beds(ICU) : \t{tmp}")

            cur.execute("select COUNT(id) from bed where category='OT'")
            tmp,= cur.fetchone()
            self.ot_bed.config(text=f"No. of Beds(OT) : \t{tmp}")

            cur.execute("select COUNT(id) from employees")
            tmp,= cur.fetchone()
            self.total_staff.config(text=f"No. of Total Staff : \t{tmp-1}")

            cur.execute("select COUNT(id) from employees where profession='Doctor'")
            tmp,= cur.fetchone()
            self.doc.config(text=f"No. of Doctors : \t{tmp}")

            cur.execute("select COUNT(id) from employees where profession='Nurse'")
            tmp,= cur.fetchone()
            self.nurse.config(text=f"No. of Nurses : \t{tmp}")
            self.total_beds.after((100*60*5),self.update_basic_info)

        except Exception as exp:
            messagebox.showerror("Error-02",f"Error due to {str(exp)}",parent=self.root)
        con.close()

    def update_today_info(self):
        ''' Update the Today's Info section with the information getting from the database'''

        con=sqlite3.connect(database="./hms1.db")
        cur=con.cursor()

        try:
            cur.execute("select COUNT(id) from bed where pid is null")
            tmp,= cur.fetchone()
            self.total_beds_avl.config(text=f"No. of total availabel Beds: \t{tmp}")

            cur.execute("select COUNT(id) from bed where category='General' and pid is null")
            tmp,= cur.fetchone()
            self.gen_bed_avl.config(text=f"No. of availabel Beds(Gen) :  {tmp}")

            cur.execute("select COUNT(id) from bed where category='ICU' and pid is null")
            tmp,= cur.fetchone()
            self.icu_bed_avl.config(text=f"No. of availabel Beds(ICU) : \t{tmp}")

            cur.execute("select COUNT(id) from bed where category='OT' and pid is null")
            tmp,= cur.fetchone()
            self.ot_bed_avl.config(text=f"No. of availabel Beds(OT) : \t{tmp}")

            cur.execute("select COUNT(id) from employees")
            tmp,= cur.fetchone()
            self.total_staff_avl.config(text=f"No. of total availabel Staff : \t{tmp-1}")

            cur.execute("select COUNT(id) from employees where profession='Doctor'")
            tmp,= cur.fetchone()
            self.doc_avl.config(text=f"No. of availabel Doctors : \t{tmp}")

            cur.execute("select COUNT(id) from employees where profession='Nurse'")
            tmp,= cur.fetchone()
            self.nurse_avl.config(text=f"No. of availabel Nurses : \t{tmp}")
            self.total_beds_avl.after((100*60*5),self.update_today_info)

        except Exception as exp:
            messagebox.showerror("Error-03",f"Error due to {str(exp)}",parent=self.root)
        con.close() 

    def first_admin(self):
        ''' Create a new window to add the first admin to the dabase'''

        # import the Create_Admin class
        from first_admin import Create_Admin
        self.new_win=Toplevel(self.root)
        self.new_obj=Create_Admin(self.new_win,self.root) 

    def login_window(self,prof):
        ''' Open a login window for authorization'''

        # import the Login class
        from log_in import Login
        self.new_win=Toplevel(self.root)
        self.new_obj=Login(self.new_win,self.hname,self.root,prof)

       
# Main function
if __name__=='__main__':
    root=Tk()
    obj=HMS(root,"Hopeview Medical Center")   # Create the object of dashboard class HMS
    root.mainloop()