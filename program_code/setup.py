
# Only run once on initialisation

def initialise_tables(cursor):
  # Working under databases called main_database and plot_database
  cursor.execute("CREATE DATABASE IF NOT EXISTS main_database")

  cursor.execute("USE main_database")
  # margin, discount is in percentages and number is in varchar to handle leading zeros
  cursor.execute("DROP TABLE IF EXISTS inventory;") # Handles setup being run more than once
  cursor.execute("""CREATE TABLE main_database.inventory
                  (
                      item_id int(10) not null AUTO_INCREMENT,
                      item_name varchar(20) not null,
                      item_cost decimal(8,2) not null,
                      item_gst decimal(8,2) not null,
                      item_discount decimal(5,2) not null,
                      item_final_cost decimal(8,2) not null,
                      item_margin decimal(5,2) not null,
                      item_stock int(10) not null,
                      item_manufacturer_name varchar(40) not null,
                      item_manufacturer_incharge varchar(20) not null,
                      item_manufacturer_contact_no varchar(10) not null,
                      PRIMARY KEY (item_id)
                  );""")
  # Debug
  cursor.execute("""INSERT INTO inventory (item_name,item_cost,item_gst,item_discount,item_final_cost,item_margin,item_stock,item_manufacturer_name,item_manufacturer_incharge,item_manufacturer_contact_no)
                 VALUES
                 ("Apples",139.00,10.00,5.00,122.55,50.00,500,"APPLE","Tim Cook","0999666333"),
                 ("Raspberry",139.00,10.00,5.00,122.55,50.00,500,"RASPBERRY PI","Eben Upton","0111222333"),
                 ("Orange",139.00,10.00,5.00,122.55,50.00,500,"ORANGE PI","Zhao Yifan","0555666777"),
                 ("Bannana",139.00,10.00,5.00,122.55,50.00,500,"BANNANA PI","U.N. Owen","0333444555"),
                 ("Potato",139.00,10.00,5.00,122.55,50.00,500,"LE POTATO LIBRE","W.H. Onos","0777888999");
                 """) # Debug
  cursor.execute('commit')


  # discount is in percentages and number is in varchar to handle leading zeros
  cursor.execute("DROP TABLE IF EXISTS orders;") # Handles setup being run more than once
  cursor.execute("""CREATE TABLE main_database.orders
                  (
                      order_id int(10) not null AUTO_INCREMENT,
                      order_item_name varchar(20) not null,
                      order_date date not null,
                      order_initial_cost decimal(8,2) not null,
                      order_gst decimal(8,2) not null,
                      order_discount decimal(5,2) not null,
                      order_final_cost decimal(8,2) not null,
                      order_quantity int(10) not null,
                      order_customer_name varchar(20) not null,
                      order_customer_contact_no varchar(10),
                      PRIMARY KEY (order_id)
                  );""")

  # Debug
  cursor.execute("""INSERT INTO orders (order_item_name,order_date,order_initial_cost,order_gst,order_discount,order_final_cost,order_quantity,order_customer_name,order_customer_contact_no)
                 VALUES
                 ("Apples","2025-04-08",139.00,10.00,5.00,122.55,1,"Tom Bakes","1999666333"),
                 ("Raspberry","2025-04-08",139.00,10.00,5.00,122.55,1,"Nebe Downton","1111222333"),
                 ("Orange","2025-04-08",139.00,10.00,5.00,122.55,1,"Zhao Yistan","1555666777"),
                 ("Bannana","2025-04-08",139.00,10.00,5.00,122.55,1,"K.N. Owen","1333444555"),
                 ("Potato","2025-04-08",139.00,10.00,5.00,122.55,1,"W.E. Noe","1777888999");
                 """) # Debug
  cursor.execute('commit')
