import sqlite3

def id_generator(table):
    
    '''Take the table name as argument and return id and error message(if any) as tupple '''

    try: 
        con=sqlite3.connect(database='./hms1.db')
        cur=con.cursor()
        cur.execute(f"select id from  {table} ORDER BY id DESC LIMIT 1")
        last_id,=cur.fetchone()
        new_id= last_id[:3]+str('{:03}'.format(int(last_id[3:])+1))
        con.close()
        return (new_id,'')
    except Exception as exp:
        return ('',exp)

def find_col_vals(col_name,table,condition=''):

    ''' Take 3 arguments 1st- name of the column whose values we need, 2nd- name of the table, 3rd- any condition (i.e. 'id="EMP001"'). Type of the arguments is String.

    The function returns the values of the column as specified in column name (1st argument) and error message(if any) as a tupple.'''

    try:
        con=sqlite3.connect(database='./hms1.db')
        cur=con.cursor()
        if condition=='':
            cur.execute(f'select distinct {col_name} from {table}')
        else:
            cur.execute(f'select distinct {col_name} from {table} where {condition}')
        names=cur.fetchall()
        values=[]
        for row in names:
            if len(row)>1 and row[1]!='None':
                values.append(row)
            elif row[0]!='None':
                values.append(row[0])
        con.close()
        return (tuple(values),'')
    except Exception as exp:
        return('',exp)

# to test the functions
if __name__=='__main__':
    n_id,err= id_generator('department')
    print(n_id)
    # print(err)

    n,err= find_col_vals('name','department')
    print(n)

    n,err= find_col_vals('id, name','employees','department= "Cardiology"')
    print(n,type(n))