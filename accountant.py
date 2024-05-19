# The code has not been updated yet, please wait for a while to get the updated code.

from tkinter import*
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
import time
import tempfile
import os
from reusable_function import id_generator
class Acc:

    def __init__(self,root,hname="Hospital Management System",parent=None,row=None):

        '''The constructor accept 4 arguments 1st- root name ,2nd- name of the hospital, 3rd- parent window reference, 4th- employee data who logged in.'''

        # Storing arguments
        self.hname= hname # Name of the hospital
        self.root=root 
        self.parent=parent
        
        # Window configurations
        self.root.title("Accounts - {}".format(self.hname)) # set the title
        self.root.geometry("1250x650+150+100") # Set the window width, height and position
        self.root.wm_iconbitmap("./images/hms_logo.ico") # Set the Icon
        self.root.resizable(FALSE,FALSE) # Block the resizable feature
        self.root.focus_force()

        # Handle the exit event
        if self.parent!=None:
            self.root.protocol("WM_DELETE_WINDOW",self.onclosing)

        # =============== Title Bar ===================
        self.title_icon=Image.open("./images/hms_logo1.png")
        self.title_icon=self.title_icon.resize((50,50))
        self.title_icon=ImageTk.PhotoImage(self.title_icon)
        title=Label(self.root,text="Hospital Management System", image= self.title_icon,compound=LEFT,font=("arial black",20),bg="#2b2d42",fg="#edf2f4",padx=10)
        title.place(x=0,y=0,relwidth=1,height=70)

        # ================ Sub Title Bar ================
        self.sub_title=Label(self.root,text="Welcome to Hospital Management System \t\t Date: DD-MM-YYY \t\t Time: HH:MM:SS",font=("Cooper Std Black",13,"bold"),bg="#ef233c",fg="#ffffff")
        self.sub_title.place(x=0,y=70,relwidth=1,height=30)
        self.update_date_time()

        # ================ Variables ====================
        self.id_var=StringVar()
        self.name_var=StringVar()
        self.dob_var=StringVar()
        self.gender_var=StringVar()
        self.admitdate_var=StringVar()
        self.doc_var=StringVar()
        self.department_var=StringVar()
        self.contact_var=StringVar()
        self.input_win_heading=StringVar()
        self.category_var= StringVar()
        self.type_var= StringVar()
        self.charges_var= StringVar()  
        self.qty_var=StringVar()  
        self.search_txt=StringVar() 
        self.search_by_var=StringVar()   
        self.address_value=StringVar()
        self.cart_var=[]
        self.search_charges_vals =('type','category','charges')
        self.type_vals= ('Bed','Doctor','Equipment')

        # ================ Profile view =================
        profile_frame= LabelFrame(self.root,text="Admin Profile",font=("arial",12),bd=4,relief=RIDGE)
        profile_frame.place(x=10,y=103,width=400,height=200)

        #Profile_img
        self.profile_img=Label(self.root,image=None,padx=10)
        self.profile_img.place(x=15,y=125)
        self.img_src_sel(row,self.profile_img)
        profile_info_frame= Frame(self.root,padx=10,pady=10)
        profile_info_frame.place(x=155,y=125,width=240,height=160)

        self.profile_breif(profile_info_frame,row)

        # Logout btn
        logout_btn= Button(profile_frame,text="Logout",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",10),pady=15,cursor="hand2",command=self.onclosing)
        logout_btn.place(x=10,y=140,height=30,width=120)
    

        # =================== Input window ==================
        self.input_frame= Frame(self.root,bd=4,relief=RIDGE,padx=10,pady=10)
        self.input_frame.place(x=420,y=110,width=400,height=520)

        # self.add_items()
        self.search_bill()

        # =================== Output window ==================

        self.output_frame= Frame(self.root,bd=4,relief=RIDGE,padx=10,pady=10)
        self.output_frame.place(x=830,y=110,width=400,height=520)
        Label(self.output_frame,text="No data to show on output window!!",font=("arial blak",13),fg="#979dac",pady=20).pack(side=TOP,anchor=W)

        # ==================== Actions Buttons =============

        btn_frame=Frame(self.root,bg="#e5e5e5")
        btn_frame.place(x=10,y=310,width=400)

        gen_bill_btn=Button(btn_frame,text="Generate Bill",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_items)
        gen_bill_btn.pack(fill=X,pady=10)

        search_bill_btn=Button(btn_frame,text="View/Update Bill",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.search_bill)
        search_bill_btn.pack(fill=X,pady=10)

        add_charges_btn=Button(btn_frame,text="Add Charges",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.add_charges)
        add_charges_btn.pack(fill=X,pady=10)

        search_charges_btn=Button(btn_frame,text="View/Update Charges",bd=0,bg="#14213d",fg="#edf2f4",font=("arial black",14),pady=10,cursor="hand2",command=self.search_charges)
        search_charges_btn.pack(fill=X,pady=10)

    # Manage Bills

    def add_items(self):
        self.clear_frame(self.input_frame)
        self.item_vals= self.find_col_vals('type','charges')
        # self.clear_fields()
        # self.id_var.set('PID001')
        # self.type_var.set('Bed')
        # self.category_var.set('ICU')
        # self.qty_var.set('2')
        Label(self.input_frame,text="Generate Bill",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)
        # self.input_win_heading.set("Generate Bill")

        self.subinput_frame1= Frame(self.input_frame,width=372,height=200,padx=5,pady=5)
        self.subinput_frame1.grid(row=1,column=0,columnspan=3,sticky=W)

        self.subinput_frame2= Frame(self.input_frame,width=372,height=260,bd=4,relief=RIDGE,padx=5,pady=5)
        self.subinput_frame2.grid(row=2,column=0,columnspan=3,sticky=W)

        id_label=Label(self.subinput_frame1,text="Patient Id",font=("arial",10,'bold'))
        id_label.grid(row=1,column=0,pady=6,sticky=W)
        id_entry=Entry(self.subinput_frame1,textvariable=self.id_var,font=("arial",12))
        id_entry.grid(row=1,column=1,padx=5,pady=6)

        item_label=Label(self.subinput_frame1,text="Item Type",font=("arial",10,'bold'))
        item_label.grid(row=2,column=0,pady=6,sticky=W)
        item_combo=ttk.Combobox(self.subinput_frame1,textvariable=self.type_var,font=("arial",12),width=18)
        item_combo['values']= self.item_vals
        item_combo.grid(row=2,column=1,padx=5,pady=6)
        item_combo.bind("<<ComboboxSelected>>",lambda event:self.update_category_combo(category_combo))

        category_label=Label(self.subinput_frame1,text="Category/Dept",font=("arial",10,'bold'))
        category_label.grid(row=3,column=0,pady=6,sticky=W)
        category_combo=ttk.Combobox(self.subinput_frame1,textvariable=self.category_var,font=("arial",12),width=18)
        category_combo['values']=()
        category_combo.grid(row=3,column=1,padx=5,pady=6)

        qnt_label=Label(self.subinput_frame1,text="Quantity/Days",font=("arial",10,'bold'))
        qnt_label.grid(row=4,column=0,pady=6,sticky=W)
        qnt_entry=Entry(self.subinput_frame1,textvariable=self.qty_var,font=("arial",12))
        qnt_entry.grid(row=4,column=1,padx=5,pady=6)

        add_btn= Button(self.subinput_frame1,text="Add to cart",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.add_to_cart)
        add_btn.grid(row=5,column=1,padx=10,pady=10,sticky=E)

        gen_bill_btn= Button(self.subinput_frame1,text="Generate Bill",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.gen_bill_string)
        gen_bill_btn.grid(row=5,column=0,padx=5,pady=10,sticky=E)

        self.show_cart()

    def update_category_combo(self,name):
        self.category_var.set('')
        cat_vals=self.find_col_vals('category','charges',f"type='{self.type_var.get()}'")
        self.update_combo(name,cat_vals)
    
    def add_to_cart(self):
        # self.input_win_heading.set("Add to cart")
        result=''
        if self.id_var.get()=="" or self.type_var.get()=="" or self.category_var.get()=="" or self.qty_var.get()=="":
            messagebox.showerror("Error","All fields must be filled",parent=self.root)

        elif self.qty_var.get()=='0':
            i=0
            for item in self.cart_var:
                if item[0]==self.type_var.get() and item[1]== self.category_var.get():
                    result= messagebox.askquestion("Warning","The item already in cart do you want to update the cart?",parent=self.root) 
                    break
                i+=1
            if result=='yes':
                self.cart_var.pop(i)
            elif result=='':
                messagebox.showerror("Error","Quantity 0 not accepted",parent=self.root)
        else:
            tmp=self.find_col_vals('name','patient',f"id='{self.id_var.get()}'")
            if tmp==() or tmp[0]==None:
                messagebox.showerror("Error","Patient not found! check the PID",parent=self.root)
            else:
                self.name_var.set(tmp[0])
                tmp,=self.find_col_vals('charges','charges',f"type='{self.type_var.get()}' and category='{self.category_var.get()}'")
                self.charges_var.set(tmp)

                # Manage Cart
                amt= int(self.qty_var.get())*float(self.charges_var.get())
                i=0
                for item in self.cart_var:
                    if item[0]==self.type_var.get() and item[1]== self.category_var.get():
                       result= messagebox.askquestion("Warning","The item already in cart do you want to update the cart?",parent=self.root) 
                       break
                    i+=1
                if result=='yes':
                    self.cart_var.pop(i)
                    self.cart_var.append([self.type_var.get(),self.category_var.get(),self.qty_var.get(),amt])
                elif result=='':
                    self.cart_var.append([self.type_var.get(),self.category_var.get(),self.qty_var.get(),amt])
        self.update_cart()
        
    def show_cart(self):

        self.cart_label1=Label(self.subinput_frame2, text=f"{'-'*80}",font=("arial blak",10),fg="#979dac")
        self.cart_label1.place(x=10,y=18)
        self.cart_label2=Label(self.subinput_frame2, text="PID: ------ \t Name: ------ ",font=("arial blak",10))
        self.cart_label2.place(x=10,y=5)

        multi_res_frame= Frame(self.subinput_frame2)
        multi_res_frame.place(x=10,y=40,width=335,height=200)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)
        scroll_x=Scrollbar(multi_res_frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
        self.cart_table=ttk.Treeview(multi_res_frame,columns=('sl','type','category','qty','amt'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.cart_table.xview)
        scroll_y.config(command=self.cart_table.yview)
        self.cart_table.heading('sl',text='Sl No.')
        self.cart_table.heading('type',text='Type')
        self.cart_table.heading('category',text="Category")
        self.cart_table.heading('qty',text='Qty.')
        self.cart_table.heading('amt',text='Amount')
        self.cart_table['show']='headings'
        self.cart_table.column('sl',width=50,anchor=CENTER)
        self.cart_table.column('type',width=90,anchor=CENTER)
        self.cart_table.column('category',width=110,anchor=CENTER)
        self.cart_table.column('qty',width=50,anchor=CENTER)
        self.cart_table.column('amt',width=70,anchor=CENTER)
        self.cart_table.pack(fill=BOTH,expand=1)
        self.cart_table.bind("<ButtonRelease-1>",lambda event: self.delete_cart_items())

    def update_cart(self):
        self.cart_label2.config(text=f"PID: {self.id_var.get()}\t Name: {self.name_var.get()}")
        self.cart_table.delete(*self.cart_table.get_children())
        i=1
        for item in self.cart_var:
            vals=[i]+item
            self.cart_table.insert('',END,values=vals)
            i+=1
    
    def delete_cart_items(self):
        result= messagebox.askquestion("Are You Sure?","To delete the data click 'yes' button",parent=self.root)
        if result=='yes':
            tmp=self.cart_table.focus()
            tmp=self.cart_table.item(tmp)['values']
            self.cart_var.pop(tmp[0]-1)
            self.update_cart()

    def gen_bill_string(self,flag=0):
        if self.cart_var==[]:
            messagebox.showerror("Error","Add Items to cart before generate bill",parent=self.root)
        else:
            self.bill_str=''
            for items in self.cart_var:
                self.bill_str=self.bill_str+','.join(map(str,items))+';'

            self.bill_str=self.bill_str[:len(self.bill_str)-1]
            if self.input_win_heading.get()=="Update Bill":
                self.display_bill()
                self.update_bill_data()
            else:
                # generate ID for the Admin
                self.bill_id,err=id_generator('bills')
                if err!='': 
                    messagebox.showerror("Error-09",f"Error due to {str(err)}",parent=self.root)
                else:
                    self.date_var=time.strftime("%d-%m-%Y")
                    self.display_bill()
                    self.save_bill()

    def save_bill(self):
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        self.input_win_heading.set("Save Bill")
        try:
            cur.execute("insert into bills (id,pid,b_date,tamt,items) values(?,?,?,?,?)",(
                self.bill_id,
                self.id_var.get(),
                self.date_var,
                self.tamt,
                self.bill_str
            ))
            con.commit()
            messagebox.showinfo("Sucess!!",f"Bill - {self.bill_id} added to database sucessfully",parent=self.root)
            self.print_vals=[self.bill_id,self.id_var.get(),self.date_var,self.bill_str]
            self.clear_fields()
            self.update_cart()
        except Exception as exp:
            messagebox.showerror("Error-01",f"Error due to {str(exp)}",parent=self.root)
        con.close()
    
    def fetch_bill_data(self,flag=0):
        if flag==1:
            tmp=self.search_table.focus()
            tmp=self.search_table.item(tmp)['values']
            self.bill_str=tmp[4]
            self.bill_id=tmp[0]
            self.date_var=tmp[2]
            self.id_var.set(tmp[1])
        
        
        self.print_vals=[self.bill_id,self.id_var.get(),self.date_var,self.bill_str]
        
        self.name_var.set(self.find_col_vals('name','patient',f"id='{self.id_var.get()}'")[0])
        self.address_value.set(self.find_col_vals('address','patient',f"id='{self.id_var.get()}'")[0].strip())
        self.contact_var.set(self.find_col_vals('mobile','patient',f"id='{self.id_var.get()}'")[0])
        self.cart_var=[]
        if len(self.bill_str)>1:
            tmp_l=self.bill_str.split(';')
            for item in tmp_l:
                self.cart_var.append(item.split(','))
        else:
            self.cart_var.append(self.bill_str.split(','))
            
        # print(self.cart_var)
        # print(self.bill_str)
        self.display_bill()

    def search_bill(self):
        self.clear_frame(self.input_frame)
        
        Label(self.input_frame,text="Search Bill ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)
        self.input_win_heading.set("Search")

        search_lable=Label(self.input_frame,text="Search By",font=("arial",10,'bold'))
        search_lable.grid(row=1,column=0,pady=6,sticky=W)
        search_combo=ttk.Combobox(self.input_frame,font=("arial",12),state='readonly',width=18,textvariable=self.search_by_var,cursor='hand2')
        search_combo['values']=['id','pid','b_date']
        search_combo.grid(row=1,column=1,pady=6)
        search_combo.current(0)

        search_value_lable=Label(self.input_frame,text="Enter Value",font=("arial",10,'bold'))
        search_value_lable.grid(row=2,column=0,pady=6,sticky=W)
        search_value_entry=Entry(self.input_frame,font=("arial",12),textvariable=self.search_txt)
        search_value_entry.grid(row=2,column=1,padx=10,pady=6)
        
        search_btn= Button(self.input_frame,text="Serach",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.search_bill_data)
        search_btn.grid(row=4,column=1,padx=10,pady=10,sticky=E)

        self.subinput_frame= Frame(self.input_frame,height=350,width=372)
        self.subinput_frame.grid(row=6,column=0,columnspan=3)

    def search_bill_data(self):
        self.clear_frame(self.subinput_frame)
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        if self.search_txt.get()=="" or self.search_by_var.get()=="":
            messagebox.showerror("Searching failure!!","Please enter some value in searchbox...",parent=self.root)
        else:
            try:
                cur.execute("select id,pid,b_date,tamt,items from bills where "+self.search_by_var.get()+" like '%"+self.search_txt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:    
                    # Handle multiple results
                    if len(rows)==1:
                        self.bill_str=rows[0][4]
                        self.bill_id=rows[0][0]
                        self.date_var=rows[0][2]
                        self.id_var.set(rows[0][1])
                        self.fetch_bill_data(0)
                    else:
                        Label(self.subinput_frame, text=f"{'-'*80}",font=("arial blak",10),fg="#979dac").place(x=8,y=0)

                        multi_res_frame= Frame(self.subinput_frame)
                        multi_res_frame.place(x=8,y=30,width=350,height=270)
                        
                        self.style = ttk.Style()
                        self.style.theme_use("clam")
                        self.style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)
                        scroll_x=Scrollbar(multi_res_frame,orient=HORIZONTAL)
                        scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
                        self.search_table=ttk.Treeview(multi_res_frame,columns=('id','pid','date','tamt'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
                        scroll_x.pack(side=BOTTOM,fill=X)
                        scroll_y.pack(side=RIGHT,fill=Y)
                        scroll_x.config(command=self.search_table.xview)
                        scroll_y.config(command=self.search_table.yview)
                        self.search_table.heading('id',text='BID')
                        self.search_table.heading('pid',text="PID")
                        self.search_table.heading('date',text='Date')
                        self.search_table.heading('tamt',text='Amt.')
                        self.search_table['show']='headings'
                        self.search_table.column('id',width=100,anchor=CENTER)
                        self.search_table.column('pid',width=100,anchor=CENTER)
                        self.search_table.column('date',width=80,anchor='ne')
                        self.search_table.column('tamt',width=100,anchor='ne')
                        self.search_table.pack(fill=BOTH,expand=1)
                        self.search_table.bind("<ButtonRelease-1>",lambda event: self.fetch_bill_data(1))

                        for row in rows:
                            self.search_table.insert('',END,values=row)

                        messagebox.showinfo("Multiple Records!!","Multiple records found select one to continue...",parent=self.root)
                else:
                    messagebox.showerror("Error","Data not found in database...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-08",f"Error due to {str(exp)}",parent=self.root)
        con.close()
        # self.clear_fields()

    def update_bill(self):
        self.input_win_heading.set("Update Bill")
        self.fetch_bill_data()
        self.add_items()
        self.update_cart()

    def update_bill_data(self):
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        self.input_win_heading.set("Update Bill")
        self.date_var=time.strftime("%d-%m-%Y")

        try:
            cur.execute("update bills set pid=?,b_date=?,tamt=?,items=? where id=?",(
                self.id_var.get(),
                self.date_var,
                self.tamt,
                self.bill_str,
                self.bill_id
            ))
            con.commit()
            messagebox.showinfo("Sucess!!",f"Bill - {self.bill_id} Updated sucessfully",parent=self.root)
            # self.clear_fields()
            self.cart_var=[]
            self.update_cart()
        except Exception as exp:
            messagebox.showerror("Error-01",f"Error due to {str(exp)}",parent=self.root)
        con.close()

    def delete_bill(self):
        result= messagebox.askquestion("Are You Sure?","To delete the data click 'yes' button",parent=self.root)
        if result=='yes':
            con=sqlite3.connect(database="hms1.db")
            cur=con.cursor()
            try:
                cur.execute("delete from bills where id=?",(self.bill_id,))
                con.commit()
                self.ouput_win_clear()
                if self.input_win_heading.get()=="Search":
                    self.clear_frame(self.subinput_frame)
                self.clear_fields()
                messagebox.showinfo("Sucess!!","Data deleted sucessfully...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-04",f"Error due to {str(exp)}",parent=self.root)
            con.close()

    def print_bill(self):
        #   messagebox.showinfo("Print","Please wait while printing",parent=self.root)
        print(self.input_win_heading.get())
        if self.input_win_heading.get()=="Save Bill" or self.input_win_heading.get()=="Update Bill":
            print(self.print_vals)
            self.bill_id=self.print_vals[0]
            self.id_var.set(self.print_vals[1])
            self.date_var=self.print_vals[2]
            self.bill_str=self.print_vals[3]
            self.fetch_bill_data()
        
        print_bill_str="{:^77}\nHospital Name\nhospital address\nph no.\nemail.\n{:^77}\nPatient Details: \nPID- {:<20}\n{:<30}\naddress- {:<30}\nph no.- {:<15}\n{:<40}{:>37}\n".format(f"{'='*77}",'----- Invoice -----',self.id_var.get(),self.name_var.get(),self.address_value.get(),self.contact_var.get(),f"Bill ID- {self.bill_id} ",f"Date- {self.date_var}")

        print_bill_str+="{:^77}\n {:^6} | {:^18} | {:^20} | {:^6} | {:^10} \n{:^77}\n".format(f"{'='*77}",'Sl No.','Type','Category','Qty','Price',f"{'='*77}")

        i=1
        for item in self.cart_var:
            print_bill_str+="\n {:>5} {:2} {:<18} {:2} {:<20} {:2} {:>5} {:2} {:>9}".format(i,' ',item[0],' ',item[1],' ',item[2],' ',item[3])
            i+=1
        print_bill_str+="\n{:^77}\n{:>74}".format(f"{'-'*77}",f"Total= {self.tamt}")
        new_file= tempfile.mktemp('.txt')
        open(new_file,'w').write(print_bill_str)
        os.startfile(new_file,'print')
        self.clear_fields()
        
    def display_bill(self):
        
        self.clear_frame(self.output_frame)

        canvas_container= Frame(self.output_frame)
        canvas_container.pack(side=LEFT,anchor='nw')
        mycanvas= Canvas(canvas_container,width=350,height=465)
        mycanvas.pack(side=LEFT,pady=2)
        
        y_scrollbar=Scrollbar(canvas_container, orient='vertical')
        y_scrollbar.pack(side=RIGHT, fill=Y)
        y_scrollbar.config(command=mycanvas.yview)

        mycanvas.configure(yscrollcommand=y_scrollbar.set)
        mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
        bill_area= Frame(mycanvas,bd=0,bg='#fcfcfc')
        mycanvas.create_window((0,0),window=bill_area,anchor='nw')

        bill_top=Frame(bill_area,background='#fcfcfc')
        bill_top.grid(row=0,column=0,sticky=W)

        bill_mid=Frame(bill_area,background='#fcfcfc')
        bill_mid.grid(row=1,column=0,sticky=W)

        bill_bottom=Frame(bill_area,background='#fcfcfc')
        bill_bottom.grid(row=2,column=0,sticky=W)

        # Bill Top Section

        Label(bill_top,
text=f'''Hospital Name
hospital address
ph no.
email.
\t\t ----- Invoice -----\n
Patient Details: \t\t\tDate- {self.date_var}
PID-  {self.id_var.get()}
Mr. {self.name_var.get()}
address-	{self.address_value.get()}			   
ph no.-     {self.contact_var.get()}

Bill ID-  {self.bill_id} ''',font=("arial",9),justify="left",background='#fcfcfc').pack(side=LEFT,anchor='nw')

        # Bill Mid Section
        Label(bill_mid,text=f"{'-'*69}",background='#fcfcfc').grid(row=0,column=0,sticky=W,columnspan=5)
        Label(bill_mid,text=f" Sl no.",width=4,wraplength=40,background='#fcfcfc').grid(row=2,column=0,sticky=W)
        Label(bill_mid,text=f"Type",width=12,wraplength=100,background='#fcfcfc').grid(row=2,column=1,sticky=W)
        Label(bill_mid,text=f"Category/ Dept.",width=12,wraplength=100,background='#fcfcfc').grid(row=2,column=2,sticky=W)
        Label(bill_mid,text=f"Qty.",width=4,background='#fcfcfc').grid(row=2,column=3,sticky=W)
        Label(bill_mid,text=f"Price",width=11,background='#fcfcfc').grid(row=2,column=4,sticky=W)
        Label(bill_mid,text=f"{'-'*69}",background='#fcfcfc').grid(row=3,column=0,sticky=W,columnspan=5)

        i=1
        self.tamt=0
        for item in self.cart_var:
            Label(bill_mid,text=f" {i}",width=4,wraplength=40,background='#fcfcfc').grid(row=i+3,column=0,sticky=W)
            Label(bill_mid,text=f"{item[0]}",width=12,wraplength=100,background='#fcfcfc').grid(row=i+3,column=1,sticky=W)
            Label(bill_mid,text=f"{item[1]}",width=12,wraplength=100,background='#fcfcfc').grid(row=i+3,column=2,sticky=W)
            Label(bill_mid,text=f"{item[2]}",width=4,background='#fcfcfc').grid(row=i+3,column=3,sticky=E)
            Label(bill_mid,text=f"{item[3]}",width=11,background='#fcfcfc').grid(row=i+3,column=4,sticky=E) 
            self.tamt+=float(item[3])
            i+=1

        #Bill bottom section
        Label(bill_mid,text=f"{'-'*69}",background='#fcfcfc').grid(row=i+3,column=0,sticky=W,columnspan=5)
        Label(bill_mid,text="Total = ",background='#fcfcfc').grid(row=i+4,column=3,sticky=E)
        Label(bill_mid,text=f"{self.tamt}",width=11,background='#fcfcfc').grid(row=i+4,column=4,sticky=E)
        Label(bill_mid,text=f"{'-'*69}",background='#fcfcfc').grid(row=i+5,column=0,sticky=W,columnspan=5)

        print_btn= Button(bill_bottom,text="Print",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",width=7,command=self.print_bill)
        print_btn.grid(row=0,column=0,padx=3,pady=10,sticky=W)

        self.update_bill_btn= Button(bill_bottom,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.update_bill)
        self.update_bill_btn.grid(row=0,column=1,padx=3,pady=10,sticky=W)

        self.delete_bill_btn= Button(bill_bottom,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.delete_bill)
        self.delete_bill_btn.grid(row=0,column=2,padx=3,pady=10,sticky=W)

        # self.clear_fields()
    # Handle Charges

    def add_charges(self):
        self.clear_frame(self.input_frame)
        Label(self.input_frame,text="Add Charges",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W)
        self.input_win_heading.set("Add charges")

        category_label=Label(self.input_frame,text="Select Type",font=("arial",10,'bold'))
        category_label.grid(row=1,column=0,pady=6,sticky=W)
        category_combo=ttk.Combobox(self.input_frame,textvariable=self.type_var,font=("arial",12),state='readonly',width=18)
        category_combo['values']=self.type_vals
        category_combo.grid(row=1,column=1,padx=5,pady=6)

        category_label=Label(self.input_frame,text="Category",font=("arial",10,'bold'))
        category_label.grid(row=2,column=0,pady=6,sticky=W)
        category_entry=Entry(self.input_frame,textvariable=self.category_var,font=("arial",12))
        category_entry.grid(row=2,column=1,padx=10,pady=6)

        charges_label=Label(self.input_frame,text="Charges",font=("arial",10,'bold'))
        charges_label.grid(row=3,column=0,pady=6,sticky=W)
        charges_entry=Entry(self.input_frame,textvariable=self.charges_var,font=("arial",12))
        charges_entry.grid(row=3,column=1,padx=10,pady=6)

        clear_btn= Button(self.input_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.clear_fields)
        clear_btn.grid(row=5,column=1,padx=20,pady=10,sticky=W)

        save_btn= Button(self.input_frame,text="Save",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.save_charges)
        save_btn.grid(row=5,column=1,padx=20,pady=10,sticky=E)

    def save_charges(self):
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        self.input_win_heading.set("Add Charges")
        try:
            if self.type_var.get()=="" or self.charges_var.get()=="" or self.category_var.get()=="":
                messagebox.showerror("Error","All fields must be filled",parent=self.root)
            else:
                cur.execute("select * from  charges where type=? and category=?",(self.type_var.get(),self.category_var.get()))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error",f"The type and category you entered is already exist change type or category to add new charges",parent=self.root)
                else:
                    cur.execute("insert into charges(type,category,charges) values (?,?,?)",(
                        self.type_var.get(),
                        self.category_var.get(),
                        self.charges_var.get()
                    ))
                    con.commit()
                    self.display_charges_details(self.type_var.get(),self.category_var.get())
                    self.clear_fields()
                    messagebox.showinfo("Sucess!!","New Charges added to database sucessfully...",parent=self.root)
        except Exception as exp:
            messagebox.showerror("Error-07",f"Error due to {str(exp)}",parent=self.root)
        con.close()
    
    def search_charges(self):
        self.clear_frame(self.input_frame)
        
        Label(self.input_frame,text="Search charges ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)
        self.input_win_heading.set("Search")

        search_lable=Label(self.input_frame,text="Search By",font=("arial",10,'bold'))
        search_lable.grid(row=1,column=0,pady=6,sticky=W)
        search_combo=ttk.Combobox(self.input_frame,font=("arial",12),state='readonly',width=18,textvariable=self.search_by_var,cursor='hand2')
        search_combo['values']=self.search_charges_vals
        search_combo.grid(row=1,column=1,pady=6)
        search_combo.current(0)

        search_value_lable=Label(self.input_frame,text="Enter Value",font=("arial",10,'bold'))
        search_value_lable.grid(row=2,column=0,pady=6,sticky=W)
        search_value_entry=Entry(self.input_frame,font=("arial",12),textvariable=self.search_txt)
        search_value_entry.grid(row=2,column=1,padx=10,pady=6)
        
        search_btn= Button(self.input_frame,text="Serach",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.search_charges_data)
        search_btn.grid(row=4,column=1,padx=10,pady=10,sticky=E)

        self.subinput_frame= Frame(self.input_frame)
        self.subinput_frame.grid(row=6,column=0,columnspan=3)

    def search_charges_data(self):
        self.clear_frame(self.subinput_frame)
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        if self.search_txt.get()=="" or self.search_by_var.get()=="":
            messagebox.showerror("Searching failure!!","Please enter some value in searchbox...",parent=self.root)
        else:
            try:
                cur.execute("select * from charges where "+self.search_by_var.get()+" like '%"+self.search_txt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:    
                    # Handle multiple results
                    type_='-1'
                    category='-1'
                    if len(rows)==1:
                        type_=rows[0][0]
                        category=rows[0][1]
                        self.display_charges_details(type_,category)
                    else:
                        Label(self.subinput_frame, text=f"{'-'*90}",font=("arial blak",10),fg="#979dac").grid(row=4,column=0,sticky=W,columnspan = 3)

                        multi_res_frame= Frame(self.subinput_frame,padx=10,pady=10,width=370)
                        multi_res_frame.grid(row=5,column=0,columnspan = 3,sticky=W)
                        
                        self.style = ttk.Style()
                        self.style.theme_use("clam")
                        self.style.configure('Treeview.Heading', background="#14213d",foreground="white",bd=0)
                        scroll_y=Scrollbar(multi_res_frame,orient=VERTICAL)
                        self.search_table=ttk.Treeview(multi_res_frame,columns=('type','category','charges'),yscrollcommand=scroll_y.set)
                        scroll_y.pack(side=RIGHT,fill=Y)
                        scroll_y.config(command=self.search_table.yview)
                        self.search_table.heading('type',text='Type')
                        self.search_table.heading('category',text="Category")
                        self.search_table.heading('charges',text='Charges')
                        self.search_table['show']='headings'
                        self.search_table.column('type',width=110,anchor=CENTER)
                        self.search_table.column('category',width=110,anchor=CENTER)
                        self.search_table.column('charges',width=110,anchor='ne')
                        self.search_table.pack(fill=BOTH,expand=1)
                        self.search_table.bind("<ButtonRelease-1>",lambda event: self.display_charges_details(type_,category))

                        for row in rows:
                            self.search_table.insert('',END,values=row)

                        messagebox.showinfo("Multiple Records!!","Multiple records found select one to continue...",parent=self.root)
                else:
                    messagebox.showerror("Error","Data not found in database...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-08",f"Error due to {str(exp)}",parent=self.root)
        con.close()
        # self.clear_fields()

    def upadate_charges(self):
    
        self.clear_frame(self.input_frame)

        Label(self.input_frame,text="Update Charges ",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,sticky=W,columnspan=2)
        self.input_win_heading.set("Update Charges")

        type_label=Label(self.input_frame,text="Type :",font=("arial",10,'bold'))
        type_label.grid(row=1,column=0,pady=6,sticky=W)
        type_entry=Entry(self.input_frame,textvariable=self.type_var,font=("arial",12),state='readonly')
        type_entry.grid(row=1,column=1,padx=10,pady=6)

        category_label=Label(self.input_frame,text="Category :",font=("arial",10,'bold'))
        category_label.grid(row=2,column=0,pady=6,sticky=W)
        category_entry=Entry(self.input_frame,textvariable=self.category_var,font=("arial",12),state='readonly')
        category_entry.grid(row=2,column=1,padx=10,pady=6)

        charges_label=Label(self.input_frame,text="Charges :",font=("arial",10,'bold'))
        charges_label.grid(row=3,column=0,pady=6,sticky=W)
        charges_entry=Entry(self.input_frame,textvariable=self.charges_var,font=("arial",12))
        charges_entry.grid(row=3,column=1,padx=10,pady=6)

        clear_btn= Button(self.input_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command= self.clear_fields)
        clear_btn.grid(row=12,column=1,padx=20,pady=10,sticky=W)

        update_btn= Button(self.input_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.update_charges_data)
        update_btn.grid(row=12,column=1,padx=20,pady=10,sticky=E)

    def update_charges_data(self):
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        try:
            if self.type_var.get()=="" or self.charges_var.get()=="" or self.category_var.get()=="":
                messagebox.showerror("Error","All fields must be filled",parent=self.root)
            else:
                # modify database
                cur.execute("update charges set charges=? where type=? and category=?",(self.charges_var.get(),self.type_var.get(),self.category_var.get()))
                con.commit()
                self.display_charges_details(self.type_var.get(),self.category_var.get())
                self.clear_fields()
                messagebox.showinfo("Sucess!!","Charges updated sucessfully...",parent=self.root)
        except Exception as exp:
            messagebox.showerror("Error-03",f"Error due to {str(exp)}",parent=self.root)
        con.close()

    def delete_charges_data(self):
        result= messagebox.askquestion("Are You Sure?","To delete the data click 'yes' button",parent=self.root)
        if result=='yes':
            con=sqlite3.connect(database="hms1.db")
            cur=con.cursor()
            try:
                cur.execute("delete from charges where type=? and category=?",(self.type_var.get(),self.category_var.get()))
                con.commit()
                self.ouput_win_clear()
                if self.input_win_heading.get()=="Search":
                    self.clear_frame(self.subinput_frame)
                self.clear_fields()
                messagebox.showinfo("Sucess!!","Data deleted sucessfully...",parent=self.root)
            except Exception as exp:
                messagebox.showerror("Error-04",f"Error due to {str(exp)}",parent=self.root)
            con.close()

    def display_charges_details(self,type_,category):
        con=sqlite3.connect(database="hms1.db")
        cur=con.cursor()
        if type_=='-1':
            tmp=self.search_table.focus()
            tmp=self.search_table.item(tmp)['values']
            type_=tmp[0]
            category=tmp[1]
        try:
            self.clear_frame(self.output_frame)
            cur.execute("select * from charges where type=? and category=?",(type_,category))
            row=cur.fetchone()
            # load data into variables
            self.type_var.set(row[0])
            self.category_var.set(row[1])
            self.charges_var.set(row[2])

            Label(self.output_frame,text="Charges",font=("arial",15,'bold','underline'),fg="#14213d").grid(row=0,column=0,columnspan=4,sticky=W)

            type_label=Label(self.output_frame,text=f"Type :  {row[0]}",font=("arial",10,'bold'))
            type_label.grid(row=1,column=0,pady=6,sticky=W,columnspan=4)

            category_label=Label(self.output_frame,text=f"Category :  {row[1]}",font=("arial",10,'bold'))
            category_label.grid(row=2,column=0,pady=6,sticky=W,columnspan=4)

            charges_label=Label(self.output_frame,text=f"Charges :  {row[2]}",font=("arial",10,'bold'))
            charges_label.grid(row=3,column=0,pady=6,sticky=W,columnspan=4)

            clr_btn= Button(self.output_frame,text="Clear",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.ouput_win_clear)
            clr_btn.grid(row=12,column=0,padx=3,pady=10,sticky=W)

            update_btn= Button(self.output_frame,text="Update",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.upadate_charges)
            update_btn.grid(row=12,column=1,padx=3,pady=10,sticky=W)

            delete_btn= Button(self.output_frame,text="Delete",bd=0,bg="#14213d",fg="white",font=("arial black",10,'bold'),padx=10,cursor="hand2",command=self.delete_charges_data)
            delete_btn.grid(row=12,column=2,padx=3,pady=10,sticky=W)

            con.commit()
        except Exception as exp:
            messagebox.showerror("Error-09",f"Error due to {str(exp)}",parent=self.root)
        con.close()


    def onclosing(self):
        if self.parent!=None:
            self.parent.deiconify()
        self.root.destroy()
        
    def update_date_time(self):
        time_= time.strftime("%I:%M:%S %p")
        date_= time.strftime("%d-%m-%Y")
        self.sub_title.config(text=f"Welcome to Hospital Management System \t\t Date: {date_} \t\t Time: {time_}")
        self.sub_title.after(200,self.update_date_time)

    def update_combo(self,name,val_list):
        self.search_by_var.set("")
        name.configure(values=val_list)

    def img_src_sel(self,gen,lb_name):
        if gen!=None and gen[4]=='female':
            img_src= "D:\\educational\\python program\\Hospital_management_system\\images\\doc_img_f.jpg"
        else:
            img_src= "D:\\educational\\python program\\Hospital_management_system\\images\\doc_img_m.jpg"

        img=Image.open(img_src)
        img= img.resize((130,130))
        img=ImageTk.PhotoImage(img)
        lb_name.configure(image=img)
        lb_name.image=img
        
    def profile_breif(self,frame,row):
        if row==None:
            Label(frame,text=f"....",font=("arial",13)).grid(row=0,sticky=W)
            Label(frame,text=f"ph no-...",font=("arial",13)).grid(row=1,sticky=W)
            Label(frame,text=f"email-...",font=("arial",13)).grid(row=2,sticky=W)
            Label(frame,text=f"department-...",font=("arial",13)).grid(row=3,sticky=W)
            Label(frame,text=f"address- ...",font=("arial",13)).grid(row=4,sticky=W)
        else:
            Label(frame,text=f"{row[1]}",font=("arial",13)).grid(row=0,sticky=W)
            Label(frame,text=f"ph no- {row[10]}",font=("arial",13)).grid(row=1,sticky=W)
            Label(frame,text=f"email- {row[11]}",font=("arial",13)).grid(row=2,sticky=W)
            Label(frame,text=f"department- {row[7]}",font=("arial",13)).grid(row=3,sticky=W)
            Label(frame,text=f"address- {row[12]}",font=("arial",13)).grid(row=4,sticky=W)

    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
        frame.pack_forget()
    
    def find_col_vals(self,col_name,table,condition=''):
        con=sqlite3.connect(database='hms1.db')
        cur=con.cursor()
        if condition=='':
            cur.execute(f'select distinct {col_name} from {table}')
        else:
            cur.execute(f'select distinct {col_name} from {table} where {condition}')
        names=cur.fetchall()
        n=[]
        for row in names:
            n.append(row[0])
        con.close()
        return tuple(n)

    def clear_fields(self):
        self.id_var.set("")
        self.name_var.set("")
        # self.guardian_name_var.set("")
        # self.dob_var.set("")
        # self.gender_var.set("")
        # self.salary_var.set("")
        # self.jdate_var.set("")
        # self.post_var.set("")
        # self.profession_var.set("")
        # self.department_var.set("")
        self.contact_var.set("")
        # self.email_var.set("")
        self.address_value.set("")
        self.qty_var.set("")
        self.search_txt.set("")
        self.category_var.set("")
        self.charges_var.set("")
        self.type_var.set("")
        # self.cart_var=[]

    def ouput_win_clear(self):
        self.clear_frame(self.output_frame)
        Label(self.output_frame,text="No data to show on output window!!",font=("arial blak",13),fg="#979dac",pady=20).pack(side=TOP,anchor=W)

if __name__=="__main__":
    root=Tk()
    obj=Acc(root)
    root.mainloop()