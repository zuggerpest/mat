from database import CursorFromConnectionFromPool


class Customer:

    def  __init__(self, customer_name, customer_address, customer_postcode,
                  customer_phone, customer_mobile, customer_email, customer_type, customer_id):

        self.name = customer_name
        self.address = customer_address
        self.postcode = customer_postcode
        self.phone = customer_phone
        self.mobile = customer_mobile
        self.email = customer_email
        self.type = customer_type
        self.id = customer_id

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            # add gate keepers to this method, I want to make sure data is a propper format and valid
            # make outside metthod to check if the customer exsists allready in db of file structure.
            cursor.execute('INSERT INTO customers (customer_name, customer_address, customer_postcode, customer_phone,'
                           ' customer_mobile, customer_email, customer_type) Values(%s, %s, %s, %s, %s, %s, %s)',
                           (self.name, self.address, self.postcode, self.phone, self.mobile, self.email, self.type))

    @classmethod
    def return_customer(cls, cursor_to_fetch):
        # return customers as a list of customers, with fully populated data
        try:
            customer_data = cursor_to_fetch.fetchall()
            customer_list =[]

            for customer in customer_data:
                customer_list.append(cls(customer_name=customer[1], customer_address=customer[2],
                                         customer_postcode=customer[3], customer_phone=customer[4],
                                         customer_mobile=customer[5], customer_email=customer[6],
                                         customer_type=customer[7], customer_id=customer[0]))

            return customer_list

        except:
            return f'no Customer with {cursor_to_fetch}'



    @classmethod
    def find_customer(cls, details, detail_type):
        '''
        search for a customer based upon the detail passed inc type
        :param details: the thing we are serching for
        :param detail_type: the category we are searching with, must be a valid column name
        :return:return a list of customers matching
        '''

        with CursorFromConnectionFromPool() as cursor:
            # make the serch non case sensetive and use basic wildcard
            if detail_type == 'id':
                try:
                    cursor.execute(f'SELECT * FROM customers WHERE {detail_type} = %s', (details,))
                    return Customer.return_customer(cursor)
                except:
                    print('summt wrong with customer id or cursor')
            else:
                try:
                    cursor.execute(f'SELECT * FROM customers WHERE {detail_type} ILIKE %s', (details+'%',))
                    return Customer.return_customer(cursor)
                except:
                    print(f'not a valid cursor: {cursor}')


    def get_customer_by_name(self, customer_name):
        # make select all and get the user id, if two users have same name make a choice happen on adress
        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute('SELECT * FROM customers WHERE customer_name=%s', (customer_name,))
                return Customer.return_customer(cursor)
            except:
                print(f'no customer found with the name: {customer_name}')
    def get_customer_by_email(self, customer_email):
        # try and load the customer, if it errors return that the customer email is not valid
        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute('SELECT * FROM customers WHERE customer_email=%s', (customer_email,))
                return Customer.return_customer(cursor)

            except:
                print('the email entered is not assigned to a customer, please check')
    @classmethod
    def get_customer_name_by_id(cls, customer_id):
        with CursorFromConnectionFromPool() as cursor:
            try:
                cursor.execute('SELECT customer_name FROM customers WHERE id=%s', (int(customer_id),))
                ret = cursor.fetchone()
                return ret

            except:
                print('the email entered is not assigned to a customer, please check')

    def __str__(self):
        return f'{self.name} -- {self.email} -- {self.address}'







