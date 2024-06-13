from models.__init__ import CURSOR, CONN

class Customer:
    #dictionary of objects saved to the database
    all = {}

    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        

    def __repr__(self):
        return f"<User {self.customer_id}: {self.name}, {self.contact} "

    #setting the customer's name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len (name):
            self._name = name

        else:
            raise ValueError ("Name must be a non empty string")
        
     # Setting the customer's contact
    @property
    def contact(self):
        return self._contact
    
    @contact.setter
    def contact(self, contact):
        if isinstance(contact, str) and len(contact):
            self._contact = contact
        else:
            raise ValueError("Contact number must be filled")

    # creating the tables
    @classmethod
    def create_table (cls):
        """Creating a new table to persist the attributes of customers instances"""
        SQL = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact INTEGER NOT NULL
        );
        """

        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    # drops the table if it exists
    def drop_table(cls):
        """Drops the table if it exists"""
        SQL = "DROP TABLE IF EXISTS customers;"
        CURSOR.execute(SQL)
        CONN.commit()

    # instance method
    def save(self):
        """
        Inserts a new row with the values of the currrent customer object
        Saves the instance to the database
        """
        SQL = """
        INSERT INTO customers (name, contact)
        VALUES (?,?);
        """
        CURSOR.execute(SQL, (self.name, self.contact))
        CONN.commit()

        self.customer_id = CURSOR.lastrowid
        type(self).all[self.customer_id] = self
    
    # updating the table row
    def update(self):
        """
        Updates a row with the values of the currrent Customer object
        Saves the instance to the database
        """
        SQL = """
        UPDATE customers
        SET name =?, contact =?
        WHERE customer_id =?;
        """
        CURSOR.execute(SQL, (self.name, self.contact, self.customer_id))
        CONN.commit()
        
    # deleting the table row
    def delete(self):
        """
        Deletes a row with the values of the currrent Cusromers object
        Saves the instance to the database
        """
        SQL = """
        DELETE FROM customers
        WHERE customer_id =?;
        """
        CURSOR.execute(SQL, (self.customer_id,))
        CONN.commit()

        # Deleting the dictionary entry using the customer_id as the key
        del type(self).all[self.customer_id]

        #Set the id to None
        self.customer_id = None

    
    @classmethod
    # creating a new customer instance and save it to the database
    def create(cls, name, contact):
        """
        Creates a new User instance and save it to the database
        """
        customer = cls(None, name, contact)
        customer.save()
        return customer
    
    #Returns a customer instance corresponding to a database row, using the instance from the all dictionary if it exists
    @classmethod
    def instance_from_db(cls, row):
        # check the dictionary for existing instances using the row's primary key
        customers = cls.all.get(row[0])

        if customers: 
            #ensure attributes match row values in case local instance was modified
            customers.name = row[1]
            customers.contact = row[2]
        else:
            #not in dictionary, create new instance and add to the dictionary
            customers = cls(row[0], row[1], row[2])
            cls.all[row[0]] = customers
        return customers

    @classmethod
    # returns a list of all customer instances from the databse
    def get_all(cls):
        SQL = """
        SELECT * FROM customers;
        """
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    # finds and returns a customer instance by it's id
    def find_by_id(cls,customer_id):
        sql = """
            SELECT * FROM customers
            WHERE customer_id =?
        """
        row = CURSOR.execute(sql, (customer_id, )).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    # finds and returns a customer instance by it's contact
    def find_by_contact(cls, contact):
        sql = """
            SELECT * FROM customers
            WHERE contact =?
        """
        row = CURSOR.execute(sql, (contact, )).fetchone()
        return cls.instance_from_db(row) if row else None