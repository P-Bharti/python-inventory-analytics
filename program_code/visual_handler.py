import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from numpy import genfromtxt
from ttkbootstrap import Style
 # DEBUG remove Frame later V
from ttkbootstrap.widgets import Button, Treeview, Frame
import database_handler as database_handler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import sys
# fix order ^ to make more sense

# CC bring back all the formatting cc's that i removed after formatting in the middle

def run_GUI():
  # all window definitions
  root = tk.Tk()
  root.title("Python Inventory Analytics")
  root.geometry("660x365")
  root.resizable(False, False)
  root.protocol('WM_DELETE_WINDOW', sys.exit)


  home_view = tk.Frame(root)
  home_view.grid(row = 1, column = 1, sticky = 'news')

  modelling_view = tk.Frame(root)
  modelling_view.columnconfigure(0,weight = 1)
  modelling_view.rowconfigure(1, weight = 1)
  modelling_view.grid(row = 1, column = 1, sticky = 'news')

  # setting style
  style = Style("solar")

  # functions for home view
  def populate_data():
   # removing response message if any
   response_message.set("")

   # inventory viewer
   inventory_data = database_handler.retrieve_via_sql_query("item_id,item_name,item_cost,item_final_cost,item_stock","inventory")

   inventory_viewer = Treeview(inventory_tab,
                               columns = ("item_id","item_name","item_cost","item_final_cost","item_stock"),
                               show = 'headings',
                               height = 13,
                               bootstyle = 'success'
                               )
   inventory_viewer.grid(row = 1,
                         column = 0,
                         sticky = "e"
                         )

   # creating the scrollbar
   scrollbar = ttk.Scrollbar(inventory_tab, orient = "vertical", command = inventory_viewer.yview)
   scrollbar.grid(row = 1,
                  column = 1,
                  sticky = "nsew"
                  )
   inventory_viewer.configure(yscrollcommand = scrollbar.set)

   # initialising columns
   inventory_viewer.column("item_id", anchor = "center", width = 45)
   inventory_viewer.heading('item_id', text = 'S.No')

   inventory_viewer.column("item_name", anchor = "center", width = 75)
   inventory_viewer.heading('item_name', text = 'Name')

   inventory_viewer.column("item_cost", anchor = "center", width = 55)
   inventory_viewer.heading('item_cost', text = 'Cost')

   inventory_viewer.column("item_final_cost", anchor = "center", width = 55)
   inventory_viewer.heading('item_final_cost', text = 'Total')

   inventory_viewer.column("item_stock", anchor = "center", width = 50)
   inventory_viewer.heading('item_stock', text = 'Stock')

   inventory_viewer.grid(row = 1, column = 0)

   # insert values into inventory_viewer
   for i in inventory_data:
     inventory_viewer.insert(parent = '', index = tk.END, values = i)

   # orders viewer code
   orders_data = database_handler.retrieve_via_sql_query("order_id,order_item_name,order_customer_name,order_final_cost,order_quantity","orders")

   orders_viewer = Treeview(orders_tab,
                            columns = ("order_id","order_item_name","order_customer_name","order_final_cost","order_quantity"),
                            show = 'headings',
                            height = 13,
                            bootstyle = 'success'
                            )
   orders_viewer.grid(row = 1,
                      column = 0,
                      sticky = "e"
                      )

   # creating the scrollbar
   scrollbar = ttk.Scrollbar(orders_tab, orient = "vertical", command = orders_viewer.yview)
   scrollbar.grid(row = 1,
                  column = 1,
                  sticky = "nsew"
                  )
   orders_viewer.configure(yscrollcommand = scrollbar.set)

   # initialising columns
   orders_viewer.column("order_id", anchor = "center", width = 45)
   orders_viewer.heading('order_id', text = 'S.No')

   orders_viewer.column("order_item_name", anchor = "center", width = 75)
   orders_viewer.heading('order_item_name', text = 'Item')

   orders_viewer.column("order_customer_name", anchor = "center", width = 60)
   orders_viewer.heading('order_customer_name', text = 'Name')

   orders_viewer.column("order_final_cost", anchor = "center", width = 55)
   orders_viewer.heading('order_final_cost', text = 'Total')

   orders_viewer.column("order_quantity", anchor = "center", width = 45)
   orders_viewer.heading('order_quantity', text = 'Amt')

   orders_viewer.grid(row = 1, column = 0)

   # insert values into orders_viewer
   for i in orders_data:
     orders_viewer.insert(parent = '', index = tk.END, values = i)

  def import_database():
    if full_inventory_path.get() !=  "" and full_orders_path.get() !=  "":
      try:
        items = genfromtxt(full_inventory_path.get(), delimiter = ",", dtype = None, skip_header = 1, encoding = "utf8")
        database_handler.import_items(items)
      except:
        # error with csv file
        response_message.set("Import Unsuccessful; Please check your CSV")
        spacer.config(fg = "red")
        return None

      try:
        orders = genfromtxt(full_orders_path.get(), delimiter = ",", dtype = None, skip_header = 1, encoding = "utf8")
        database_handler.import_orders(orders)
      except:
        # error with csv file
        response_message.set("Import Unsuccessful; Please check your CSV")
        spacer.config(fg = "red")
        return None

      # if function reaches here, the code was sucessfull
      response_message.set("Import Successful; Please Refresh")
      spacer.config(fg = "green")
    else:
      response_message.set("Import Unsuccessful; Please try again")
      spacer.config(fg = "red")

  def set_inventory_path():
    full_inventory_path.set(tk.filedialog.askopenfilename ())
    temp = full_inventory_path.get()
    inventory_path.set("Inventory path: \n" + temp[:20] + "...")

  def set_orders_path():
    full_orders_path.set(tk.filedialog.askopenfilename())
    temp = full_inventory_path.get()
    orders_path.set("Orders path: \n" + temp[:20] + "...")

  def refresh():
    populate_data()
    draw_name_cost_plot()

  def switch_to_modelling_view():
    modelling_view.tkraise()
  # home view GUI
  database_label = tk.Label(home_view,text = "▭▭▪▣▓ ▒ ░ Database Viewer ░ ▒ ▓▣▪▭▭", relief = "ridge", font = "TkFixedFont")
  database_label.grid(row = 0,
                      column = 0,
                      padx = 10,
                      pady = 10,
                      sticky = "nesw"
                      )

  other_functions_label = tk.Label(home_view, text = ' ▭▣▓ ▒ ░ Other Functions ░ ▒ ▓▣▭ ', relief = "ridge", font = "TkFixedFont")
  other_functions_label.grid(row = 0,
                             column = 1,
                             sticky = "ew"
                             )

  button_frame = tk.Frame(home_view)
  button_frame.grid(row = 1,
                    column = 1,
                    sticky = "nsew"
                    )

  first_row_frame = tk.Frame(button_frame)
  first_row_frame.grid(row = 0,
                       columnspan = 3,
                       pady = 5,
                       sticky = "nsew"
                       )

  modelling_view_button = Button(first_row_frame,
                                 text = "▰▱▰▱▰▰▱▰\n 📊 Modelling \n Viewport \n ▰▱▰▱▰▰▱▰",
                                 command = switch_to_modelling_view,
                                 bootstyle = "primary-outline"
                                 )

  modelling_view_button.grid(row = 0,
                             column = 0,
                             pady = 5,
                             sticky = "e"
                             )

  refresh_database_button = Button(first_row_frame,
                                   text = "▰▱▰▱▰▰▱▰ \n ↻ Refresh \n  Database \n ▰▱▰▱▰▰▱▰",
                                   command = refresh,
                                   bootstyle = "warning-outline"
                                   )

  refresh_database_button.grid(row = 0,
                               column = 1,
                               padx = 5,
                               pady = 5,
                               sticky = "nsew"
                               )


  full_inventory_path = tk.StringVar()
  full_orders_path = tk.StringVar()

  import_database_button = Button(first_row_frame,
                                  text = "▰▱▰▱▰▰▱▰ \n 🗎 Import \n Database \n ▰▱▰▱▰▰▱▰",
                                  command = import_database,
                                  bootstyle = "success-outline"
                                  )

  import_database_button.grid(row = 0,
                              column = 2
                              )

  inventory_path = tk.StringVar()
  inventory_path_button = tk.Button(button_frame,
                                    textvariable = inventory_path,
                                    command = set_inventory_path,
                                    font = "TkFixedFont",
                                    height = 3
                                    )
  inventory_path.set("Set inventory path")

  inventory_path_button.grid(row = 1,
                             columnspan = 3,
                             sticky = "nsew"
                             )

  orders_path = tk.StringVar()
  orders_path_button = tk.Button(button_frame,
                                 textvariable = orders_path,
                                 command = set_orders_path,
                                 font = "TkFixedFont",
                                 height = 3
                                 )
  orders_path.set("Set orders path")

  orders_path_button.grid(row = 2,
                          columnspan = 3,
                          sticky = "nsew"
                          )

  response_message = tk.StringVar()
  spacer = tk.Label(button_frame,textvariable = response_message, relief = "raised")
  spacer.grid(row = 3,
              columnspan = 3,
              pady = 5,
              sticky = "nsew"
              )
  response_message.set("")

  exit_button = tk.Button(button_frame,
                          text = "▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱ \nQuit Python-Inventory-Analytics\n ▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱",
                          command = sys.exit,
                          font = "TkFixedFont",
                          height = 2
                          )
  exit_button.grid(row = 4,
                   columnspan = 3,
                   sticky = "ew"
                   )

  # Notebook to contain the two tables in our database
  table_frame = tk.Frame(home_view)
  table_frame.grid(row = 1,
                   column = 0,
                   sticky = "nsew"
                   )

  # Each column must take equal amount of space
  table_frame.rowconfigure(0, weight = 1)
  table_frame.rowconfigure(1, weight = 1)
  table_frame.rowconfigure(2, weight = 1)

  tables_notebook = ttk.Notebook(table_frame)
  tables_notebook.grid(row = 1,
                       padx = 10
                       )

  inventory_tab =  tk.Frame(tables_notebook)
  tables_notebook.add(inventory_tab, text =  "    Inventory    ")

  orders_tab =  tk.Frame(tables_notebook)
  tables_notebook.add(orders_tab, text =  "    Orders    ")

  populate_data()


  # functions for modelling view GUI
  def switch_to_home_view():
    home_view.tkraise()

  def switch_to_inventory_models_view():
    inventory_models_view.tkraise()

  def switch_to_order_models_view():
    order_models_view.tkraise()

  def draw_name_cost_plot(save_plot = False):
      inventory_data = database_handler.retrieve_via_sql_query("item_name,item_cost", "inventory")
      item_name_list = [inventory_data[i][0] for i in range(0,len(inventory_data))]
      item_cost_list = [inventory_data[i][1] for i in range(0,len(inventory_data))]

      fig, ax = plt.subplots(figsize=(4, 3))
      ax.plot(item_name_list, item_cost_list, marker='x')
      ax.set_title("Item vs Cost")

      # CC see if we can implement V (clutters the view at the moment)
      # ax.set_xlabel("Item Name")
      # ax.set_ylabel("Item Cost")
      # fig.autofmt_xdate()

      canvas = FigureCanvasTkAgg(fig, master = inventory_models_view)
      canvas.get_tk_widget().grid(row = 0,
                                 column = 0,
                                 padx = 5,
                                 pady = 7,
                                 sticky = "nsew"
                                 )
      canvas.draw()

      # CC in db_hander add this as a function in another table and make allow comparing possible

      # data_pairs = list(zip(item_cost_list, item_name_list))
      if save_plot == True:
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0) # resetting the pointer to the start of the byte stream again so that we can recall the data later

        database_handler.save_plot_data(img_buffer.getvalue(),"name_cost_plots")

  def save_plot():
    draw_name_cost_plot(True) # refreshs the plot and saves it

  # modelling view GUI
  title_row = tk.Frame(modelling_view)
  title_row.columnconfigure(0, weight = 1) # centering
  title_row.columnconfigure(1, weight = 0)
  title_row.columnconfigure(2, weight = 1)


  title_row.grid(row = 0,
                 columnspan = 3,
                 sticky = "nsew"
                 )

  inventory_view_button = Button(title_row,
                                 text = "Inventory",
                                 command = switch_to_inventory_models_view,
                                 bootstyle = "warning-outline"
                                 )
  inventory_view_button.grid(row = 0,
                             column = 0
                             )

  order_view_button = Button(title_row,
                             text = "Orders",
                             command = switch_to_order_models_view,
                             bootstyle = "success-outline"
                             )
  order_view_button.grid(row = 0,
                        column = 1
                        )

  title_label = tk.Label(title_row, text = "       ▭▭▪▣▓ ▒ ░ Modelling View ░ ▒ ▓▣▪▭▭       ", relief = "ridge", font = "TkFixedFont")
  title_label.grid(row = 0,
                   column = 2
                   )

  back_button = Button(title_row,
                       text = "Back",
                       command = switch_to_home_view,
                       bootstyle = "primary-outline"
                       )
  back_button.grid(row = 0,
                   column = 3,
                   pady = 5
                   )

  # padx = (10,0) pads only on left side
  inventory_models_view = tk.Frame(modelling_view)
  inventory_models_view.grid(row = 1,
                             columnspan = 2,
                             padx = (10,0),
                             sticky = "nsew"
                             )

  # padx = (10,0) pads only on left side
  order_models_view = Frame(modelling_view, bootstyle = "success") # DEBUG Frame instead of tk.frame
  order_models_view.grid(row = 1,
                         columnspan = 2,
                         padx = (10,0),
                         sticky = "nsew"
                         )

  debug_label2 = tk.Label(order_models_view, text = "   ▭▭▪▣▓ ▒ ░ Temp Orders View Placeholder░░ ▒ ▓▣▪▭▭   ", relief = "ridge", font = "TkFixedFont")# DEBUG
  debug_label2.grid(row = 0) # DEBUG

  inventory_models_view.tkraise()

  # inventory viewer
  draw_name_cost_plot()

  # CC add functionallity later
  save_plot_button = tk.Button(inventory_models_view,
                               text = "▰▱▰▱▰▰▱▰ \n 🗎 Save Plot \n ▰▱▰▱▰▰▱▰",
                               command = save_plot)
  save_plot_button.grid(row = 0,
                        column = 1,
                        padx = 5)




  # Sets initial frame to be home_view
  home_view.tkraise()

  root.mainloop()
