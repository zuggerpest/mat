from database import CursorFromConnectionFromPool
from customer import Customer


class Projects:

    def __init__(self, customer_id, project_name, project_reference, project_address,
                 project_postcode, primary_contact, project_type, project_price_approx,project_price_final, project_expected_profit,
                 project_actual_profit, project_triage, project_lead_mes, project_completed_on, project_id):

        self.customer_id = customer_id
        self.project_name = project_name
        self.project_reference = project_reference
        self.project_address = project_address
        self.project_postcode = project_postcode
        self.primary_contact = primary_contact
        self.project_type = project_type
        self.project_price_approx = project_price_approx
        self.project_price_final = project_price_final
        self.project_expected_profit = project_expected_profit
        self.project_actual_profit = project_actual_profit
        self.project_triage = project_triage
        self.project_lead_mes = project_lead_mes
        self.project_completed_on = project_completed_on
        self.project_id = project_id

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            # add gate keepers to this method, I want to make sure data is a propper format and valid
            # make outside metthod to check if the project exsists allready in db or the file structure.
            cursor.execute('INSERT INTO projects'
                           '(customer_id,'
                           'project_name,'
                           'project_reference,'
                           'project_address,'
                           'project_postcode,'
                           'primary_contact,'
                           'project_type,'
                           'project_price_approx,'
                           'project_expected_profit,'
                           'project_triage,'
                           'project_lead_mes)'
                           ' Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (int(self.customer_id),
                            self.project_name,
                            self.project_reference,
                            self.project_address,
                            self.project_postcode,
                            int(self.primary_contact),
                            self.project_type,
                            self.project_price_approx,
                            self.project_expected_profit,
                            self.project_triage,
                            self.project_lead_mes,))

    @classmethod
    def return_project(cls, cursor_to_fetch,):
    # return a list of projects with fully populated data
        try:
            project_data = cursor_to_fetch.fetchall()
            project_list = []

            for project in project_data:
                project_list.append(cls(customer_id=project[1],
                                        project_name=project[2],
                                        project_reference=project[3],
                                        project_address=project[4],
                                        project_postcode=project[5],
                                        primary_contact=project[6],
                                        project_type=project[7],
                                        project_price_approx=project[8],
                                        project_price_final=project[9],
                                        project_expected_profit=project[10],
                                        project_actual_profit=project[11],
                                        project_triage=project[12],
                                        project_lead_mes=project[13],
                                        project_completed_on=project[14],
                                        project_id=project[0],
                                        ))

            return project_list


        except:
              print(cursor_to_fetch+' not found')







    @classmethod
    def find_project(cls, details, detail_type):
        '''
        search for a customer based upon the detail passed inc type
        :param details: the thing we are serching for
        :param detail_type: the category we are searching with, must be a valid column name
        :return:return a list of customers matching
        '''
        if detail_type == 'customer_id' or detail_type == 'project_id':

            with CursorFromConnectionFromPool() as cursor:
                try:
                    cursor.execute(f'SELECT * FROM projects WHERE {detail_type} = %s', (details,))
                    # cursor.execute(f'SELECT * FROM projects')
                    return Projects.return_project(cursor)
                except:
                    print(f'not a valid cursor: {cursor}')

        with CursorFromConnectionFromPool() as cursor:
            # make the serch non case sensetive and use basic wildcard
                try:
                    cursor.execute(f'SELECT * FROM projects WHERE {detail_type} ILIKE %s', (details+'%',))
                    # cursor.execute(f'SELECT * FROM projects')
                    return Projects.return_project(cursor)
                except:
                    print(f'not a valid cursor: {cursor}')

    @classmethod
    def search_by_cust_name(cls, name_to_serch):

        # call the customer method for searching, get the id then find all projects with that
        cust_list = Customer.find_customer(name_to_serch, 'customer_name')
        projects_list =[]
        for cust in cust_list:
            pro_list = (Projects.get_projects_by_id(cust.id))
            for pro in pro_list:
                projects_list.append(pro)

        return projects_list

    @classmethod
    def get_projects_by_id(cls, customer_id):
        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute('SELECT * FROM projects WHERE customer_id=%s', (int(customer_id),))
                ret = cursor.fetchall()
                return ret

            except:
                print('the email entered is not assigned to a customer, please check')





    # # search for a project based upon a type and value
    #
    #     with CursorFromConnectionFromPool() as cursor:
    #
    #         try:
    #             # cursor.execute(f'SELECT * FROM projects WHERE {search_term} ILIKE %s', (search_text+'%',))
    #             # return Projects.return_project(cursor)
    #
    #             cursor.execute('SELECT * FROM projects')
    #             return Projects.return_project(cursor)
    #         except:
    #
    #             print(f'nothing like that found here {search_term} : {search_text}')








    def __repr__(self):
        print(              self.customer_id,
                            self.project_name,
                            self.project_reference,
                            self.project_address,
                            self.project_postcode,
                            self.primary_contact,
                            self.project_type,
                            self.project_price_approx,
                            self.project_expected_profit,
                            self.project_triage,
                            self.project_lead_mes,)






