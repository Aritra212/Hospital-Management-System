# =============================================================
#   Project Title: Hospital Management System
#   Page Description: Administration Page
#   Author: Aritra Paul
#   Date: 19/04/2024
# ==============================================================

# Import necessary modules
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import time
import sqlite3
from reusable_function import id_generator,find_col_vals

# Create the class that enclosed the features of Administration page of the HMS system

class Admin:
    def __init__(self,root,hname="Hospital Management System",parent=None,row=None):

        '''The constructor accept 4 arguments 1st- root name ,2nd- name of the hospital, 3rd- parent window reference, 4th- employee data who logged in.'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        self.parent=parent
        
        # Window configurations
        self.root.title("Administration - {}".format(self.hname)) # set the title
        self.root.geometry("1250x650+150+100") # Set the window width, height and position
        self.root.wm_iconbitmap("../images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature
        self.root.focus_force()

        # Handle the exit event
        if self.parent!=None:
            self.root.protocol("WM_DELETE_WINDOW",self.onclosing)

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

        ### ================ Administration ==================

        # Create global tupples for dropdown menus
        self.profession_types= ('HR','Admin','Official Staff','Accountant','Receptinist','Doctor','other')
        self.search_emp_types =('id','name','profession','department','post')
        self.bed_types= ('ICU','OT','General','Emergency')

        # Now the entire window is divided into 4 frames; 2 frames set at the leftmost portion (1at- For Admin Profile, 2nd- For Buttons), 1 frame at the center (3rd- To Handle Inputs) and 1 frame at the extreme right (4th- To Display Outputs).

        ## ================ Admin Profile Frame ====================

        profile_frame= LabelFrame(self.root,text="Admin Profile",font=("arial",12),bd=4,relief=RIDGE)
        profile_frame.place(x=10,y=103,width=400,height=200)
        self.profile_details(profile_frame,row)


        ## =============== Button Container Frame ==================
        btn_frame=Frame(self.root,bg="#e5e5e5")
        btn_frame.place(x=10,y=310,width=400)

        # --------------- Set the Buttons -------------------------
        # Add Employee Button
        add_btn=Button(btn_frame,text="Add Employee",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_employee)
        add_btn.pack(fill=X,pady=10)

        #Search Employee Button
        search_btn=Button(btn_frame,text="Search Employee",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command= self.search_employee)
        search_btn.pack(fill=X,pady=10)

        #Add Department/Beds Button
        add_depts_beds_btn=Button(btn_frame,text="Add Department / Beds",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_dept_beds)
        add_depts_beds_btn.pack(fill=X,pady=10)

        #View or Update Department/Beds Button
        search_dept_btn=Button(btn_frame,text="View Department / Beds",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.search_dept_bed)
        search_dept_btn.pack(fill=X,pady=10)

        ## ================ Input window Frame ====================
        self.input_frame= Frame(self.root,bd=4,relief=RIDGE,padx=10,pady=10)
        self.input_frame.place(x=420,y=110,width=400,height=520)
        
        # default
        self.search_employee()

        ## ================ Output window Frame ====================
        self.output_frame= Frame(self.root,bd=4,relief=RIDGE,padx=10,pady=10)
        self.output_frame.place(x=830,y=110,width=400,height=520)
        Label(self.output_frame,text="No data to show on output window!!",font=("arial blak",13),fg="#979dac",pady=20).pack(side=TOP,anchor=W)

    # Common Functions ----------------------------------------------------

    def profile_details(self,frame,details):

        ''' Add elements into the profile frame'''

        # set profile image
        profile_img=Label(frame,image=None,padx=10)
        profile_img.place(x=5,y=0)
        gender= details[4] if details!=None else None
        self.img_src_sel(gender,profile_img) # select the image according to the gender

        # Logout btn
        logout_btn= Button(frame,text="Logout",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",10),pady=15,cursor="hand2",command=self.onclosing)
        logout_btn.place(x=10,y=140,height=30,width=120)

        # Include other details
        profile_info_frame= Frame(frame,padx=10,pady=10)
        profile_info_frame.place(x=155,y=10,width=240,height=160)

        # If employee data not available
        if details==None:
            Label(profile_info_frame,text="....",font=("arial",13)).grid(row=0,sticky=W)
            Label(profile_info_frame,text="Eid-...",font=("arial",13)).grid(row=1,sticky=W)
            Label(profile_info_frame,text="ph no-...",font=("arial",13)).grid(row=2,sticky=W)
            Label(profile_info_frame,text="email-...",font=("arial",13)).grid(row=3,sticky=W)
            Label(profile_info_frame,text="department-...",font=("arial",13)).grid(row=4,sticky=W)
        #otherwise
        else:
            Label(profile_info_frame,text=f"{details[1]}",font=("arial",13)).grid(row=0,sticky=W)
            Label(profile_info_frame,text=f"Eid- {details[0]}",font=("arial",13)).grid(row=1,sticky=W)
            Label(profile_info_frame,text=f"ph no- {details[10]}",font=("arial",13)).grid(row=2,sticky=W)
            Label(profile_info_frame,text=f"email- {details[11]}",font=("arial",13)).grid(row=3,sticky=W)
            Label(profile_info_frame,text=f"department- {details[7]}",font=("arial",13)).grid(row=4,sticky=W)

    def img_src_sel(self,gen,lb_name):

        ''' Set the image according to the gender. Take two arguments 1st- gender type (eg. male, female) and 2nd- label reference where the image should place'''

        if gen!=None and gen=='female':
            img_src= "../images/doc_img_f.jpg"
        else:
            img_src= "../images/doc_img_m.jpg"

        img=Image.open(img_src)
        img= img.resize((130,130))
        img=ImageTk.PhotoImage(img)
        lb_name.configure(image=img)
        lb_name.image=img

    def update_date_time(self):
        ''' Update the date and the clock according to the time of system.'''

        time_= time.strftime("%I:%M:%S %p")
        date_= time.strftime("%d-%m-%Y")
        self.sub_title.config(text=f"Welcome to {self.hname} \t\t Date: {date_} \t\t Time: {time_}")
        self.sub_title.after(1000,self.update_date_time) # continuously invoke the fnction after a second

    def onclosing(self):
        ''' Set the actions to perform before exit'''
        self.root.destroy()
        self.parent.deiconify()

    def clear_fields(self,values,addr=''):

        '''Used to clear input fields. Take two arguments 1st- A list of values to be cleared, 2nd- address text.
        
        address text treated separately becuase Text has no method set(), we need to use delete() method to remove the text'''
        
        for value in values:
           if value!='': value.set('') 
        if addr!='':
            addr.delete('1.0',END)

    def clear_frame(self,frame,shownull=False):

        ''' Destroy the frame elemetns '''

        for widgets in frame.winfo_children():
            widgets.destroy()
        frame.pack_forget()

        # if shownull true print the statement
        if shownull:
            Label(frame,text="No data to show....",font=("arial blak",13),fg="#979dac",pady=20).pack(side=TOP,anchor=W)

    def update_combo(self,var,combo,types):

        '''Update a combobox. Take 3 arguments 1st- reference of the text variable, 2nd- reference to the combobox and 3rd- values to be included'''

        var.set("")
        combo.configure(values=types)
        combo.current(0)

    def delete_data(self,id,tablename=None,searchtable=None):
        
        ''' Delete Employee/Department/Bed details from the database. Take 3 arguments 1st- ID to find the Employee/Bed/Dept to be deleted, 2nd- name of the table where the data is, 3rd- search table reference if multiple search results found '''

        # Confirmation message
        result= messagebox.askquestion("Are You Sure?","To delete data of the {} click 'yes' button".format(tablename),parent=self.root)

        # if clicked 'yes' by the user then delete the employee
        if result=='yes':
            con=sqlite3.connect(database="./hms1.db")
            cur=con.cursor()
            try:
                cur.execute("delete from {} where id=?".format(tablename),(id,))
                con.commit()

                # Clear the output frame
                self.clear_frame(self.output_frame,True)

                # Handle search table
                if searchtable!=None:
                    selected_itm= searchtable.focus()
                    searchtable.delete(selected_itm)

                messagebox.showinfo("Sucess!!","{} data deleted sucessfully...".format(tablename),parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-20",f"Error due to {str(exp)}",parent=self.root)
            con.close()

    # Functions that manage employees ------------------------------------

    def add_employee(self):

        ''' Manage the Input Frame elements for Add Employee event form '''

        # -------------- local variables --------------------
        name_var= StringVar()
        guardian_name_var= StringVar()
        dob_var= StringVar()
        gender_var= StringVar()
        jdate_var= StringVar()
        profession_var= StringVar()
        department_var= StringVar()
        post_var= StringVar()
        salary_var= StringVar()
        contact_var= StringVar()
        email_var= StringVar()
        password_var= StringVar()

        # create a list of the variables to share wiht other functions easily
        val_list=[name_var,guardian_name_var,dob_var,gender_var,jdate_var,profession_var,department_var,post_var,salary_var,contact_var,email_var,password_var]

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        # Find all departments
        all_depts,err= find_col_vals('name','department')
        if err!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)

        ### =============== Add Employee Form ===================

        Label(self.input_frame,text="Add Employee ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw')

        # To make the frame scrollable we need to use canvas becuse we can't make a frame scrollable in TK but canvas can have the scrollable property and we can also add a frame within a canvas.

        # So the logic is - First make a frame("canvas_container") within the root to contain the canvas("mycanvas"). Then create a canvas("mycanvas") within the frame "canvas_container" and make it scrollable afterthat create another frame named 'scrollable_frame1' within the cavas("mycanvas").

        canvas_container= Frame(self.input_frame)  # Create the first frame
        canvas_container.pack(side=LEFT,anchor='nw')

        mycanvas= Canvas(canvas_container,width=343,height=450) # Create the canvas within the first frame
        mycanvas.pack(side=LEFT,pady=10)

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
        profession_combo=ttk.Combobox(scrollable_frame1,textvariable=profession_var,font=("arial",12),state='readonly',width=18)
        profession_combo['values']=self.profession_types
        profession_combo.grid(row=7,column=1,padx=5,pady=6)

        department_label=Label(scrollable_frame1,text="Select Department*",font=("arial",10,'bold'))
        department_label.grid(row=8,column=0,pady=6,sticky=W)
        department_combo=ttk.Combobox(scrollable_frame1,textvariable=department_var,font=("arial",12),state='readonly',width=18)
        department_combo['values']=all_depts
        department_combo.grid(row=8,column=1,padx=5,pady=6)
        
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

        save_btn= Button(scrollable_frame1,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.save_emp(val_list,address_text))
        save_btn.grid(row=15,column=1,padx=20,pady=10,sticky=E)

    def save_emp(self,values,addr):

        '''Used to add employee to the database. Take two arguments 1st- A list of values to be used, 2nd- address text.
        
        address text treated separately becuase Text has different syntax'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        # add address to the list
        val_list.insert(11,addr.get("1.0",END).strip())

        # remember the order of the values in the list here it is as follows-
        # val_list=[name,guardian name,dob, gender,joining date,profession,department,post,salary,contact,email,address,password]

        try:

            # Check the '*' marked fields is empty or not
            if val_list[0]=="" or val_list[1]=="" or val_list[2]=="" or val_list[6]=="" or val_list[9]=="" or val_list[10]=="" or val_list[12]=="":
                messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
            else:
                con=sqlite3.connect(database="./hms1.db")
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
                        messagebox.showerror("Error-09",f"Error due to {str(err)}",parent=self.root)
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
                            val_list[11],
                            val_list[12]
                        ))
                        con.commit()
                        con.close()

                        # Update val_list according to display() function
                        display_list_items=list(val_list)
                        display_list_items.insert(0,n_id)
                        # print(display_list_items)

                        self.display_emp_details(n_id,display_list_items)

                        messagebox.showinfo("Sucess!!","employee {}(id: {}) added to database sucessfully...".format(val_list[0],n_id),parent=self.root)

        except Exception as exp:
            messagebox.showerror("Error-10",f"Error due to {str(exp)}",parent=self.root)

    def search_employee(self):

        ''' Manage the Input Frame elements for Search Employee event form '''

        # -------------- local variables --------------------
        search_txt= StringVar()
        search_by_var= StringVar()

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        
        ### =============== Search Employee Form ===================

        Label(self.input_frame,text="Search Employee ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)

        search_lable=Label(self.input_frame,text="Search By:",font=("arial",10,'bold'))
        search_lable.grid(row=1,column=0,pady=6,sticky=W)
        search_combo=ttk.Combobox(self.input_frame,font=("arial",12),state='readonly',width=18,textvariable=search_by_var,cursor='hand2')
        search_combo['values']=self.search_emp_types
        search_combo.grid(row=1,column=1,pady=6)
        search_combo.current(0)

        search_value_lable=Label(self.input_frame,text="Enter Value:",font=("arial",10,'bold'))
        search_value_lable.grid(row=2,column=0,pady=6,sticky=W)
        search_value_entry=Entry(self.input_frame,font=("arial",12),textvariable=search_txt)
        search_value_entry.grid(row=2,column=1,padx=10,pady=6)

        # Create a frame to show multiple searh results
        subinput_frame= Frame(self.input_frame)
        subinput_frame.grid(row=4,column=0,columnspan=3)

        # Search Button
        search_btn= Button(self.input_frame,text="Serach",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.search_emp_data([search_by_var.get(),search_txt.get()],subinput_frame))
        search_btn.grid(row=3,column=1,padx=10,pady=10,sticky=E)

    def search_emp_data(self,values,frame):

        '''Used to search employee from the database. Take two arguments 1st- A list of values (search type and search text), 2nd- A frame to diplay the table if multiple values found.'''

        # Clear the frame elements
        self.clear_frame(frame)

        # check for empty field
        if values[0]=="" or values[1]=="":
            messagebox.showerror("Searching failure!!","Please enter some value in searchbox...",parent=self.root)
        else:

            try:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from employees where "+values[0]+" like '%"+values[1]+"%'")
                data=cur.fetchall() 
                con.close()
            except Exception as exp:
                messagebox.showerror("Error-11",f"Error due to {str(exp)}",parent=self.root)

            # if Data found
            if len(data)!=0:  

                eid='-1' # Need to manage display function properly

                # if variable data has only one element or employee then call the display function directly.
                if len(data)==1:
                    eid=data[0][0]
                    self.display_emp_details(eid,data[0])

                # Otherwise create a table to show multiple data  
                else:
                    Label(frame, text="-------------------------------------------------------------------------------------------",font=("arial blak",10),fg="#979dac").grid(row=4,sticky=W,columnspan = 2)

                    # Create a frame and show the table of data within that
                    multi_res_frame= Frame(frame,padx=10,pady=10,width=370)
                    multi_res_frame.grid(row=5,columnspan = 2,sticky=W)
                    
                    # Table theme/style configarations
                    style = ttk.Style()
                    style.theme_use("clam")
                    style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)
                    
                    # Add Vertical scrollbar
                    scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
                    scroll_y.pack(side=RIGHT,fill=Y)

                    # Table configarations 
                    search_table=ttk.Treeview(multi_res_frame,columns=('eid','name','dob','mobile'),yscrollcommand=scroll_y.set)
                    search_table.pack(fill=BOTH,expand=1)

                    # Attached the scrollber with the table
                    scroll_y.config(command=search_table.yview)

                    # Set the table Headings and width of the columns
                    search_table.heading('eid',text='Eid')
                    search_table.heading('name',text="Employee Name")
                    search_table.heading('dob',text='D.O.B')
                    search_table.heading('mobile',text='Mobile No.')
                    search_table['show']='headings'
                    search_table.column('eid',width=50,anchor=CENTER)
                    search_table.column('name',width=110,anchor=CENTER)
                    search_table.column('dob',width=70,anchor=CENTER)
                    search_table.column('mobile',width=100,anchor=CENTER)
                    
                    # Add event when user click on a row from the table
                    search_table.bind("<ButtonRelease-1>",lambda event: self.display_emp_details(eid,tablename=search_table))

                    # Set Table values
                    for row in data:
                        if row[1]!=None: # used to pop the reserve row (1st row of the employee table)
                            search_table.insert('',END,values=[row[0],row[1],row[3],row[10]])

                    messagebox.showinfo("Multiple Records!!","Multiple records found select one to continue...",parent=self.root)
            else:
                messagebox.showerror("Error","Data not found in database...",parent=self.root)

    def upadate_employee(self,values):

        ''' Manage the Input Frame elements for Update Employee event form '''

        # -------------- local variables --------------------
        id_var= StringVar(value=values[0])
        name_var= StringVar(value=values[1])
        guardian_name_var= StringVar(value=values[2])
        dob_var= StringVar(value=values[3])
        gender_var= StringVar(value=values[4])
        jdate_var= StringVar(value=values[5])
        profession_var= StringVar(value=values[6])
        department_var= StringVar(value=values[7])
        post_var= StringVar(value=values[8])
        salary_var= StringVar(value=values[9])
        contact_var= StringVar(value=values[10])
        email_var= StringVar(value=values[11])
        password_var= StringVar(value=values[13])

        address_var=values[12].strip()

        # create a list of the variables to share wiht other functions easily
        val_list=[id_var,name_var,guardian_name_var,dob_var,gender_var,jdate_var,profession_var,department_var,post_var,salary_var,contact_var,email_var,password_var]

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        # Find all departments
        all_depts,err= find_col_vals('name','department')
        if err!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)

        ### =============== Update Employee Form ===================

        Label(self.input_frame,text="Update Employee ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw')

        # To make the frame scrollable we need to use canvas becuse we can't make a frame scrollable in TK but canvas can have the scrollable property and we can also add a frame within a canvas.

        # So the logic is - First make a frame("canvas_container") within the root to contain the canvas("mycanvas"). Then create a canvas("mycanvas") within the frame "canvas_container" and make it scrollable afterthat create another frame named 'scrollable_frame1' within the cavas("mycanvas").

        canvas_container= Frame(self.input_frame)  # Create the first frame
        canvas_container.pack(side=LEFT,anchor='nw')

        mycanvas= Canvas(canvas_container,width=343,height=450) # Create the canvas within the first frame
        mycanvas.pack(side=LEFT,pady=10)

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
        id_label=Label(scrollable_frame1,text="Employee Id",font=("arial",10,'bold'))
        id_label.grid(row=1,column=0,pady=6,sticky=W)
        id_entry=Entry(scrollable_frame1,textvariable=id_var,font=("arial",12),state='readonly')
        id_entry.grid(row=1,column=1,padx=5,pady=6)

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

        jdate_label=Label(scrollable_frame1,text="Joining Date",font=("arial",10,'bold'))
        jdate_label.grid(row=6,column=0,pady=6,sticky=W)
        jdate_entry=Entry(scrollable_frame1,textvariable=jdate_var,font=("arial",12))
        jdate_entry.grid(row=6,column=1,padx=5,pady=6)

        profession_label=Label(scrollable_frame1,text="Profession",font=("arial",10,'bold'))
        profession_label.grid(row=7,column=0,pady=6,sticky=W)
        profession_combo=ttk.Combobox(scrollable_frame1,textvariable=profession_var,font=("arial",12),state='readonly',width=18)
        profession_combo['values']=self.profession_types
        profession_combo.grid(row=7,column=1,padx=5,pady=6)

        department_label=Label(scrollable_frame1,text="Select Department*",font=("arial",10,'bold'))
        department_label.grid(row=8,column=0,pady=6,sticky=W)
        department_combo=ttk.Combobox(scrollable_frame1,textvariable=department_var,font=("arial",12),state='readonly',width=18)
        department_combo['values']=all_depts
        department_combo.grid(row=8,column=1,padx=5,pady=6)
        
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
        address_text.grid(row=13,column=1,padx=10,pady=6)
        address_text.insert(END,address_var)

        password_label=Label(scrollable_frame1,text="Password*",font=("arial",10,'bold'))
        password_label.grid(row=14,column=0,pady=6,sticky=W)
        password_entry=Entry(scrollable_frame1,textvariable=password_var,font=("arial",12))
        password_entry.grid(row=14,column=1,padx=5,pady=6)

        cancel_btn= Button(scrollable_frame1,text="Cacel",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields(val_list,address_text))
        cancel_btn.grid(row=15,column=0,padx=5,pady=10,sticky=W)

        update_btn= Button(scrollable_frame1,text="Update Data",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.update_emp_data(val_list,address_text))
        update_btn.grid(row=15,column=1,padx=5,pady=10,sticky=E)

    def update_emp_data(self,values,addr):

        '''Used to Update employee details to the database. Take two arguments 1st- A list of values to be cleared, 2nd- address text.
        
        address text treated separately becuase Text has different syntax'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        # add address to the list
        val_list.insert(12,addr.get("1.0",END).strip())

        # remember the order of the values in the list here it is as follows-
        # val_list=[id,name,guardian name,dob, gender,joining date,profession,department,post,salary,contact,email,address,password]

        
        try:
            # Check the id field is empty or not
            if val_list[0]=="":
                messagebox.showerror("Error","Id field data removed!! Try again, click the 'Update' button from the search result",parent=self.root)

            # Check the '*' marked fields is empty or not
            elif val_list[1]=="" or val_list[2]=="" or val_list[3]=="" or val_list[7]=="" or val_list[10]=="" or val_list[11]=="" or val_list[13]=="":
                messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
            else:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()

                # Update the database
                cur.execute("update employees set name=?,guardian_name=?,dob=?,gender=?,joining_date=?,profession=?,department=?,post=?,salary=?,mobile=?,email=?,address=?, password=? where id=?",((*val_list[1:],val_list[0])))

                con.commit()
                con.close()

                # display updated data
                self.display_emp_details(val_list[0],val_list)

                #clear input fields
                self.clear_fields(values,addr)

                messagebox.showinfo("Sucess!!","employee data updated sucessfully...",parent=self.root)
        except Exception as exp:
            messagebox.showerror("Error-12",f"Error due to {str(exp)}",parent=self.root)

    def display_emp_details(self,eid,values=None,tablename=None):

        ''' Take 3 arguments 1st- employee id, 2nd- employee details, 3rd- search table reference and display Employee details into the Output frame '''

        # To manage the function call from search action
        if eid=='-1':
            # for handling multiple values in searh table
            tmp=tablename.focus()
            tmp=tablename.item(tmp)['values']
            eid=tmp[0]

            try:
                # find the employee details to be displayed
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from employees where id=?",(eid,))
                values=cur.fetchone()
                con.commit()
                con.close()

            except Exception as exp:
                messagebox.showerror("Error-13",f"Error due to {str(exp)}",parent=self.root)

        ### ================ Display Employee Data ====================

        # Clear the Output frame
        self.clear_frame(self.output_frame)

        # Display data ------------------------------------------

        Label(self.output_frame,text="Employee Details ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw')

        canvas_container= Frame(self.output_frame)
        canvas_container.pack(side=LEFT,anchor='nw')
        mycanvas= Canvas(canvas_container,width=350,height=465)
        mycanvas.pack(side=LEFT,pady=10)

        y_scrollbar=Scrollbar(canvas_container, orient='vertical')
        y_scrollbar.pack(side=RIGHT, fill=Y)
        y_scrollbar.config(command=mycanvas.yview)

        mycanvas.configure(yscrollcommand=y_scrollbar.set)
        mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
        scrollable_frame1= Frame(mycanvas)
        mycanvas.create_window((0,0),window=scrollable_frame1,anchor='nw')
        
        emp_img_label=Label(scrollable_frame1,image=None)
        emp_img_label.grid(row=2,column=2,padx=6,pady=6,sticky=E,rowspan=4,columnspan=2)
        self.img_src_sel(values[4],emp_img_label)

        name_label=Label(scrollable_frame1,text=f"Employee Name :  {values[1]}",font=("arial",10,'bold'))
        name_label.grid(row=0,column=0,pady=6,sticky=W,columnspan=4)

        guardian_label=Label(scrollable_frame1,text=f"Guardian's Name :  {values[2]}",font=("arial",10,'bold'))
        guardian_label.grid(row=1,column=0,pady=6,sticky=W,columnspan=4)

        id_label=Label(scrollable_frame1,text=f"Employee Id :  {values[0]}",font=("arial",10,'bold'))
        id_label.grid(row=2,column=0,pady=6,sticky=W,columnspan=2)

        dob_label=Label(scrollable_frame1,text=f"Date Of Barth :  {values[3]}",font=("arial",10,'bold'))
        dob_label.grid(row=3,column=0,pady=6,sticky=W,columnspan=2)

        gender_label=Label(scrollable_frame1,text=f"Gender :  {values[4]}",font=("arial",10,'bold'))
        gender_label.grid(row=4,column=0,pady=6,sticky=W,columnspan=2)

        jdate_label=Label(scrollable_frame1,text=f"Joining Date :  {values[5]}",font=("arial",10,'bold'))
        jdate_label.grid(row=5,column=0,pady=6,sticky=W,columnspan=2)

        profession_label=Label(scrollable_frame1,text=f"Profession :  {values[6]}",font=("arial",10,'bold'))
        profession_label.grid(row=6,column=0,pady=6,sticky=W,columnspan=4)

        dep_label=Label(scrollable_frame1,text=f"Department :  {values[7]}",font=("arial",10,'bold'))
        dep_label.grid(row=7,column=0,pady=6,sticky=W,columnspan=4)

        post_label=Label(scrollable_frame1,text=f"Post :  {values[8]}",font=("arial",10,'bold'))
        post_label.grid(row=8,column=0,pady=6,sticky=W,columnspan=4)

        salary_label=Label(scrollable_frame1,text=f"Salary :  {values[9]}",font=("arial",10,'bold'))
        salary_label.grid(row=9,column=0,pady=6,sticky=W,columnspan=2)

        mobile_label=Label(scrollable_frame1,text=f"Mobile No:  {values[10]}",font=("arial",10,'bold'))
        mobile_label.grid(row=10,column=0,pady=6,sticky=W,columnspan=3)

        email_label=Label(scrollable_frame1,text=f"Email :  {values[11]}",font=("arial",10,'bold'))
        email_label.grid(row=11,column=0,pady=6,sticky=W,columnspan=4)

        address_label=Label(scrollable_frame1,text=f"Address :",font=("arial",10,'bold'))
        address_label.grid(row=12,column=0,pady=6,sticky='nw')
        address_value_label=Label(scrollable_frame1,text=f"{values[12]}",font=("arial",10,'bold'),wraplength=230,justify='left')
        address_value_label.grid(row=12,column=1,sticky=W,columnspan=3)

        clr_btn= Button(scrollable_frame1,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.clear_frame(self.output_frame,True))
        clr_btn.grid(row=15,column=0,padx=3,pady=10,sticky=W)

        update_btn= Button(scrollable_frame1,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.upadate_employee(values))
        update_btn.grid(row=15,column=1,padx=3,pady=10,sticky=W)

        delete_btn= Button(scrollable_frame1,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.delete_data(values[0],"employees",tablename))
        delete_btn.grid(row=15,column=2,padx=3,pady=10,sticky=W)

    # Functions that manage Department and Beds --------------------------

    def add_dept_beds(self):
        
        ''' Manage the Input Frame elements for Add Department/Beds event form '''

        # -------------- local variables --------------------
        dept_name_var= StringVar()
        bed_type_var= StringVar()
        num_bed_var= StringVar() # number of beds

        # Clear the Input frame
        self.clear_frame(self.input_frame)

        # Add Department elemtents
        Label(self.input_frame,text="Add Department",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=3)

        name_label=Label(self.input_frame,text="Name Of The Dept.*",font=("arial",10,'bold'))
        name_label.grid(row=2,column=0,pady=6,sticky=W)
        name_entry=Entry(self.input_frame,textvariable=dept_name_var,font=("arial",12))
        name_entry.grid(row=2,column=1,padx=10,pady=6)

        clear_btn= Button(self.input_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields([dept_name_var]))
        clear_btn.grid(row=3,column=1,padx=20,pady=10,sticky=W)

        save_btn= Button(self.input_frame,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.save_dept_beds([dept_name_var],isBed=False))
        save_btn.grid(row=3,column=1,padx=20,pady=10,sticky=E)

        # Add Bed elements
        Label(self.input_frame,text="Add Beds",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=7,column=0,sticky=W)

        category_label=Label(self.input_frame,text="Select Category*",font=("arial",10,'bold'))
        category_label.grid(row=8,column=0,pady=6,sticky=W)
        category_combo=ttk.Combobox(self.input_frame,textvariable=bed_type_var,font=("arial",12),state='readonly',width=18)
        category_combo['values']=self.bed_types
        category_combo.grid(row=8,column=1,padx=5,pady=6)

        newbeds_label=Label(self.input_frame,text="No. Of New Beds*",font=("arial",10,'bold'))
        newbeds_label.grid(row=9,column=0,pady=6,sticky=W)
        newbeds_entry=Entry(self.input_frame,textvariable=num_bed_var,font=("arial",12))
        newbeds_entry.grid(row=9,column=1,padx=10,pady=6)

        clear_btn= Button(self.input_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields([bed_type_var,num_bed_var]))
        clear_btn.grid(row=12,column=1,padx=20,pady=10,sticky=W)

        save_btn= Button(self.input_frame,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.save_dept_beds([bed_type_var,num_bed_var],isBed=True))
        save_btn.grid(row=12,column=1,padx=20,pady=10,sticky=E)

    def save_dept_beds(self,values,isBed=False):

        '''Used to add Department or Beds to the database. Take two arguments 1st- A list of values to be used, 2nd- a flag to manage department or bed entity separately.'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())
        
        # Add beds 
        if isBed:
            try:
                # Check the '*' marked fields is empty or not
                if val_list[0]=="" or val_list[1]=="":
                    messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
                else:
                    con=sqlite3.connect(database="./hms1.db")
                    cur=con.cursor()

                    # Add beds val_list[1] times
                    for i in range(int(val_list[1])):
                        cur.execute("insert into bed (category) values(?)",(
                            val_list[0],
                        ))

                    con.commit()
                    con.close()

                    self.clear_fields(values)
                    messagebox.showinfo("Sucess!!",f"{val_list[1]} beds of category {val_list[0]} added to database sucessfully...",parent=self.root)

            except Exception as exp:
                messagebox.showerror("Error-15",f"Error due to {str(exp)}",parent=self.root)


        # Add department
        else:
            try:
                # Check the '*' marked fields is empty or not
                if val_list[0]=="":
                    messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
                else:
                    con=sqlite3.connect(database="./hms1.db")
                    cur=con.cursor()

                    # Check the department table to restrict duplicate entry
                    cur.execute("select * from  department where name=?",(val_list[0],))
                    row=cur.fetchone()
                    if row!=None:
                        messagebox.showerror("Error",f"{val_list[0]} is already exist change name to add new Department",parent=self.root)

                    # otherwise add the Department data to the database
                    else:
                        # generate ID for the Admin
                        n_id,err=id_generator('department')
                        if err!='': 
                            messagebox.showerror("Error-09",f"Error due to {str(err)}",parent=self.root)
                        else:
                            cur.execute("insert into department(id,name) values (?,?)",(
                                n_id,
                                val_list[0]
                            ))
                            con.commit()
                            con.close()

                            # Display data
                            self.display_dept_beds(n_id,[n_id,val_list[0]],isBed=False)

                            #clear input fields
                            self.clear_fields(values)

                            messagebox.showinfo("Sucess!!","department  {}( id: {} )added to database sucessfully...".format(val_list[0],n_id),parent=self.root)

            except Exception as exp:
                messagebox.showerror("Error-14",f"Error due to {str(exp)}",parent=self.root)

    def search_dept_bed(self):

        ''' Manage the Input Frame elements for Search department or bed event '''

        # -------------- local variables --------------------
        search_txt= StringVar()
        search_by_var= StringVar()
        ch=IntVar(value=1) # Used to manage department or bed separately

        dept_search_types=("id","name")
        bed_search_types=("category","id")

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        
        ### =============== Search Department or Bed Form ================

        Label(self.input_frame,text="Search Department / Beds ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=3)

        # Select Department or Bed
        radio1= Radiobutton(self.input_frame,text="Department",variable=ch,value=1,command= lambda : self.update_combo(search_by_var,search_combo,dept_search_types),tristatevalue=0)
        radio1.grid(row=1,column=0,pady=6,sticky=W)

        radio2= Radiobutton(self.input_frame,text="Bed",variable=ch,value=2,command= lambda : self.update_combo(search_by_var,search_combo,bed_search_types),tristatevalue=0)
        radio2.grid(row=1,column=1,pady=6,sticky=W)

        search_lable=Label(self.input_frame,text="Search By:",font=("arial",10,'bold'))
        search_lable.grid(row=2,column=0,pady=6,sticky=W)
        search_combo=ttk.Combobox(self.input_frame,font=("arial",12),state='readonly',width=18,textvariable=search_by_var,cursor='hand2')
        search_combo['values']=()
        search_combo.grid(row=2,column=1,pady=6)

        self.update_combo(search_by_var,search_combo,dept_search_types) #default set to department

        search_value_lable=Label(self.input_frame,text="Enter Value:",font=("arial",10,'bold'))
        search_value_lable.grid(row=3,column=0,pady=6,sticky=W)
        search_value_entry=Entry(self.input_frame,font=("arial",12),textvariable=search_txt)
        search_value_entry.grid(row=3,column=1,padx=10,pady=6)
        
        # Search Button
        search_btn= Button(self.input_frame,text="Serach",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda:self.search_dept_bed_data(ch.get(),[search_by_var.get(),search_txt.get()],subinput_frame))
        search_btn.grid(row=4,column=1,padx=10,pady=10,sticky=E)

        # Create a frame to show multiple searh results
        subinput_frame= Frame(self.input_frame)
        subinput_frame.grid(row=6,column=0,columnspan=3)

    def search_dept_bed_data(self,sel,values,frame):

        '''Used to search Department/Beds from the database. Take 3 arguments 1st- a flag variable to separate department and bed, 2nd- A list of values (search type and search text), 3rd- A frame to diplay the table if multiple values found.'''

        # Clear the frame elements
        self.clear_frame(frame)

        # check for empty field
        if values[0]=="" or values[1]=="":
            messagebox.showerror("Searching failure!!","Please enter some value in searchbox...",parent=self.root)

        # For Department
        elif sel==1:
            try:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from department where "+values[0]+" like '%"+values[1]+"%'")
                data=cur.fetchall()
                con.close()
                # if Data found
                if len(data)!=0:    
                    
                    dept_id='-1' # Need to manage display function properly

                    # if variable data has only one element then call the display function directly.
                    if len(data)==1:
                        dept_id=data[0][0]
                        self.display_dept_beds(dept_id,data[0],isBed=False)

                    # Otherwise create a table to show multiple data    
                    else:
                        Label(frame, text="-------------------------------------------------------------------------------------------",font=("arial blak",10),fg="#979dac").grid(row=4,sticky=W,columnspan = 2)

                        # Create a frame and show the table of data within that
                        multi_res_frame= Frame(frame,padx=10,pady=10,width=370)
                        multi_res_frame.grid(row=5,columnspan = 2,sticky=W)
                        
                        # Table theme/style configarations
                        style = ttk.Style()
                        style.theme_use("clam")
                        style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)

                        # Add Vertical scrollbar
                        scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
                        scroll_y.pack(side=RIGHT,fill=Y)

                        # Table configarations 
                        search_table=ttk.Treeview(multi_res_frame,columns=('id','name'),yscrollcommand=scroll_y.set)
                        search_table.pack(fill=BOTH,expand=1)
                        
                        # Attached the scrollber with the table
                        scroll_y.config(command=search_table.yview)

                        # Set the table Headings and width of the columns
                        search_table.heading('id',text='Deptartment id')
                        search_table.heading('name',text="Department Name")
                        search_table['show']='headings'
                        search_table.column('id',width=110,anchor=CENTER)
                        search_table.column('name',width=110,anchor=CENTER)
                        search_table.bind("<ButtonRelease-1>",lambda event: self.display_dept_beds(dept_id,isBed=False,tablename=search_table))

                        # Set Table values
                        for row in data:
                            if row[1]!='None': # used to pop the reserve row (1st row of the department table)
                                search_table.insert('',END,values=[row[0],row[1]])

                        messagebox.showinfo("Multiple Records!!","Multiple records found select one to continue...",parent=self.root)
                else:
                    messagebox.showerror("Error","Data not found in database...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-16",f"Error due to {str(exp)}",parent=self.root)

        # For Bed
        elif sel==2:
            try:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from bed where "+values[0]+" like '%"+values[1]+"%'")
                data=cur.fetchall()
                con.close()

                # if Data found
                if len(data)!=0:    
                    
                    bed_id='-1' # Needed to manage display function properly

                    # if variable data has only one element or employee then call the display function directly.
                    if len(data)==1:
                        bed_id=data[0][0]
                        self.display_dept_beds(bed_id,data[0],isBed=True)

                    # Otherwise create a table to show multiple data 
                    else:
                        Label(frame, text="-------------------------------------------------------------------------------------------",font=("arial blak",10),fg="#979dac").grid(row=4,sticky=W,columnspan = 2)

                        # Create a frame and show the table of data within that
                        multi_res_frame= Frame(frame,padx=10,pady=10,width=370)
                        multi_res_frame.grid(row=5,columnspan = 2,sticky=W)
                        
                        # Table theme/style configarations
                        style = ttk.Style()
                        style.theme_use("clam")
                        style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)

                        # Add Vertical scrollbar
                        scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
                        scroll_y.pack(side=RIGHT,fill=Y)

                        # Table configarations 
                        search_table=ttk.Treeview(multi_res_frame,columns=('id','category','charges','pid'),yscrollcommand=scroll_y.set)
                        search_table.pack(fill=BOTH,expand=1)

                        # Attached the scrollber with the table
                        scroll_y.config(command=search_table.yview)

                        # Set the table Headings and width of the columns
                        search_table.heading('id',text='Bed id')
                        search_table.heading('category',text='Bed Category')
                        search_table.heading('charges',text="Bed Price")
                        search_table.heading('pid',text="Patient ID")
                        search_table['show']='headings'
                        search_table.column('id',width=50,anchor=CENTER)
                        search_table.column('category',width=90,anchor=CENTER)
                        search_table.column('charges',width=90,anchor=CENTER)
                        search_table.column('pid',width=90,anchor=CENTER)

                        # Add event when user click on a row from the table
                        search_table.bind("<ButtonRelease-1>",lambda event: self.display_dept_beds(bed_id,tablename=search_table,isBed=True))

                        # Set Table values
                        for row in data:
                                search_table.insert('',END,values=row)

                        messagebox.showinfo("Multiple Records!!",f"Total {len(data)} number of records found select one to continue...",parent=self.root)
                else:
                    messagebox.showerror("Error","Data not found in database...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-17",f"Error due to {str(exp)}",parent=self.root)

    def update_dept_bed(self,values,isBed=False):

        ''' Manage the Input Frame elements for Update department/bed event form. Take two arguments 1st- a list of values, 2nd- flag variable to manage department and bed separtely'''

        # Clear the Input frame
        self.clear_frame(self.input_frame)

        ##============== Update Department ==================
        if isBed:

            # -------------- local variables --------------------
            id_var= StringVar(value=values[0])
            bed_type_var= StringVar(value=values[1])
            charges_var= StringVar(value=values[2])
            pid_var= StringVar(value=values[3])

            # create a list of the variables to share wiht other functions easily
            val_list=[id_var,bed_type_var,charges_var,pid_var]

            # -------------- Update form ------------------------
            Label(self.input_frame,text="Update Bed Values",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)

            id_label=Label(self.input_frame,text="Bed Id",font=("arial",10,'bold'))
            id_label.grid(row=1,column=0,pady=6,sticky=W)
            id_entry=Entry(self.input_frame,textvariable=id_var,font=("arial",12),state='readonly')
            id_entry.grid(row=1,column=1,padx=10,pady=6)

            category_label=Label(self.input_frame,text="Select Category*",font=("arial",10,'bold'))
            category_label.grid(row=2,column=0,pady=6,sticky=W)
            category_combo=ttk.Combobox(self.input_frame,textvariable=bed_type_var,font=("arial",12),state='readonly',width=18)
            category_combo['values']=self.bed_types
            category_combo.grid(row=2,column=1,padx=5,pady=6)

            cancel_btn= Button(self.input_frame,text="Cacel",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields([id_var,bed_type_var]))
            cancel_btn.grid(row=3,column=1,padx=20,pady=10,sticky=W)

            update_btn= Button(self.input_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.update_dept_bed_data(val_list,isBed=True))
            update_btn.grid(row=3,column=1,padx=20,pady=10,sticky=E)

        ##============== Update Department ==================
        else:

            # -------------- local variables --------------------
            id_var= StringVar(value=values[0])
            dept_name_var= StringVar(value=values[1])

            # -------------- Update form ------------------------
            Label(self.input_frame,text="Update Department ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)

            id_label=Label(self.input_frame,text="Department Id",font=("arial",10,'bold'))
            id_label.grid(row=1,column=0,pady=6,sticky=W)
            id_entry=Entry(self.input_frame,textvariable=id_var,font=("arial",12),state='readonly')
            id_entry.grid(row=1,column=1,padx=10,pady=6)

            name_label=Label(self.input_frame,text="Name Of The Department*",font=("arial",10,'bold'))
            name_label.grid(row=2,column=0,pady=6,sticky=W)
            name_entry=Entry(self.input_frame,textvariable=dept_name_var,font=("arial",12))
            name_entry.grid(row=2,column=1,padx=10,pady=6)

            cancel_btn= Button(self.input_frame,text="Cacel",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields([id_var,dept_name_var]))
            cancel_btn.grid(row=3,column=1,padx=20,pady=10,sticky=W)

            update_btn= Button(self.input_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.update_dept_bed_data([id_var,dept_name_var]))
            update_btn.grid(row=3,column=1,padx=20,pady=10,sticky=E)

    def update_dept_bed_data(self,values,isBed=False):

        '''Used to Update Department/Bed details to the database. Take two arguments 1st- a list of TK values, 2nd- flag variable to manage department and bed separtely '''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        ## ================= Update Bed ======================
        if isBed:
            try:
                # Check for empty fields
                if val_list[0]=="" or val_list[1]=="":
                    messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)

                else:
                    con=sqlite3.connect(database="./hms1.db")
                    cur=con.cursor()

                    # Update the database
                    cur.execute("update bed set category=? where id=?",(val_list[1],val_list[0]))
                    
                    con.commit()
                    con.close()

                    # Display bed data
                    self.display_dept_beds(val_list[0],val_list,isBed=True)
                
                    #clear input fields
                    self.clear_fields(values)

                    messagebox.showinfo("Sucess!!","Bed data updated sucessfully...",parent=self.root)
                    
            except Exception as exp:
                messagebox.showerror("Error-21",f"Error due to {str(exp)}",parent=self.root)                

        ## ================= Update Department ===============
        else:
            try:
                # Check for empty fields
                if val_list[0]=="" or val_list[1]=="":
                    messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
                
                else:
                    con=sqlite3.connect(database="./hms1.db")
                    cur=con.cursor()

                    # Update the database
                    cur.execute("update department set name=? where id=?",(val_list[1],val_list[0]))
                    
                    con.commit()
                    con.close()

                    # Display department data
                    self.display_dept_beds(val_list[0],val_list)
                
                    #clear input fields
                    self.clear_fields(values)

                    messagebox.showinfo("Sucess!!","Department's data updated sucessfully...",parent=self.root)
                    
            except Exception as exp:
                messagebox.showerror("Error-19",f"Error due to {str(exp)}",parent=self.root)

    def display_dept_beds(self,id_,values=None,tablename=None,isBed=False):

        ''' Take 4 arguments 1st- department/bed id, 2nd- values, 3rd- search table reference, 4th- flag to manage dept or bed elements and display the details into the Output frame '''

        # To manage the function call from search action
        if id_=='-1':
            # for handling multiple values in searh table
            tmp=tablename.focus()
            tmp=tablename.item(tmp)['values']
            id_=tmp[0]

            try:
                # find the details to be displayed
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                if isBed:
                    cur.execute("select * from bed where id=?",(id_,))
                else:
                    cur.execute("select * from department where id=?",(id_,))
                values=cur.fetchone()
                con.commit()
                con.close()

            except Exception as exp:
                messagebox.showerror("Error-18",f"Error due to {str(exp)}",parent=self.root)

        # Clear the Output frame
        self.clear_frame(self.output_frame)

        ### ================ Display Department Data ====================
        if not isBed:

            Label(self.output_frame,text="Department Details ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,columnspan=4,sticky=W)

            id_label=Label(self.output_frame,text=f"Department Name :  {values[0]}",font=("arial",10,'bold'))
            id_label.grid(row=1,column=0,pady=6,sticky=W,columnspan=4)

            name_label=Label(self.output_frame,text=f"Department Name :  {values[1]}",font=("arial",10,'bold'))
            name_label.grid(row=2,column=0,pady=6,sticky=W,columnspan=4)

            clr_btn= Button(self.output_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.clear_frame(self.output_frame,True))
            clr_btn.grid(row=3,column=0,padx=3,pady=10,sticky=W)

            update_btn= Button(self.output_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.update_dept_bed(values,isBed=False))
            update_btn.grid(row=3,column=1,padx=3,pady=10,sticky=W)

            delete_btn= Button(self.output_frame,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.delete_data(values[0],"department",tablename))
            delete_btn.grid(row=3,column=2,padx=3,pady=10,sticky=W)

        ### ================ Display Bed Data ====================
        else:

            Label(self.output_frame,text="Bed Details ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,columnspan=4,sticky=W)

            id_label=Label(self.output_frame,text=f"Bed id:  {values[0]}",font=("arial",10,'bold'))
            id_label.grid(row=1,column=0,pady=6,sticky=W,columnspan=4)

            category_label=Label(self.output_frame,text=f"Bed Category :  {values[1]}",font=("arial",10,'bold'))
            category_label.grid(row=2,column=0,pady=6,sticky=W,columnspan=4)

            pid_label=Label(self.output_frame,text=f"Patient ID :  {values[3]}",font=("arial",10,'bold'))
            pid_label.grid(row=3,column=0,pady=6,sticky=W,columnspan=4)

            clr_btn= Button(self.output_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.clear_frame(self.output_frame,True))
            clr_btn.grid(row=4,column=0,padx=3,pady=10,sticky=W)

            update_btn= Button(self.output_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.update_dept_bed(values,isBed=True))
            update_btn.grid(row=4,column=1,padx=3,pady=10,sticky=W)

            delete_btn= Button(self.output_frame,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.delete_data(values[0],"bed",tablename))
            delete_btn.grid(row=4,column=2,padx=3,pady=10,sticky=W)


# Main function
if __name__=='__main__':
    root=Tk()
    obj=Admin(root,"Hopeview Medical Center")   # Create the object of dashboard class HMS
    root.mainloop()



