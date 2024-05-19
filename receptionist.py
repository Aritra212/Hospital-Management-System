# =============================================================
#   Project Title: Hospital Management System
#   Page Description: Receptionist Page
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

# Create the class that enclosed the features of Receptionist page of the HMS system

class RPT:
    def __init__(self,root,hname="Hospital Management System",parent=None,row=None):

        '''The constructor accept 4 arguments 1st- root name ,2nd- name of the hospital, 3rd- parent window reference, 4th- employee data who logged in.'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        self.parent=parent

        # Window configurations
        self.root.title("Reception - {}".format(self.hname)) # set the title
        self.root.geometry("1250x650+150+100") # Set the window width, height and position
        self.root.wm_iconbitmap("./images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature
        self.root.focus_force()

         # Handle the exit event
        if self.parent!=None:
            self.root.protocol("WM_DELETE_WINDOW",self.onclosing)

        ### =============== Title Bar ===================
        self.title_icon=Image.open("./images/hms_logo1.png")
        self.title_icon=self.title_icon.resize((50,50))
        self.title_icon=ImageTk.PhotoImage(self.title_icon)
        title=Label(self.root,text=self.hname, image= self.title_icon,compound=LEFT,font=("arial black",20),bg="#2b2d42",fg="#edf2f4",padx=10)
        title.place(x=0,y=0,relwidth=1,height=70)

        ### ================ Sub Title Bar ================
        self.sub_title=Label(self.root,text="Welcome to {} \t\t Date: DD-MM-YYY \t\t Time: HH:MM:SS".format(self.hname),font=("Cooper Std Black",13,"bold"),bg="#ef233c",fg="#ffffff")
        self.sub_title.place(x=0,y=70,relwidth=1,height=30)

        self.update_date_time() # Handle the date and the clock

        ### ================ Receptionist ==================

        # Create global tupples for dropdown menus
        self.search_patient_types =('id','name','department')
        self.bed_types= ('ICU','OT','General','Emergency')

        # Now the entire window is divided into 4 frames; 2 frames set at the leftmost portion (1at- For Admin Profile, 2nd- For Buttons), 1 frame at the center (3rd- To Handle Inputs) and 1 frame at the extreme right (4th- To Display Outputs).

        
        ## ================ Receptionist Profile Frame ====================

        profile_frame= LabelFrame(self.root,text="Admin Profile",font=("arial",12),bd=4,relief=RIDGE)
        profile_frame.place(x=10,y=103,width=400,height=200)
        self.profile_details(profile_frame,row)

        ## =============== Button Container Frame ==================
        btn_frame=Frame(self.root,bg="#e5e5e5")
        btn_frame.place(x=10,y=310,width=400)

        # --------------- Set the Buttons -------------------------
        # Add Patient Button
        add_btn=Button(btn_frame,text="Admit Patient",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_patient)
        add_btn.pack(fill=X,pady=10)

        #Search Patient Button
        search_btn=Button(btn_frame,text="Search Patient",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command= self.search_patient)
        search_btn.pack(fill=X,pady=10)

        #Update Patient Button
        # update_btn=Button(btn_frame,text="Update Patient",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_dept_beds)
        # update_btn.pack(fill=X,pady=10)

        #Delete Patient Button
        # delete_btn=Button(btn_frame,text="Delete Patient",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.search_dept_bed)
        # delete_btn.pack(fill=X,pady=10)

        ## ================ Input window Frame ====================
        self.input_frame= Frame(self.root,bd=4,relief=RIDGE,padx=10,pady=10)
        self.input_frame.place(x=420,y=110,width=400,height=520)
        
        # default
        self.search_patient()

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
            img_src= "./images/doc_img_f.jpg"
        else:
            img_src= "./images/doc_img_m.jpg"

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
        if(len(types)>=1):
            combo.current(0)

    def find_docs_val(self,comboname,dept,doc_var,doc_dict):

        ''' Find doctor id and names according to the department. Take 4 arguments 1st- combobox refeence, 2nd- name of the department, 3rd- reference to docotor variable and 4th an empty dictionary'''
        doc_dict.clear()
        doc_vals,err= find_col_vals('id, name','employees','department= "{}"'.format(dept))
        if err!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)
        else:
            for doc in doc_vals:
                doc_dict[doc[1]]=doc[0]

        #set the combobox values
        self.update_combo(doc_var,comboname,tuple(doc_dict.keys()))

    def find_bed_val(self,bed_var,ward):
        ''' Find available bed number or id for the patient. Take two arguments 1st- refence to bed_varoable, 2nd- ward type'''

        bed_var.set('')
        value,err= find_col_vals('id','bed','category="{}" and pid is null'.format(ward))

        if err!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)
        elif len(value)<1:
            messagebox.showerror("Error",f"Bed not available for {ward}",parent=self.root)
        else:
            bed_var.set(value[0])
   
    # Functions that manage Patients ------------------------------------
    
    def add_patient(self):

        ''' Manage the Input Frame elements for Add Patient event '''

        # -------------- local variables --------------------
        name_var= StringVar()
        guardian_name_var= StringVar()
        dob_var= StringVar()
        gender_var= StringVar()
        ward_var= StringVar()
        admit_date_var= StringVar()
        department_var= StringVar()
        doctor_var= StringVar()
        bed_no_var= StringVar()
        contact_var= StringVar()
        email_var= StringVar()
        doc_dict= {}

        # create a list of the variables to share wiht other functions easily
        val_list=[name_var,guardian_name_var,dob_var,gender_var,ward_var,admit_date_var,department_var,doctor_var,bed_no_var,contact_var,email_var]

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        # Find all departments
        all_depts,err= find_col_vals('name','department')
        if err!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)

        ### =============== Add Patient Form ===================

        Label(self.input_frame,text="Add Patient ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw')

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
        name_label=Label(scrollable_frame1,text="Patient's Name*",font=("arial",10,'bold'))
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

        ward_label=Label(scrollable_frame1,text="Ward Type",font=("arial",10,'bold'))
        ward_label.grid(row=7,column=0,pady=6,sticky=W)
        ward_combo=ttk.Combobox(scrollable_frame1,textvariable=ward_var,font=("arial",12),state='readonly',width=18)
        ward_combo['values']=self.bed_types
        ward_combo.grid(row=7,column=1,padx=5,pady=6)
        #To find bed number according to the type
        ward_combo.bind("<<ComboboxSelected>>",lambda event:self.find_bed_val(bed_no_var,ward_var.get()))

        # Get the date
        date_=time.strftime("%d-%m-%Y")
        # set the date
        admit_date_var.set(date_)
        admit_date_label=Label(scrollable_frame1,text="Admission Date",font=("arial",10,'bold'))
        admit_date_label.grid(row=6,column=0,pady=6,sticky=W)
        admit_date_entry=Entry(scrollable_frame1,textvariable=admit_date_var,font=("arial",12))
        admit_date_entry.grid(row=6,column=1,padx=5,pady=6)

        department_label=Label(scrollable_frame1,text="Select Department*",font=("arial",10,'bold'))
        department_label.grid(row=8,column=0,pady=6,sticky=W)
        department_combo=ttk.Combobox(scrollable_frame1,textvariable=department_var,font=("arial",12),state='readonly',width=18)
        department_combo['values']=all_depts
        department_combo.grid(row=8,column=1,padx=5,pady=6)
        #To find doctors according to the selected department
        department_combo.bind("<<ComboboxSelected>>",lambda event: self.find_docs_val(doctor_combo,department_var.get(),doctor_var,doc_dict))

        doctor_label=Label(scrollable_frame1,text="Doctor",font=("arial",10,'bold'))
        doctor_label.grid(row=9,column=0,pady=6,sticky=W)
        doctor_combo=ttk.Combobox(scrollable_frame1,textvariable=doctor_var,font=("arial",12),width=18)
        doctor_combo['values']=()
        doctor_combo.grid(row=9,column=1,padx=5,pady=6)
        
        bed_label=Label(scrollable_frame1,text="Bed No.",font=("arial",10,'bold'))
        bed_label.grid(row=10,column=0,pady=6,sticky=W)
        bed_entry=Entry(scrollable_frame1,textvariable=bed_no_var,font=("arial",12))
        bed_entry.grid(row=10,column=1,padx=5,pady=6)

        contact_label=Label(scrollable_frame1,text="Mobile No.*",font=("arial",10,'bold'))
        contact_label.grid(row=11,column=0,pady=6,sticky=W)
        contact_entry=Entry(scrollable_frame1,textvariable=contact_var,font=("arial",12))
        contact_entry.grid(row=11,column=1,padx=5,pady=6)

        email_label=Label(scrollable_frame1,text="Email",font=("arial",10,'bold'))
        email_label.grid(row=12,column=0,pady=6,sticky=W)
        email_entry=Entry(scrollable_frame1,textvariable=email_var,font=("arial",12))
        email_entry.grid(row=12,column=1,padx=5,pady=6)

        address_label=Label(scrollable_frame1,text="Address",font=("arial",10,'bold'))
        address_label.grid(row=13,column=0,pady=7,sticky=W)
        address_text=Text(scrollable_frame1,font=("arial",12),width=20,height=3)
        address_text.grid(row=13,column=1,padx=5,pady=6)

        clear_btn= Button(scrollable_frame1,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields(val_list[:len(val_list)-1],address_text))
        clear_btn.grid(row=15,column=1,padx=20,pady=10,sticky=W)

        save_btn= Button(scrollable_frame1,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.save_patient(val_list,address_text,doc_dict))
        save_btn.grid(row=15,column=1,padx=20,pady=10,sticky=E)

    def save_patient(self,values,addr,doc_dict):

        '''Used to add patient to the database. Take 3 arguments 1st- A list of values to be used, 2nd- address text, 3rd- a dictionary that contain doctor name with id.
        
        address text treated separately becuase Text has different syntax'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        # add address to the list
        val_list.append(addr.get("1.0",END).strip())

        # remember the order of the values in the list here it is as follows-
        # val_list=[name,guardian's name,dob,gender,ward,admit date,department,doctor,bed no,contact,email,address]


        try:
            # Check the '*' marked fields is empty or not
            if val_list[0]=="" or val_list[1]=="" or val_list[2]=="" or val_list[6]=="" or val_list[9]=="":
                messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
            
            elif val_list[8]!='' and val_list[4]=='':
                messagebox.showerror("Error","Bed number privided but Ward not selected",parent=self.root)

            else:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()

                # to Check the patient table to restrict duplicate entry
                cur.execute("select * from  patient where name=? and guardian_name=? and dob=? ",(val_list[0],val_list[1],val_list[2]))
                row=cur.fetchone()

                # to check the bed available or not
                cur.execute("select pid,name from bed, patient where bed.pid=patient.id and bed.id=?",(val_list[8],))
                p_d=cur.fetchone()
                if p_d!=None:
                    pid=p_d[0]
                    pname=p_d[1]
                else:
                    pid=pname=None

                # to match the bed number with the ward
                cur.execute("select category from bed where id=?",(val_list[8],))
                category,=cur.fetchone()

                if row!=None:
                    messagebox.showerror("Error",f"{val_list[0]} is already exist change name or other details to add new patient",parent=self.root)

                elif pid!=None:
                    messagebox.showerror("Error",f"Bed {val_list[8]} is already booked for patient {pid} ( {pname} ) change the number",parent=self.root)

                elif val_list[4] != category and val_list[8]!='':
                    messagebox.showerror("Error",f"Bed {val_list[8]} is allocated for another category ({category}) not for {val_list[4]} or not exists, change the status or bed number",parent=self.root)

                # otherwise add the patient data to the database
                else:
                    # generate ID for the Patient
                    n_id,err=id_generator('patient')
                    if err!='': 
                        messagebox.showerror("Error-09",f"Error due to {str(err)}",parent=self.root)
                    else:
                        cur.execute("insert into patient(id,name,guardian_name,dob,gender,status,admit,department,doctor,mobile,email,address) values (?,?,?,?,?,?,?,?,?,?,?,?)",(
                            n_id,
                            val_list[0],
                            val_list[1],
                            val_list[2],
                            val_list[3],
                            val_list[4],
                            val_list[5],
                            val_list[6],
                            doc_dict[val_list[7]],
                            val_list[9],
                            val_list[10],
                            val_list[11]
                        ))

                        # Upadte the bed table if bed allocated for the patient
                        if val_list[8]!='':
                            cur.execute("update bed set pid=? where id=?",(n_id,val_list[8]))

                        # create a list to call display()
                        cur.execute("select * from patient where id= '{}'".format(n_id))
                        display_list_items=list(cur.fetchone())

                        con.commit()
                        con.close()

                        self.display_patient_details(n_id,display_list_items)

                        messagebox.showinfo("Sucess!!","Patient {}(id: {}) added to database sucessfully...".format(val_list[0],n_id),parent=self.root)

        except Exception as exp:
            messagebox.showerror("Error-26",f"Error due to {str(exp)}",parent=self.root)

    def search_patient(self):

        ''' Manage the Input Frame elements for Search Patient event form '''

        # -------------- local variables --------------------
        search_txt= StringVar()
        search_by_var= StringVar()

        # Clear the Input frame
        self.clear_frame(self.input_frame)
        
        ### =============== Search Employee Form ===================

        Label(self.input_frame,text="Search Patient ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)

        search_lable=Label(self.input_frame,text="Search By:",font=("arial",10,'bold'))
        search_lable.grid(row=1,column=0,pady=6,sticky=W)
        search_combo=ttk.Combobox(self.input_frame,font=("arial",12),state='readonly',width=18,textvariable=search_by_var,cursor='hand2')
        search_combo['values']=self.search_patient_types
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
        search_btn= Button(self.input_frame,text="Serach",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.search_patient_data([search_by_var.get(),search_txt.get()],subinput_frame))
        search_btn.grid(row=3,column=1,padx=10,pady=10,sticky=E)

    def search_patient_data(self,values,frame):

        '''Used to search Patient from the database. Take two arguments 1st- A list of values (search type and search text), 2nd- A frame to diplay the table if multiple values found.'''

        # Clear the frame elements
        self.clear_frame(frame)

        # check for empty field
        if values[0]=="" or values[1]=="":
            messagebox.showerror("Searching failure!!","Please enter some value in searchbox...",parent=self.root)
        else:

            try:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from patient where "+values[0]+" like '%"+values[1]+"%'")
                data=cur.fetchall() 
                con.close()
            except Exception as exp:
                messagebox.showerror("Error-11",f"Error due to {str(exp)}",parent=self.root)

            # if Data found
            if len(data)!=0:  

                pid='-1' # Need to manage display function properly

                # if variable data has only one element or patient then call the display function directly.
                if len(data)==1:
                    pid=data[0][0]
                    self.display_patient_details(pid,data[0])

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
                    search_table=ttk.Treeview(multi_res_frame,columns=('pid','name','dob','mobile'),yscrollcommand=scroll_y.set)
                    search_table.pack(fill=BOTH,expand=1)

                    # Attached the scrollber with the table
                    scroll_y.config(command=search_table.yview)

                    # Set the table Headings and width of the columns
                    search_table.heading('pid',text='Eid')
                    search_table.heading('name',text="Employee Name")
                    search_table.heading('dob',text='D.O.B')
                    search_table.heading('mobile',text='Mobile No.')
                    search_table['show']='headings'
                    search_table.column('pid',width=50,anchor=CENTER)
                    search_table.column('name',width=110,anchor=CENTER)
                    search_table.column('dob',width=70,anchor=CENTER)
                    search_table.column('mobile',width=100,anchor=CENTER)
                    
                    # Add event when user click on a row from the table
                    search_table.bind("<ButtonRelease-1>",lambda event: self.display_patient_details(pid,tablename=search_table))

                    # Set Table values
                    for row in data:
                        if row[1]!=None: # used to pop the reserve row (1st row of the employee table)
                            search_table.insert('',END,values=[row[0],row[1],row[3],row[9]])

                    messagebox.showinfo("Multiple Records!!","Multiple records found select one to continue...",parent=self.root)
            else:
                messagebox.showerror("Error","Data not found in database...",parent=self.root)

    def upadate_patient(self,values):

        ''' Manage the Input Frame elements for Update Employee event form '''
        # print(values)
        # print(len(values))

        # -------------- local variables --------------------
        id_var= StringVar(value=values[0])
        name_var= StringVar(value=values[1])
        guardian_name_var= StringVar(value=values[2])
        dob_var= StringVar(value=values[3])
        gender_var= StringVar(value=values[4])
        ward_var= StringVar(value=values[5])
        admit_date_var= StringVar(value=values[6])
        department_var= StringVar(value=values[7])
        contact_var= StringVar(value=values[9])
        email_var= StringVar(value=values[10])

        
        doctor_var= StringVar(value=values[14])
        bed_no_var= StringVar(value=values[15])
        doc_dict= {values[14]:values[8]}

        # create a list of the variables to share wiht other functions easily
        val_list=[id_var,name_var,guardian_name_var,dob_var,gender_var,ward_var,admit_date_var,department_var,doctor_var,bed_no_var,contact_var,email_var]

        address_var=values[11].strip()

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
        id_label=Label(scrollable_frame1,text="Patient Id",font=("arial",10,'bold'))
        id_label.grid(row=1,column=0,pady=6,sticky=W)
        id_entry=Entry(scrollable_frame1,textvariable=id_var,font=("arial",12),state='readonly')
        id_entry.grid(row=1,column=1,padx=5,pady=6)

        name_label=Label(scrollable_frame1,text="Patient's Name*",font=("arial",10,'bold'))
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

        ward_label=Label(scrollable_frame1,text="Ward Type",font=("arial",10,'bold'))
        ward_label.grid(row=7,column=0,pady=6,sticky=W)
        ward_combo=ttk.Combobox(scrollable_frame1,textvariable=ward_var,font=("arial",12),state='readonly',width=18)
        ward_combo['values']=self.bed_types
        ward_combo.grid(row=7,column=1,padx=5,pady=6)
        #To find bed number according to the type
        ward_combo.bind("<<ComboboxSelected>>",lambda event:self.find_bed_val(bed_no_var,ward_var.get()))

        # Get the date
        date_=time.strftime("%d-%m-%Y")
        # set the date
        admit_date_var.set(date_)
        admit_date_label=Label(scrollable_frame1,text="Admission Date",font=("arial",10,'bold'))
        admit_date_label.grid(row=6,column=0,pady=6,sticky=W)
        admit_date_entry=Entry(scrollable_frame1,textvariable=admit_date_var,font=("arial",12))
        admit_date_entry.grid(row=6,column=1,padx=5,pady=6)

        department_label=Label(scrollable_frame1,text="Select Department*",font=("arial",10,'bold'))
        department_label.grid(row=8,column=0,pady=6,sticky=W)
        department_combo=ttk.Combobox(scrollable_frame1,textvariable=department_var,font=("arial",12),state='readonly',width=18)
        department_combo['values']=all_depts
        department_combo.grid(row=8,column=1,padx=5,pady=6)
        #To find doctors according to the selected department
        department_combo.bind("<<ComboboxSelected>>",lambda event: self.find_docs_val(doctor_combo,department_var.get(),doctor_var,doc_dict))

        doctor_label=Label(scrollable_frame1,text="Doctor",font=("arial",10,'bold'))
        doctor_label.grid(row=9,column=0,pady=6,sticky=W)
        doctor_combo=ttk.Combobox(scrollable_frame1,textvariable=doctor_var,font=("arial",12),width=18)
        doctor_combo['values']=()
        doctor_combo.grid(row=9,column=1,padx=5,pady=6)
        
        bed_label=Label(scrollable_frame1,text="Bed No.",font=("arial",10,'bold'))
        bed_label.grid(row=10,column=0,pady=6,sticky=W)
        bed_entry=Entry(scrollable_frame1,textvariable=bed_no_var,font=("arial",12))
        bed_entry.grid(row=10,column=1,padx=5,pady=6)

        contact_label=Label(scrollable_frame1,text="Mobile No.*",font=("arial",10,'bold'))
        contact_label.grid(row=11,column=0,pady=6,sticky=W)
        contact_entry=Entry(scrollable_frame1,textvariable=contact_var,font=("arial",12))
        contact_entry.grid(row=11,column=1,padx=5,pady=6)

        email_label=Label(scrollable_frame1,text="Email",font=("arial",10,'bold'))
        email_label.grid(row=12,column=0,pady=6,sticky=W)
        email_entry=Entry(scrollable_frame1,textvariable=email_var,font=("arial",12))
        email_entry.grid(row=12,column=1,padx=5,pady=6)

        address_label=Label(scrollable_frame1,text="Address",font=("arial",10,'bold'))
        address_label.grid(row=13,column=0,pady=7,sticky=W)
        address_text=Text(scrollable_frame1,font=("arial",12),width=20,height=3)
        address_text.grid(row=13,column=1,padx=5,pady=6)

        cancel_btn= Button(scrollable_frame1,text="Cacel",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.clear_fields(val_list,address_text))
        cancel_btn.grid(row=15,column=0,padx=5,pady=10,sticky=W)

        update_btn= Button(scrollable_frame1,text="Update Data",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= lambda: self.update_patient_data(val_list,address_text,doc_dict))
        update_btn.grid(row=15,column=1,padx=5,pady=10,sticky=E)

    def update_patient_data(self,values,addr,doc_dict):

        '''Used to Update patient to the database. Take 3 arguments 1st- A list of values to be used, 2nd- address text, 3rd- a dictionary that contain doctor name with id.
        
        address text treated separately becuase Text has different syntax'''

        # extract the data from the parameter and store into a list
        val_list=[]
        for value in values:
            val_list.append(value.get())

        # add address to the list
        val_list.append(addr.get("1.0",END).strip())

        # remember the order of the values in the list here it is as follows-
        # val_list=[id,name,guardian's name,dob,gender,ward,admit date,department,doctor,bed no,contact,email,address]


        try:
            # Check the id field is empty or not
            if val_list[0]=="":
                messagebox.showerror("Error","Id field data removed!! Try again, click the 'Update' button from the search result",parent=self.root)
            # Check the '*' marked fields is empty or not
            if val_list[1]=="" or val_list[2]=="" or val_list[3]=="" or val_list[7]=="" or val_list[10]=="":
                messagebox.showerror("Error","'*' marked fields must be filled",parent=self.root)
            
            elif val_list[9]!='' and val_list[5]=='':
                messagebox.showerror("Error","Bed number privided but Ward not selected",parent=self.root)

            else:
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()

                # to check the bed available or not
                cur.execute("select pid,name from bed, patient where bed.pid=patient.id and bed.id=?",(val_list[9],))
                p_d=cur.fetchone()
                if p_d!=None:
                    pid=p_d[0]
                    pname=p_d[1]
                else:
                    pid=pname=None

                # to match the bed number with the ward
                cur.execute("select category from bed where id=?",(val_list[9],))
                category,=cur.fetchone()

                if pid!=None and pid!=val_list[0]:
                    messagebox.showerror("Error",f"Bed {val_list[9]} is already booked for patient {pid} ( {pname} ) change the number",parent=self.root)

                elif val_list[5] != category and val_list[9]!='':
                    messagebox.showerror("Error",f"Bed {val_list[9]} is allocated for another category ({category}) not for {val_list[5]} or not exists, change the status or bed number",parent=self.root)

                # otherwise add the patient data to the database
                else:
                    cur.execute("update patient set name=?,guardian_name=?,dob=?,gender=?,status=?,admit=?,department=?,doctor=?,mobile=?,email=?,address=? where id=?",(
                        val_list[1],
                        val_list[2],
                        val_list[3],
                        val_list[4],
                        val_list[5],
                        val_list[6],
                        val_list[7],
                        doc_dict[val_list[8]],
                        val_list[10],
                        val_list[11],
                        val_list[12],
                        val_list[0]
                    ))

                    # Remove the patient from the bed table if exist
                    cur.execute("select id from bed where pid=?",(val_list[0],))
                    tmp=cur.fetchone()
                    if tmp is not None : 
                        tmp,=tmp
                        cur.execute("update bed set pid=? where id=?",(None,tmp))

                    # Upadte the bed table if bed allocated for the patient
                    if val_list[9]!='':
                        cur.execute("update bed set pid=? where id=?",(val_list[0],val_list[9]))

                    # create a list to call display()
                    cur.execute("select * from patient where id= '{}'".format(val_list[0]))
                    display_list_items=list(cur.fetchone())

                    con.commit()
                    con.close()

                    self.display_patient_details(val_list[0],display_list_items)

                    messagebox.showinfo("Sucess!!","Patient {}(id: {}) Updated to database sucessfully...".format(val_list[1],val_list[0]),parent=self.root)

        except Exception as exp:
            messagebox.showerror("Error-26",f"Error due to {str(exp)}",parent=self.root)

    def delete_patient_data(self,id,tablename=None,searchtable=None):
        
        ''' Delete Patient details from the database. Take 3 arguments 1st- ID to find the patient to be deleted, 2nd- name of the table where the data is, 3rd- search table reference if multiple search results found '''

        # Confirmation message
        result= messagebox.askquestion("Are You Sure?","To delete data of the {} click 'yes' button".format(tablename),parent=self.root)

        # if clicked 'yes' by the user then delete the Patient
        if result=='yes':
            con=sqlite3.connect(database="./hms1.db")
            cur=con.cursor()
            try:
                # Set null to the bed table
                cur.execute("select id from bed where pid=?",(id,))
                tmp=cur.fetchone()
                if tmp is not None : 
                    tmp,=tmp
                    cur.execute("update bed set pid=? where id=?",(None,tmp))
                
                # Delte the patient from patient table
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

    def display_patient_details(self,pid,values=None,tablename=None):

        ''' Take 3 arguments 1st- patient id, 2nd- patient details, 3rd- search table reference and display Patient details into the Output frame '''

        # To manage the function call from search action
        if pid=='-1':
            # for handling multiple values in searh table
            tmp=tablename.focus()
            tmp=tablename.item(tmp)['values']
            pid=tmp[0]

            try:
                # find the patient details to be displayed
                con=sqlite3.connect(database="./hms1.db")
                cur=con.cursor()
                cur.execute("select * from patient where id=?",(pid,))
                values=cur.fetchone()
                con.commit()
                con.close()

            except Exception as exp:
                messagebox.showerror("Error-13",f"Error due to {str(exp)}",parent=self.root)

        ### ================ Display Patient Data ====================

        # Clear the Output frame
        self.clear_frame(self.output_frame)

        # find name of the doctor
        doc_name,err1= find_col_vals('name','employees','id= "{}"'.format(values[8]))
        bed_no,err2= find_col_vals('id','bed','pid="{}"'.format(values[0]))

        if err1!='' or err2!='': 
            messagebox.showerror("Error-08",f"Error due to {str(err)}",parent=self.root)

        # Display data ------------------------------------------

        Label(self.output_frame,text="Patient Details ",font=("arial",15,'bold','underline'),fg="#14213d").pack(side=TOP,anchor='nw')

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

        name_label=Label(scrollable_frame1,text=f"Patient Name :  {values[1]}",font=("arial",10,'bold'))
        name_label.grid(row=0,column=0,pady=6,sticky=W,columnspan=4)

        guardian_label=Label(scrollable_frame1,text=f"Guardian's Name :  {values[2]}",font=("arial",10,'bold'))
        guardian_label.grid(row=1,column=0,pady=6,sticky=W,columnspan=4)

        id_label=Label(scrollable_frame1,text=f"Patient Id :  {values[0]}",font=("arial",10,'bold'))
        id_label.grid(row=2,column=0,pady=6,sticky=W,columnspan=2)

        dob_label=Label(scrollable_frame1,text=f"Date Of Barth :  {values[3]}",font=("arial",10,'bold'))
        dob_label.grid(row=3,column=0,pady=6,sticky=W,columnspan=2)

        gender_label=Label(scrollable_frame1,text=f"Gender :  {values[4]}",font=("arial",10,'bold'))
        gender_label.grid(row=4,column=0,pady=6,sticky=W,columnspan=2)

        admit_label=Label(scrollable_frame1,text=f"Admission Date :  {values[6]}",font=("arial",10,'bold'))
        admit_label.grid(row=5,column=0,pady=6,sticky=W,columnspan=2)

        ward_label=Label(scrollable_frame1,text=f"Ward :  {values[5]}",font=("arial",10,'bold'))
        ward_label.grid(row=6,column=0,pady=6,sticky=W,columnspan=4)

        bed_label=Label(scrollable_frame1,text=f"Bed No. :  {bed_no[0]}",font=("arial",10,'bold'))
        bed_label.grid(row=7,column=0,pady=6,sticky=W,columnspan=4)

        dept_label=Label(scrollable_frame1,text=f"Department :  {values[7]}",font=("arial",10,'bold'))
        dept_label.grid(row=8,column=0,pady=6,sticky=W,columnspan=4)

        doc_label=Label(scrollable_frame1,text=f"Doctor : {doc_name[0]} ({values[8]})",font=("arial",10,'bold'))
        doc_label.grid(row=9,column=0,pady=6,sticky=W,columnspan=3)

        mobile_label=Label(scrollable_frame1,text=f"Mobile No:  {values[9]}",font=("arial",10,'bold'))
        mobile_label.grid(row=10,column=0,pady=6,sticky=W,columnspan=3)

        email_label=Label(scrollable_frame1,text=f"Email :  {values[10]}",font=("arial",10,'bold'))
        email_label.grid(row=11,column=0,pady=6,sticky=W,columnspan=4)

        address_label=Label(scrollable_frame1,text=f"Address :",font=("arial",10,'bold'))
        address_label.grid(row=12,column=0,pady=6,sticky='nw')
        address_value_label=Label(scrollable_frame1,text=f"{values[11]}",font=("arial",10,'bold'),wraplength=230,justify='left')
        address_value_label.grid(row=12,column=1,sticky=W,columnspan=3)

        clr_btn= Button(scrollable_frame1,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda: self.clear_frame(self.output_frame,True))
        clr_btn.grid(row=15,column=0,padx=3,pady=10,sticky=W)

        update_btn= Button(scrollable_frame1,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.upadate_patient(list(values)+list(doc_name)+list(bed_no)))
        update_btn.grid(row=15,column=1,padx=3,pady=10,sticky=W)

        delete_btn= Button(scrollable_frame1,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=lambda:self.delete_patient_data(values[0],"patient",tablename))
        delete_btn.grid(row=15,column=2,padx=3,pady=10,sticky=W)


# Main function
if __name__=='__main__':
    root=Tk()
    obj=RPT(root,"Hopeview Medical Center")   # Create the object of dashboard class HMS
    root.mainloop()