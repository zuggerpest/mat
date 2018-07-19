import datetime
import calendar
import tkinter as tk
from tkinter import ttk
import hud as Hud
from customer import Customer
from database import Database
from projects import Projects
from tasks import Tasks
from tkcalendar import Calendar
from tkcalendar import DateEntry

current_customer = Customer('', '', '', '', '', '', '', '')
current_project = Projects('', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
current_task = Tasks('', '', '', '', '', '', '', '')
task_frame_count = []


LARGE_FONT = ('Verdaba', 12)
def convert_date_postgres(date_to_conv,I_or_O):
    # if I prepare for input, if O prepare for output
    if I_or_O.lower() == 'i':
        year_to = date_to_conv[6:10]
        month_to = date_to_conv[3:5]
        day_to = date_to_conv[0:2]
        iso = f'{year_to}-{month_to}-{day_to}'
        return iso

    if I_or_O.lower() == 'o':
        #30/04/1988
        #1988-04-30
        year_to = date_to_conv[0:4]
        month_to = date_to_conv[5:7]
        day_to = date_to_conv[8:10]
        iso = f'{day_to} {month_to} {year_to}'
        return iso

def format_day_tasks(date):
    '''
    make the date into a nice format to read
    #TODO make the reutrn a color, if overdue or in emidiate future

    :param date:
    :return: the date in a short format, ie today, tmorrow yesterday or day and month
    '''
    #get current date and compate it to the date input
    current_date = datetime.datetime.now()
    current_date = datetime.datetime.strftime(current_date,'%d %m %Y')
    cd_year = int(current_date[6:10])
    cd_month = int(current_date[3:5])
    cd_day = int(current_date[0:2])
    # task_date = convert_date_postgres(date,'i')
    task_date = date
    td_year = int(task_date[6:10])
    td_month = int(task_date[3:5])
    td_day = int(task_date[0:2])

    #convert dates to python format
    cd_python = datetime.datetime.strptime(f'{cd_day} {cd_month} {cd_year}','%d %m %Y')
    td_python = datetime.datetime.strptime(f'{td_day} {td_month} {td_year}','%d %m %Y')

    #if it is today
    if current_date == task_date:
        return ('Today')

    if td_year == cd_year: # dont check month as if week and year same
        if td_day-1 == cd_day or td_day+1 == cd_day:
            if cd_python.strftime('%W') == td_python.strftime('%W'): # W meams the week numbeer starting on monday
                if td_day-1 == cd_day:
                    return 'Tomorrow'
                elif td_day+1 == cd_day:
                    return 'Yesterday'

            if td_day > cd_day:
                return (td_python.strftime('%A'))

        elif td_month >= cd_month and td_day >= cd_month:
            return (f"{td_python.strftime('%d')} {td_python.strftime('%b')}")

        else:
            return (f"{td_python.strftime('%d')} {td_python.strftime('%b')}")
    else:
        return (f"{td_python.strftime('%d')} {td_python.strftime('%b')} {td_python.strftime('%y')}")

class MatrixCrmApp(tk.Tk):
    Database.initialise(user='postgres', password='StugerPest**', database='Matrix_CRM_1', host='localhost')

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # make title of the program and change the icon
        tk.Tk.wm_title(self, 'Matrix CPRM!')
        tk.Tk.iconbitmap(self, r"C:\Users\Tom\PycharmProjects\tkinter_matrix_1.0\logo.ico")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)  # 0 is for minimun size
        container.grid_columnconfigure(0, weight=1)

# create menu's for all pages

        menu_bar = tk.Menu(container)

        hud = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='H.U.D', menu=hud)
        hud.add_command(label='Open H.U.D', command=lambda: self.show_frame(HomePage))
        hud.add_command(label="List today's task's", command=Hud.list_todays_tasks)

        customer_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Customers', menu=customer_menu)
        customer_menu.add_command(label='Customers ', command=lambda: self.show_frame(CustomersPage))

        projects_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Projects', menu=projects_menu)
        projects_menu.add_command(label='Projects', command=lambda: self.show_frame(ProjectsPage))

        task_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Tasks', menu=task_menu)
        task_menu.add_command(label='Tasks', command=lambda: self.show_frame(TaskPage))

        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}
        for F in (HomePage, CustomersPage, ProjectsPage, TaskPage): # add the pages into here
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        app_tile_lable = tk.Label(self, text='Matrix Customer and Project manager', font=LARGE_FONT)
        app_tile_lable.pack(padx=10, pady=10)

        # create button that wil list customers

        load_customers_button = tk.Button(self, text='display 10 active customers',
                                          command=lambda: Hud.return_top_customers(self))
        load_customers_button.pack()


class CustomersPage(tk.Frame):
    def __init__(self, parent, controler):
        tk.Frame.__init__(self, parent)

        # section for header info, about active customer and active project
        active_project_lable = tk.Label(self, text=f'Customer: <{current_customer.name}>')
        active_project_lable.grid(row=0, column=0)

        # make a Notebook to house find customer, add customer, active custoemrs and top custoemrs

        cust_note = ttk.Notebook(self)
        find_cust_frame = ttk.Frame(cust_note)
        add_cust_frame = ttk.Frame(cust_note)
        cust_note.add(find_cust_frame, text='Find Customer')
        cust_note.add(add_cust_frame, text='Add Customer')

        # add customer labels and entrys to the add_cust_frame

        customer_name_label = tk.Label(add_cust_frame, text='Customer Name: ')
        customer_name_entry = tk.Entry(add_cust_frame)
        customer_address_label = tk.Label(add_cust_frame, text='Customer Address: ')
        customer_address_entry = tk.Entry(add_cust_frame)
        customer_postcode_label = tk.Label(add_cust_frame, text='Post Code:')
        customer_postcode_entry = tk.Entry(add_cust_frame)
        customer_phone_label = tk.Label(add_cust_frame, text='Phone Number: ')
        customer_phone_entry = tk.Entry(add_cust_frame)
        customer_mobile_label = tk.Label(add_cust_frame, text='Mobile Number: ')
        customer_mobile_entry = tk.Entry(add_cust_frame)
        customer_email_label = tk.Label(add_cust_frame, text='Email Address: ')
        customer_email_entry = tk.Entry(add_cust_frame)
        customer_type_label = tk.Label(add_cust_frame, text='Type of Customer: ')
        customer_type_entry = tk.Entry(add_cust_frame)

        add_customer_button = ttk.Button(add_cust_frame, text='Add Customer to DB', command=lambda: add_customer_to_DB())
        clear_entry_button = ttk.Button(add_cust_frame, text="Clear all entry's", command=lambda: clear_customer_entry())
        # pack all the items, maybe pack onto a frame, then we can unpack the frame depending on the required usage

        clear_entry_button.grid(row=0, sticky='w')
        customer_name_label.grid(row=1,column=0, sticky='e')
        customer_name_entry.grid(row=1,column=1,sticky='e')
        customer_address_label.grid(row=2,column=0,sticky='e')
        customer_address_entry.grid(row=2,column=1,sticky='e')
        customer_postcode_label.grid(row=3,column=0,sticky='e')
        customer_postcode_entry.grid(row=3,column=1,sticky='e')
        customer_phone_label.grid(row=4,column=0,sticky='e')
        customer_phone_entry.grid(row=4,column=1,sticky='e')
        customer_mobile_label.grid(row=5,column=0,sticky='e')
        customer_mobile_entry.grid(row=5,column=1,sticky='e')
        customer_email_label.grid(row=6,column=0,sticky='e')
        customer_email_entry.grid(row=6,column=1,sticky='e')
        customer_type_label.grid(row=7,column=0,sticky='e')
        customer_type_entry.grid(row=7,column=1,sticky='e')
        add_customer_button.grid(row=8, columnspan=2, sticky='nsew')


        # add find customer widgets etc

        search_by_var = ['Name', 'Address', 'Postcode', 'Email', 'Phone', 'Mobile']
        search_by_lable = tk.Label(find_cust_frame, text='Search BY:')
        search_by_combo = ttk.Combobox(find_cust_frame, state='readonly')
        search_by_combo['values'] = search_by_var
        search_entry = ttk.Entry(find_cust_frame)
        search_button = ttk.Button(find_cust_frame, text='Search', command=lambda: search_cust_by_name())
        select_customer_button = ttk.Button(find_cust_frame, text='Select Highlighted Customer', command=lambda:select_cust())

        customer_tree = ttk.Treeview(find_cust_frame, height=10, columns=8)
        customer_tree['columns'] = ['ID', 'Name', 'Address', 'Postcode', 'Phone', 'Mobile','Email',  'Type']
        customer_tree['show'] = 'headings'
        customer_tree.heading('ID', text='ID')
        customer_tree.heading('Name', text='Name')
        customer_tree.heading('Address', text='Address')
        customer_tree.heading('Postcode', text='Postcode')
        customer_tree.heading('Phone', text='Phone')
        customer_tree.heading('Mobile', text='Mobile')
        customer_tree.heading('Email', text='Email')
        customer_tree.heading('Type', text='Type')

        search_by_lable.grid(row=0, column=0)
        search_by_combo.grid(row=0, column=1)
        search_entry.grid(row=0, column=2)
        search_button.grid(row=0, column=3)
        select_customer_button.grid(row=0, column=4)


       # grid the note book in the window

        cust_note.grid(row=1,column=0, sticky='nw', pady=0)

        def pressed_key_entry(event):
            if len(search_entry.get()) >= 2:
                search_cust_by_name()

        # make event binding, that if the entry box has focus and the text contined is over 2 fire off the search funct
        search_entry.bind('<KeyRelease>', pressed_key_entry)

        def display_serch(customer_list):
            # display the search results into the tree, first wipe the tree



            customer_tree.grid(row=1, column=0, columnspan=8)
            customer_tree.delete(*customer_tree.get_children())
            for customer in customer_list:
                customer_tree.insert('', 'end', text='cust deets', values=(customer.id,
                                                                           customer.name,
                                                                           customer.address,
                                                                           customer.postcode,
                                                                           customer.phone,
                                                                           customer.mobile,
                                                                           customer.email,
                                                                           customer.type,
                                                                           ))
        def select_cust():
            focus = customer_tree.focus()
            cust_selected = customer_tree.item(focus)
            global current_customer
            current_customer = Customer(cust_selected['values'][1],
                                        cust_selected['values'][2],
                                        cust_selected['values'][3],
                                        cust_selected['values'][4],
                                        cust_selected['values'][5],
                                        cust_selected['values'][6],
                                        cust_selected['values'][7],
                                        cust_selected['values'][0],
                                        )
            # update the top label with the current customer, name, postcode
            active_project_lable.config(text=f'Customer: <{current_customer.name}>')








        def add_customer_to_DB():

            # need to implement gate keepers to validate input and check custoemr does not allready exsist

            cust_to_add = Customer(customer_name_entry.get(),
                                   customer_address_entry.get(),
                                   customer_postcode_entry.get(),
                                   customer_phone_entry.get(),
                                   customer_mobile_entry.get(),
                                   customer_email_entry.get(),
                                   customer_type_entry.get(),
                                   '',
                                   )
            print(cust_to_add.address)

            Customer.save_to_db(cust_to_add)

        def clear_customer_entry():
            # clear the entry boxes for fresh entry
            customer_name_entry.delete(0,'end')
            customer_address_entry.delete(0,'end')
            customer_postcode_entry.delete(0,'end')
            customer_phone_entry.delete(0,'end')
            customer_mobile_entry.delete(0,'end')
            customer_email_entry.delete(0,'end')
            customer_type_entry.delete(0,'end')

        def search_cust_by_name():
            # search the database for a customer name, return the results
            search_text = search_entry.get()
            type_ = search_by_combo.get()

            if search_text == '':
                print('enter term to search for')
                return

            if type_ == '':
                print('choose paramiter to search by')
                return

            global search_term
            search_term = ''
            if type_ == 'Name':
                search_term = 'customer_name'
            if type_ == 'Address':
                search_term = 'customer_address'
            elif type_ == 'Postcode':
                search_term = 'customer_postcode'
            elif type_ == 'Email':
                search_term = 'customer_email'
            elif type_ == 'Phone':
                search_term = 'customer_phone'
            elif type_ == 'Mobile':
                search_term = 'customer_mobile'

            new_var = Customer.find_customer(search_text, search_term)
            print([f'{customer.name} {customer.address}' for customer in new_var])

            display_serch(new_var)


class ProjectsPage(tk.Frame):
    def __init__(self, parent, controler):
        tk.Frame.__init__(self, parent)

        def up_project_labels():
            # check to see if the current customer is the owber of the project, if not then scrap it !
            active_project_lable.config(text=f'Customer: <{current_customer.name}>'
                                             f' Project: <{current_project.project_name}>')


        # section for header info, about active customer and active project
        active_project_lable = tk.Label(self, text=f'Customer: <{current_customer.name}>'
                                                   f' Project: <{current_project.project_name}>')

        button234 = tk.Button(self, text='press to update', command=lambda: up_project_labels())
        button234.grid(row=5)

       # define the notebook its windows and
        active_project_lable.grid(row=0, column=0)
        project_note = ttk.Notebook(self)
        active_project_frame = ttk.Frame(project_note)
        search_project_frame = ttk.Frame(project_note)
        add_project_frame = ttk.Frame(project_note)
        project_note.add(active_project_frame, text='Active Project')
        project_note.add(search_project_frame, text='Search Projects')
        project_note.add(add_project_frame, text='Add Project')

        # active projects
        active_customer_key_deets_label = tk.Label(active_project_frame, text='KEY Customer Details')

        active_customer_key_deets_label.grid()

        # add project
        project_label_list = ['Customer ID',
                              'Project Name',
                              'Project Reference',
                              'Project Address',
                              'Project Postcode',
                              'Primary Contact',
                              'Project Type',
                              'Project Price Approx',
                              'Project Expected Profit',
                              'Project Triage',
                              'Project Lead MES',
                              ]
        entry = {}
        label = {}
        for i, name in enumerate(project_label_list):
            e = tk.Entry(add_project_frame)
            entry[name] = e
            e.grid(sticky='e', column=1)

            lb = tk.Label(add_project_frame, text=name)
            lb.grid(row=i, column=0, sticky='w')

            label[name] = lb
        project_note.grid(row=1, column=0, sticky='nw',pady=5)

        #define buttons, etc on the add projects page

        add_project_button = ttk.Button(add_project_frame, text='Add Project', command=lambda: add_project_to_db(entry))
        take_cuttent_button = ttk.Button(add_project_frame, text='Take Current', command=lambda: take_current())
        find_customer_for_project_button = ttk.Button(add_project_frame, text='Search')
        clear_all_project_info_button = ttk.Button(add_project_frame, text='Clear all entrys', command=lambda: clear_project_entrys())

        #grid widgets on the add projects page
        add_project_button.grid(row=len(entry)+1, column=0, columnspan=2, stick='nsew')
        take_cuttent_button.grid(row=0, column=2)
        find_customer_for_project_button.grid(row=0, column=3)
        clear_all_project_info_button.grid(row=1, column=2, columnspan=2, stick='nsew')

        # add stuf into the search for projects page
        project_serch_list =['Customer Name', 'Project Name','Primary Contact' 'Reference', 'Address', 'Post Code', 'Triage']
        search_project_label = tk.Label(search_project_frame, text='Search For')
        seach_project_combo = ttk.Combobox(search_project_frame, state='readonly')
        seach_project_combo['values'] = project_serch_list
        search_projects_entry = ttk.Entry(search_project_frame)
        search_projects_button = ttk.Button(search_project_frame, text='Search', command =lambda: search_projects())
        select_highligted_button = ttk.Button(search_project_frame,
                                              text='Select Highlighted Project',command=lambda: select_project())



        # make the ability to be able to view all projects for a given customer ID
        # make the serch work from the customer name
        # make the seatch work for primay contact
        projects_tree = ttk.Treeview(search_project_frame, height=10, columns=7)
        projects_tree['columns'] = ['Customer Name', 'Project Name', 'Primary Contact', 'Reference', 'Address', 'Post Code', 'Triage']
        projects_tree['show'] = 'headings'
        projects_tree.heading('Customer Name', text='Customer Name')
        projects_tree.heading('Project Name', text='Project Name')
        projects_tree.heading('Primary Contact', text='Primary Contact')
        projects_tree.heading('Reference', text='Reference')
        projects_tree.heading('Address', text='Address')
        projects_tree.heading('Post Code', text='Post Code')
        projects_tree.heading('Triage', text='Triage')

        #grids for project serch

        search_project_label.grid(row=0, column=0, stick='w')
        seach_project_combo.grid(row=0, column=1, stick='w')
        search_projects_entry.grid(row=0, column=2, stick='w')
        search_projects_button.grid(row=0, column=3, stick='w')
        select_highligted_button.grid(row=0,column=4, stick='w')














        def add_project_to_db(entry_list):
            # take all the details from the page and add a new prject, make sure to check that the input is valid
            # and that the project does not exsist
            #get the info from the boxes, pass it to the project method


            new_project = Projects(
                                   entry_list['Customer ID'].get(),
                                   entry_list['Project Name'].get(),
                                   entry_list['Project Reference'].get(),
                                   entry_list['Project Address'].get(),
                                   entry_list['Project Postcode'].get(),
                                   entry_list['Primary Contact'].get(),
                                   entry_list['Project Type'].get(),
                                   entry_list['Project Price Approx'].get(),
                                   '',
                                   entry_list['Project Expected Profit'].get(),
                                   '',
                                   entry_list['Project Triage'].get(),
                                   entry_list['Project Lead MES'].get(),
                                   '',
                                   '',

                                 )
            # print(new_project)
            new_project.save_to_db()
        def display_search(project_list):
            # create a list of all projects matching serch criteria, if customer name list all projects beling to naem or names
            projects_tree.grid(row=1, column=0, columnspan=8)
            projects_tree.delete(*projects_tree.get_children())

            if type(project_list) == list:
                _list =[]
                for project in project_list:
                    _list.append(Projects(project[1],
                                        project[2],
                                        project[3],
                                        project[4],
                                        project[5],
                                        project[6],
                                        project[7],
                                        project[8],
                                        project[9],
                                        project[10],
                                        project[11],
                                        project[12],
                                        project[13],
                                        project[14],
                                        project[0],
                                        ))
                project_list = _list

            for projects in project_list:
                projects_tree.insert('',
                                     'end', text='project details',
                                     values=(Customer.get_customer_name_by_id(projects.customer_id),
                                             projects.project_name,
                                             projects.primary_contact,
                                             projects.project_reference,
                                             projects.project_address,
                                             projects.project_postcode,
                                             projects.project_triage,
                                             projects.project_id,
                                             projects.customer_id,
                ))

            # get the values from the boxes and pass them to a fucntion in proctects

        def select_project():
            # slect a project high lighted in the tree view
            # find the project based upon id, load from database
            focus = projects_tree.focus()
            project_selected = projects_tree.item(focus)
            global current_project, current_customer
            project_id = project_selected['values'][7]
            customer_id =project_selected['values'][8]

            current_customer = Customer.find_customer(customer_id, 'id')[0]
            current_project = Projects.find_project(project_id, 'project_id')[0]
            up_project_labels()


            # current_project = Projects()

        def search_projects():
            # get the vales from the box and from the combo
            type_ = seach_project_combo.get()
            search_text = search_projects_entry.get()

            if search_text == "" or type_ == "":
                print('Fill Both entrys')
                return

            global search_term

            if type_ =='Customer Name':
                search_term ='customer_name'
                # fire over to 'find customer' return all projects under matching customers

            elif type_ =='Primay Contant':
                search_term ='primary_conatact'
                # fire over to 'find contact' return all project under matching contact
                projects_found ='primay constat'
                print('not yet implemented')

            elif type_ =='Project Name':
                search_term ='project_name'
            elif type_ =='Refrence':
                search_term ='project_refrence'
            elif type_ =='Address':
                search_term ='project_address'
            elif type_ =='Post Code':
                search_term ='project_postcode'
            elif type_ =='Triage':
                search_term ='project_triage'
                search_text =search_text

            if type_ == 'Customer Name' or type_ == 'Primary Contact':
                if type_ == 'Customer Name':
                    display_search(Projects.search_by_cust_name(search_text))
            else:
                results = Projects.find_project(search_text,search_term)
                display_search((Projects.find_project(search_text, search_term)))

        def take_current():
            # take the id of the currentley selected customer and put it in the form
            customer_id_entry_var = tk.StringVar()
            entry['Customer ID'].config(textvariable=customer_id_entry_var)
            global current_customer
            customer_id_entry_var.set(current_customer.id)

        def clear_project_entrys():
            # clear the entry boxes for fresh entry
            for entry_var in project_label_list:
                entry[entry_var].delete(0, 'end')

class TaskPage(tk.Frame):
    def __init__(self, parent, controler):
        tk.Frame.__init__(self, parent)
        # add side frame for notes, one frame for a list of tasks.

        active_project_lable = tk.Label(self, text=f'Customer: <{current_customer.name}>'
                                                   f' Project: <{current_project.project_name}>')

        # update_project_button = tk.Button(self, text='press to update', command=lambda: up_project_labels())

       # define the notebook its windows and
       #  active_project_lable.grid(row=0, column=0)
        task_note = ttk.Notebook(self)
        task_list_frame = ttk.Frame(task_note)
        search_task_frame = ttk.Frame(task_note)
        add_task_frame = ttk.Frame(task_note)
        task_note.add(task_list_frame, text='Task List')
        task_note.add(search_task_frame, text='Search Tasks')
        task_note.add(add_task_frame, text='Add Tasks')

        task_note.grid(row=1,column=0,stick='nesw')

        # active projects
        # active_customer_key_deets_label = tk.Label(active_project_frame, text='KEY Customer Details')

        # active_customer_key_deets_label.grid()

         # add task
        task_label_list = ['Project ID',
                           'Task Description',
                           'Task MES Lead',
                           'Task Triage',
                           ]
        entry = {}
        label = {}
        for i, name in enumerate(task_label_list):
            e = tk.Entry(add_task_frame)
            entry[name] = e

            if name == 'Task Description':
                e.grid(sticky='ew',column=1, columnspan=3)

            elif name != 'Task Description':
                e.grid(sticky='e', column=1)

            lb = tk.Label(add_task_frame, text=name)
            lb.grid(row=i, column=0, sticky='w')

            label[name] = lb

        pick_start_date_label = ttk.Label(add_task_frame, text='Start Date')
        pick_end_date_label = ttk.Label(add_task_frame, text='End Date')
        pick_start_date_label.grid(row=5,column=0,sticky='w')
        pick_end_date_label.grid(row=6,column=0,sticky='w')


        pick_start_date_entry = DateEntry(add_task_frame)
        pick_end_date_entry = DateEntry(add_task_frame)
        pick_start_date_entry.grid(row=5,column=1,sticky='e')
        pick_end_date_entry.grid(row=6,column=1,sticky='e')


        #define buttons, etc on the add tasks page

        add_task_button = ttk.Button(add_task_frame, text='Add Task', command=lambda: add_task_to_db(entry))
        take_task_button = ttk.Button(add_task_frame, text='Take Current', command=lambda: take_current())
        find_project_for_task_button = ttk.Button(add_task_frame, text='Search')
        clear_all_tasks_info_button = ttk.Button(add_task_frame, text='Clear all entrys', command=lambda: clear_task_entrys())

        #grid the buttons etc add task Page
        add_task_button.grid(row=7, column=0, columnspan=2, stick='nsew')
        take_task_button.grid(row=0, column=2)
        find_project_for_task_button.grid(row=0,column=3)
        clear_all_tasks_info_button.grid(row=8, column=0, columnspan=2, stick='nsew')

        #define panned window on list tasks frame
        button_bar_frame = tk.Frame(task_list_frame, height=25, bg='light sea green')
        button_bar_frame.grid(row=0,column=0,sticky='nsew',columnspan=11)
        task_panned = tk.PanedWindow(task_list_frame)

        task_panned.grid(row=1, column=1, stick='NSEW', columnspan=10)
        frame_panned_left = ttk.Frame(task_list_frame,height=300,width=200)
        text_panned_right = tk.Text(task_panned,height=100,width=100)
        #TODO make panned window have a scroll bar
        frame_panned_left.grid()

        canvas_panned_left = tk.Canvas(frame_panned_left,height=510,width=220)
        display_task_frame = tk.Frame(canvas_panned_left)
        scroll_task_list = tk.Scrollbar(frame_panned_left,orient='vertical',command=canvas_panned_left.yview)
        canvas_panned_left.configure(yscrollcommand=scroll_task_list.set)

        scroll_task_list.pack(side='right',fill='y')
        canvas_panned_left.pack(side='left', fill='both', expand=True)
        canvas_panned_left.create_window((4,4),window=display_task_frame,anchor='nw')

        task_panned.add(frame_panned_left)
        task_panned.add(text_panned_right)





        display_task_frame.bind('<Configure>',lambda event,canvas=canvas_panned_left:costom_config_canvas(canvas))









        #make buttons etc for list tasks
        list_task_label = ttk.Label(button_bar_frame, text="List tasks with triage or triage's comma separated list: P,L,A")
        list_task_entry = ttk.Entry(button_bar_frame)
        list_task_lead_label = ttk.Label(button_bar_frame,text="Chose Mes task lead: #, 'all mes' Or 'all' ")
        list_task_lead_entry = ttk.Entry(button_bar_frame)
        list_task_search_contact_button = ttk.Button(button_bar_frame,text='Search for name',command=lambda:search_contact())
        list_task_button = ttk.Button(button_bar_frame, text='List Tasks',command=lambda:list_tasks())

        #grid the button for list tasks
        list_task_label.grid(row=1,column=1)
        list_task_entry.grid(row=1,column=2)
        list_task_entry.insert(0,"P,L")
        list_task_lead_label.grid(row=1,column=3)
        list_task_lead_entry.grid(row=1,column=4)
        list_task_lead_entry.insert(0,'all mes')
        list_task_search_contact_button.grid(row=1,column=5)
        list_task_button.grid(row=1,column=6)

        # function definitions

        def search_contact():
            print('not yet implemented, will eventually search for the name of the contact, then pull its id into the box')

        def add_task_to_db(entry_list):
            # take all the info enterd into the fields and pass to save to db method
            # need to convert the dates into the correct ISO
            start_date = pick_start_date_entry.get()
            print(convert_date_postgres(start_date,'i'))

            new_task = Tasks(entry_list['Project ID'].get(),
                             entry_list['Task Description'].get(),
                             entry_list['Task MES Lead'].get(),
                             convert_date_postgres(pick_start_date_entry.get(),'i'),
                             convert_date_postgres(pick_end_date_entry.get(),'i'),
                             '',
                             entry_list['Task Triage'].get(),
                             '',

                             )

            new_task.save_to_db()


        def take_current():
            # take the currentley selected project as the project id
            project_id_entry_var = tk.StringVar()
            entry['Project ID'].config(textvariable=project_id_entry_var)
            global current_project
            project_id_entry_var.set(current_project.project_id)

        def clear_task_entrys():
            #clear all info from the task entrys
            for entry_var in task_label_list:
                entry[entry_var].delete(0, 'end')
            pick_end_date_entry.delete(0,'end')
            pick_start_date_entry.delete(0,'end')

        def pop_up_cal():
            # make a window pop up with a calander, return to the sender the date picked
            win = tk.Toplevel()
            win.wm_title('Choose Calander')

            start_date_cal = Calendar(win)
            start_date_cal.grid()

        def list_tasks():

            # get the input from the entry
            # get the matrix memeber or other to search for
            # pass to the class method and return a list to display
            # task owner wants to be global, searchable on the contacts page
            global task_frame_count

            user_triage = list_task_entry.get()
            task_owner_or_owners = list_task_lead_entry.get()
            list_of_tasks = Tasks.get_tasks_by_triage(task_owner_or_owners,user_triage)


            # clear the frames generated previosey
            if len(task_frame_count) != 0:
                try:
                    for _ in task_frame_count:
                        _.grid_forget()
                        _.destroy()
                except:
                    print('tcl error no frames to delete')

            # get the projects title and ID from the task, display it after the task tilte
            # clear the elements in the tree view
            #loop through all the tasks and add the to the tree view,
            task_frame_count =[]
            for i,task in enumerate(list_of_tasks):
                i_int = i
                i = task_display_frame(task,display_task_frame,'head_only')
                i.grid(row=i_int, column=0)
                task_frame_count.append(i)

            #update the scroll bar

            canvas_panned_left.configure(scrollregion=canvas_panned_left.bbox('all'))

        def display_task_list(task_list, orderby, task_or_project_focus):
            '''
            a fuction to display the given tasks, ordering by input and biasing task or projects
            :param task_list: list of tasks to display
            :param orderby is the way to order the tasks
            :param task_or_project_focus: will the list focus on tasks or projects
            :return:
            '''

        def task_display_frame(item, frame_to_display_on, starting_state, *args):
            '''
            build a frame to whitch we pass a task item, the tasks list is built from these frames
            the frame consists of header with basic info about the task and project, a button to expand the header
            showing greater detail about the task, task and project info should be able to be modified from this frame

            :param item: is the task item we wish to display
            :param args: are other arguments not yet decided such as order, color, info to dispaly
            :param starting_state: what state to start in, expanded, colored etc
            :return: a frame onto the task page,
            '''

            frame = ttk.Frame(frame_to_display_on)
            frame_header = ttk.Label(frame, text=f'{item.task_description} <{format_day_tasks(item.task_end_date)}>')
            expand_frame_button = tk.Button(frame,text='+',height=0,width=0,command=lambda:expand_frame(item))
            frame_header.grid(row=0,column=0)
            expand_frame_button.grid(row=1,column=0)




            def expand_frame(task):
               # make a new function to disaplay a task in full view, contaning all info that is editible
               # get all info for the customer, the project, contacts etc.
               project_for_frame = Projects.find_project(task.project_id,'project_id')[0]
               customer_for_frame = Customer.find_customer(project_for_frame.customer_id,'id')[0]

               task_win = tk.Toplevel()
               task_win.wm_title(f'{task.task_description} --- {project_for_frame.project_name} --- {customer_for_frame.name}')

               task_frame = ttk.Frame(task_win)
               #add some meaningfull info to the frame, make it editible and saveable to the database,

               #section for the customer
                #key contact deets, add contact to customer, change contact deets
               customer_lable_frame = ttk.LabelFrame(task_frame,text='Customer')
               customer_lable_frame.grid(row=0,column=0)
               customer_name_entry = ttk.Entry(customer_lable_frame)
               customer_name_entry.insert(0,customer_for_frame.name)

               customer_name_entry.grid()







               task_frame.grid()

            return frame
        def costom_config_canvas(canvas):

            canvas.configure(scrollregion=canvas.bbox('all'))



app = MatrixCrmApp()
app.mainloop()





