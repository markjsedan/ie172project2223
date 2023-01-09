import apps.dbconnect as db
from datetime import datetime

def addemployeestable():
    sqlcode = """ CREATE TABLE employees(
        emp_id serial primary key not null,
        emp_name varchar(256),
        emp_role varchar(256),
        emp_email varchar (256),
	    emp_contact_num varchar (256),
        emp_modified_date timestamp without time zone default now(),
        emp_delete_ind bool default false
    )
    """
addemployeestable()

# def addfewgenres():
#     sqlcode = """ INSERT INTO genres (
#         genre_name,
#         genre_modified_date,
#         genre_delete_ind
#     )
#     VALUES (%s, %s, %s)"""

#     db.modifydatabase(sqlcode,['Academic', datetime.now(), False])
#     db.modifydatabase(sqlcode,['Children', datetime.now(), False])
#     db.modifydatabase(sqlcode,['Fiction', datetime.now(), False])
#     db.modifydatabase(sqlcode,['Lifestyle', datetime.now(), False])
#     db.modifydatabase(sqlcode,['Nonfiction', datetime.now(), False])


# def addfewcustomers():
#     sqlcode = """ INSERT INTO customers_individuals (
#         cust_ind_id,
#         cust_ind_name,
#         cust_ind_prof,
#         cust_ind_email,
#         cust_ind_contact_num,
#         cust_ind_address,
#         cust_ind_modified_date,
#         cust_ind_delete_ind
#     )
#     VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"""

#     db.modifydatabase(sqlcode, ["1",'Mark Jay Sedan',"Student","mosedan@up.edu.ph","09159665941","Ipil Residence Hall, Quezon City",datetime.now(), False])
#     db.modifydatabase(sqlcode, ["2",'Marc Justin Vergara',"Teacher","mpvergara2@up.edu.ph","09123456789","Batangas City",datetime.now(), False])

# addfewcustomers()

# sql_resetgenres = """
#     TRUNCATE TABLE genres RESTART IDENTITY CASCADE
# """
# db.modifydatabase(sql_resetgenres, [])
# addfewgenres()

# sql_query = """ SELECT * FROM customers_individuals"""
# values = []
# columns = ['cust_ind_id',
#         'cust_ind_name',
#         'cust_ind_prof',
#         'cust_ind_email',
#         'cust_ind_contact_num',
#         'cust_ind_address',
#         'cust_ind_modified_date',
#         'cust_ind_delete_ind']
# df = db.querydatafromdatabase(sql_query, values, columns) # or print(db.querydatafromdatabase(sql_query, values, columns))
# print(df)



# def addfewbooks():
#     sqlcode = """ INSERT INTO books (
#         bk_id,
#         bk_title,
#         genre_id,
#         au_id,
#         pub_id,
#         bk_pb_yr,
#         bk_price,
#         bk_inv_count,
#         bk_modified_date,
#         bk_delete_ind
#     )
#     VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

#     db.modifydatabase(sqlcode, ["1",'Mark Jay Sedan',"Student","mosedan@up.edu.ph","09159665941","Ipil Residence Hall, Quezon City",datetime.now(), False])
#     db.modifydatabase(sqlcode, ["2",'Marc Justin Vergara',"Teacher","mpvergara2@up.edu.ph","09123456789","Batangas City",datetime.now(), False])

# addfewbooks()

# sql_resetgenres = """
#     TRUNCATE TABLE genres RESTART IDENTITY CASCADE
# """
# db.modifydatabase(sql_resetgenres, [])
# addfewgenres()

# sql_query = """ SELECT * FROM customers_individuals"""
# values = []
# columns = ['cust_ind_id',
#         'cust_ind_name',
#         'cust_ind_prof',
#         'cust_ind_email',
#         'cust_ind_contact_num',
#         'cust_ind_address',
#         'cust_ind_modified_date',
#         'cust_ind_delete_ind']
# df = db.querydatafromdatabase(sql_query, values, columns) # or print(db.querydatafromdatabase(sql_query, values, columns))
# print(df)