import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from numpy import genfromtxt
from ttkbootstrap import Style
 # DEBUG remove Frame later V
from ttkbootstrap.widgets import Button, Treeview, Frame
import database_handler as database_handler
import matplotlib.pyplot as plt
import sys
import datetime
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

  #CC rebrand modelling with analysis
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

  def close_plot():
    plt.close()

  def draw_plot():
    #first, remove existing plot
    close_plot()

    x_axis = x_axis_column_name.get()
    y_axis = y_axis_column_name.get()
    z_axis = z_axis_column_name.get()

    # CC add error msgs everywhere in code
    # without z-axis
    if x_axis != "unspecified" and y_axis != "unspecified" and z_axis == "unspecified":
      inventory_data = database_handler.retrieve_via_sql_query(str(x_axis + "," + y_axis), "inventory")
      x_axis_list = [inventory_data[i][0] for i in range(0,len(inventory_data))]
      y_axis_list = [inventory_data[i][1] for i in range(0,len(inventory_data))]

      ax = plt.axes()
      ax.plot(x_axis_list, y_axis_list, marker = 'x')
      ax.set_title(x_axis + " vs " + y_axis)
      ax.set_xlabel(x_axis)
      ax.set_ylabel(y_axis)

      plt.show()
    # with z-axis
    elif x_axis != "unspecified" and y_axis != "unspecified" and z_axis != "unspecified":
      inventory_data = database_handler.retrieve_via_sql_query(str(x_axis + "," + y_axis + "," + z_axis), "inventory")
      x_axis_list = [inventory_data[i][0] for i in range(0,len(inventory_data))]
      y_axis_list = [inventory_data[i][1] for i in range(0,len(inventory_data))]
      z_axis_list = [inventory_data[i][2] for i in range(0,len(inventory_data))]

      # checking if type is string as need to treat them diffenently in plot
      x_axis_type_string = False
      y_axis_type_string = False
      z_axis_type_string = False

      if isinstance(x_axis_list[0], str) == True:
        x_axis_type_string = True
        x_plot_data = range(len(x_axis_list))
      else:
        x_plot_data = x_axis_list

      if isinstance(y_axis_list[0], str) == True:
        y_axis_type_string = True
        y_plot_data = range(len(y_axis_list))
      else:
        y_plot_data = y_axis_list

      if isinstance(z_axis_list[0], str) == True:
        z_axis_type_string = True
        z_plot_data = range(len(z_axis_list))
      else:
        z_plot_data = z_axis_list

      ax = plt.axes(projection='3d')

      if plot_type.get()[17:] == "Scatter":
        ax.scatter(x_plot_data, y_plot_data, z_plot_data, c= range(len(z_axis_list)), cmap='plasma', marker='x') # colours reqiure numeric data always
      if plot_type.get()[17:] == "Line":
        ax.plot3D(x_plot_data, y_plot_data, z_plot_data)
      # replacing the pseudo-numbers (for string data) in the above statement by actual data if present (required to avoid datatype issues)
      if x_axis_type_string == True:
        ax.set(xticks=range(len(x_axis_list)), xticklabels=x_axis_list)

      if y_axis_type_string == True:
        ax.set(yticks=range(len(y_axis_list)), yticklabels=y_axis_list)

      if z_axis_type_string == True:
        ax.set(zticks=range(len(z_axis_list)), zticklabels=z_axis_list)

      ax.set_title(x_axis + " vs " + y_axis + " vs " + z_axis)
      ax.set_xlabel(x_axis, labelpad=20)
      ax.set_ylabel(y_axis, labelpad=20)
      ax.set_zlabel(z_axis, labelpad=20)

      plt.show()

  def toggle_plot_type():
    plot_type_list = ["Scatter","Line"]
    current_index = plot_type_list.index(plot_type.get()[17:])

    # CC clean up logic below V
    if current_index == len(plot_type_list) - 1:
      current_index = -1
    current_index += 1

    plot_type.set("📈 3D Graph type: " + plot_type_list[current_index])

  def set_x_axis():
    # retriving the column list
    # CC make the information common in all three functions into one
    table_information = database_handler.retrieve_headers("inventory")
    column_list = []
    for i in range(0,len(table_information)):
      column_list.append(table_information[i][0])

    # finding current index
    current_column = x_axis_column_name.get()
    try:
      current_column_index = column_list.index(current_column)
    except:
      #CC add a msg for x axis not set yet (right now, it just sts it to -1 then +1 below so sets to the zeroth position)
      current_column_index = -1

    #in case at the last column
    if current_column_index + 1 == len(column_list):
      current_column_index = -1

    x_axis_column_name.set(column_list[current_column_index + 1])

    #formating the text
    if len(x_axis_column_name.get()) < 25:
      x_axis.set("Set Graph's X-Axis:\n" + x_axis_column_name.get())
    else:
      x_axis.set("Set Graph's X-Axis:\n" + x_axis_column_name.get()[0:22] + "...")

  def set_y_axis():
    # retriving the column list
    table_information = database_handler.retrieve_headers("inventory")
    column_list = []
    for i in range(0,len(table_information)):
      column_list.append(table_information[i][0])

    # finding current index
    current_column = y_axis_column_name.get()
    try:
      current_column_index = column_list.index(current_column)
    except:
      #CC add a msg for x axis not set yet (right now, it just sts it to -1 then +1 below so sets to the zeroth position)
      current_column_index = -1

    #in case at the last column
    if current_column_index + 1 == len(column_list):
      current_column_index = -1

    y_axis_column_name.set(column_list[current_column_index + 1])

    #formating the text
    if len(y_axis_column_name.get()) < 25:
      y_axis.set("Set Graph's Y-Axis:\n" + y_axis_column_name.get())
    else:
      y_axis.set("Set Graph's Y-Axis:\n" + y_axis_column_name.get()[0:22] + "...")

  def set_z_axis():
    # retriving the column list
    table_information = database_handler.retrieve_headers("inventory")
    column_list = []
    for i in range(0,len(table_information)):
      column_list.append(table_information[i][0])

    #as 3d plotting is optional,
    column_list.append("unspecified")

    # finding current index
    current_column = z_axis_column_name.get()
    try:
      current_column_index = column_list.index(current_column)
    except:
      #CC add a msg for x axis not set yet (right now, it just sts it to -1 then +1 below so sets to the zeroth position)
      current_column_index = -1

    #in case at the last column
    if current_column_index + 1 == len(column_list):
      current_column_index = -1

    z_axis_column_name.set(column_list[current_column_index + 1])

    #formating the text
    if len(z_axis_column_name.get()) < 25:
      z_axis.set("Set Graph's Z-Axis:\n" + z_axis_column_name.get())
    else:
      z_axis.set("Set Graph's Z-Axis:\n" + z_axis_column_name.get()[0:22] + "...")

  def tabularise_full_inventory_database():
    # temp table soln
    headers = database_handler.retrieve_headers("inventory")
    column_list = []
    for i in range(0,len(headers)):
      header_name = headers[i][0][5:]
      if "manufacturer_" in header_name:
        header_name = "Manf. " + header_name[13:]
      column_list.append(header_name)

    full_data = database_handler.retrieve_via_sql_query("*","inventory")

    ax = plt.axes()
    ax.axis('off') # hide axis
    colour_list = tuple("0.8" for i in range(len(column_list)))
    full_inventory_database_table = ax.table(cellText = full_data, colLabels = column_list, colColours = colour_list, loc = 'center')
    full_inventory_database_table.auto_set_font_size(False)
    full_inventory_database_table.set_fontsize(10)
    full_inventory_database_table.scale(1.2,1)
    plt.show()


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

  debug_label2 = tk.Label(order_models_view, text = "   ▭▭▪▣▓ ▒ ░ Temp Orders View Placeholder ░ ▒ ▓▣▪▭▭   ", relief = "ridge", font = "TkFixedFont")# DEBUG
  debug_label2.grid(row = 0) # DEBUG
  # inventory plotter section
  graph_plotter_label = tk.Label(inventory_models_view, text = " ▪▣▓ ▒ ░ Graph Plotter ░ ▒ ▓▣▪ ", relief = "ridge")
  graph_plotter_label.grid(row = 0,
                           column = 0
                           )

  x_axis = tk.StringVar()
  x_axis_column_name = tk.StringVar() # CC place it like in modelling view (cleanup)
  set_x_axis_button = tk.Button(inventory_models_view,
                                 textvariable = x_axis,
                                 command = set_x_axis
                                 )
  set_x_axis_button.grid(row = 1,
                        column = 0,
                        pady = 2,
                        sticky = "nsew"
                        )
  x_axis_column_name.set("unspecified")
  x_axis.set("Set Graph's X-Axis:\n" + x_axis_column_name.get())

  y_axis = tk.StringVar()
  y_axis_column_name = tk.StringVar() # CC place it like in modelling view (cleanup)
  set_y_axis_button = tk.Button(inventory_models_view,
                                 textvariable = y_axis,
                                 command = set_y_axis
                                 )
  set_y_axis_button.grid(row = 2,
                        column = 0,
                        pady = 2,
                        sticky = "nsew"
                        )
  y_axis_column_name.set("unspecified")
  y_axis.set("Set Graph's Y-Axis:\n" + y_axis_column_name.get())

  z_axis = tk.StringVar()
  z_axis_column_name = tk.StringVar() # CC place it like in modelling view (cleanup)
  set_z_axis_button = tk.Button(inventory_models_view,
                                 textvariable = z_axis,
                                 command = set_z_axis
                                 )
  set_z_axis_button.grid(row = 3,
                        column = 0,
                        pady = 2,
                        sticky = "nsew"
                        )
  z_axis_column_name.set("unspecified")
  z_axis.set("Set Graph's Z-Axis:\n" + z_axis_column_name.get())

  plot_button_frame = tk.Frame(inventory_models_view)
  plot_button_frame.grid(row = 4,
                            column = 0,
                            sticky = "nsew"
                            )

  scatter_plot_button = Button(plot_button_frame,
                                 text = "📊 Plot Graph",
                                 command = draw_plot,
                                 bootstyle = "warning-outline"
                                 )
  scatter_plot_button.grid(row = 0,
                        column = 0,
                        padx = 2,
                        pady = 5
                        )

  graph_close_button = Button(plot_button_frame,
                                 text = "Close Graph",
                                 command = close_plot,
                                 bootstyle = "success-outline"
                                 )
  graph_close_button.grid(row = 0,
                          column = 1,
                          padx = 2,
                          pady = 5
                          )

  plot_type = tk.StringVar()
  plot_type_button = tk.Button(inventory_models_view,
                                 textvariable = plot_type,
                                 command = toggle_plot_type
                                 )
  plot_type_button.grid(row = 5,
                        column = 0,
                        sticky = "nsew"
                        )
  plot_type.set("📈 3D Graph type: Scatter")

  date_frame = tk.Frame(inventory_models_view)
  date_frame.grid(row = 6,
                  column = 0,
                  pady = 5,
                  sticky = "nsew",
                  )

  day_month_year_label = tk.Label(date_frame, text = " Date | Month | Year ", relief = "groove") # DEBUG CC change text later
  day_month_year_label.grid(row = 0,
                            columnspan = 3,
                            pady = 2,
                            sticky = "nsew"
                            )

  current_date = datetime.date.today()
  day_label = tk.Label(date_frame,
                       text = str(current_date)[8:],
                       relief = "raised",
                       width = 8
                       )
  day_label.grid(row = 1,
                 column = 0,
                 padx = 1,
                 sticky = "nsew"
                 )

  month_label = tk.Label(date_frame,
                         text = str(current_date)[5:7],
                         relief = "raised",
                         width = 8
                         )
  month_label.grid(row = 1,
                  column = 1,
                  padx = 4,
                  sticky = "nsew"
                  )

  year_label = tk.Label(date_frame,
                        text = str(current_date)[0:4],
                        relief = "raised",
                        width = 8
                        )
  year_label.grid(row = 1,
                  column = 2,
                  padx = 1,
                  sticky = "nsew"
                  )

  inventory_response_message = tk.StringVar()
  inventory_response_message_board = tk.Label(inventory_models_view, textvariable = inventory_response_message, relief = "groove") # CC standardardise relief
  inventory_response_message_board.grid(row = 0,
                                        column = 1,
                                        padx = 3,
                                        pady = 2,
                                        rowspan = 2,
                                        sticky = "nsew"
                                        )
  inventory_response_message.set("     Action status will be displayed here:     \n\n") # CC add msgs CC make pretty?

  full_inventory_database_viewer_button = Button(inventory_models_view,
                                                 text = "Full inventory database",
                                                 command = tabularise_full_inventory_database,
                                                 bootstyle = "warning"
                                                 )
  full_inventory_database_viewer_button.grid(row = 2,
                                             column = 1,
                                             padx = 3,
                                             pady = 2,
                                             sticky = "nsew"
                                             ) # CC standardise pady in inventory models view

  inventory_models_view.tkraise()

  # Sets initial frame to be home_view
  home_view.tkraise()

  root.mainloop()
