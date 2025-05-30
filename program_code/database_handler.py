# Requires MqSQL connector
import mysql.connector as conn
import setup as setup
import sys # to exit the program

conn_obj = "" # this is used to create the connection to mysql via enter_mysql()

def enter_mysql():
    global conn_obj

    correct_credentials = False
    while correct_credentials != True:
        try:
            user_name = str(input("Please enter your MySQL username: "))
            user_password = str(input("Please enter your MySQL password: "))
            user_host = str(input("Please enter MySQL host: ('localhost' if using localhost): "))
            user_port = str(input("Please enter MySQL port: ('n' if using localhost): "))
            print("Attempting connection...")

            if user_port == 'n':
                conn_obj = conn.connect(host = user_host, user = user_name, passwd = user_password)
            else:
                conn_obj = conn.connect(host = user_host, port = user_port, user = user_name, passwd = user_password)

            correct_credentials = True
        except:
            exit_program = input("There was a mistake with the username, password or port; Please any key to try again (or 'q' to quit) \n")
            if exit_program == "q":
                sys.exit(1) # exits program


    if conn_obj.is_connected() == True:
        print("Connected successfully")

    cursor = conn_obj.cursor()
    setup.initialise_tables(cursor)
    cursor.close() # CC Remember to close the connection later as well

def import_items(values):

    # values is a list of tuples; each tuple describes an item in the format: (item_name,item_cost,item_gst,item_discount,item_final_cost,item_margin,item_stock,item_manufacturer_name,item_manufacturer_incharge,item_manufacturer_contact_no)
    command = """INSERT INTO inventory (item_name,item_cost,item_gst,item_discount,item_final_cost,item_margin,item_stock,item_manufacturer_name,item_manufacturer_incharge,item_manufacturer_contact_no)
                VALUES
            """

    for i in values:
        command += str(i) + ","

    command = command[:-1] + ";" # as last element ends with colon not comma

    cursor = conn_obj.cursor()
    cursor.execute("USE main_database")
    cursor.execute("DELETE FROM inventory")
    cursor.execute("ALTER TABLE inventory AUTO_INCREMENT = 1")
    cursor.execute(command)
    cursor.execute("commit")
    cursor.close()

def import_orders(values):

    # values is a list of tuples; each tuple describes an order in the format: (order_item_name,order_initial_cost,order_gst,order_discount,order_final_cost,order_quantity,order_customer_name,order_customer_contact_no)
    command = """INSERT INTO orders (order_item_name,order_date,order_initial_cost,order_gst,order_discount,order_final_cost,order_quantity,order_customer_name,order_customer_contact_no)
                 VALUES
              """

    for i in values:
        command += str(i) + ","

    command = command[:-1] + ";" # as last element ends with colon not comma

    cursor = conn_obj.cursor()
    cursor.execute("USE main_database")
    cursor.execute("DELETE FROM orders")
    cursor.execute("ALTER TABLE orders AUTO_INCREMENT = 1")
    cursor.execute(command)
    cursor.execute("commit")
    cursor.close()

def retrieve_via_sql_query(sql_select, sql_from, sql_where = "",sql_database = "main_database"):
    command = "SELECT " + sql_select + "\n"

    if sql_where == "":
        command += "FROM " + sql_from + ";" # if no where clause specified
    else:
        command += "FROM " + sql_from + "\n"
        command += "WHERE " + sql_where + ";"

    cursor = conn_obj.cursor()
    cursor.execute("USE " + sql_database + ";")
    cursor.execute(command)

    data = cursor.fetchall()

    cursor.execute("commit")
    cursor.close()

    return(data)

def save_plot_data(plot_data,plot_type):

    # plot types denotes which table it will save in (example: name_cost_plots) whereas the plot_data is the plot's png from BYTESIO
    command = "INSERT INTO " + plot_type + " (plot_data)\nVALUES (%s);"

    cursor = conn_obj.cursor()
    cursor.execute("USE plot_database")
    cursor.execute(command,[plot_data])
    cursor.execute("commit")
    cursor.close()