# In customer.py

from models import CURSOR, CONN  # Adjust import as necessary

class Customer:
    all = {}

    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact

    def __repr__(self):
        return f"<Customer {self.customer_id}: {self.name}, {self.contact}>"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def contact(self):
        return self._contact
    
    @contact.setter
    def contact(self, contact):
        if isinstance(contact, (int, str)) and len(str(contact)) > 0:
            self._contact = contact
        else:
            raise ValueError("Contact must be a non-empty string or integer")

    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact INTEGER UNIQUE NOT NULL
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        SQL = "DROP TABLE IF EXISTS customers;"
        CURSOR.execute(SQL)
        CONN.commit()

    def save(self):
        SQL = """
        INSERT INTO customers (name, contact)
        VALUES (?, ?);
        """
        CURSOR.execute(SQL, (self.name, self.contact))
        CONN.commit()

        self.customer_id = CURSOR.lastrowid
        type(self).all[self.customer_id] = self

    def update(self):
        SQL = """
        UPDATE customers
        SET name = ?, contact = ?
        WHERE customer_id = ?;
        """
        CURSOR.execute(SQL, (self.name, self.contact, self.customer_id))
        CONN.commit()

    def delete(self):
        SQL = """
        DELETE FROM customers
        WHERE customer_id = ?;
        """
        CURSOR.execute(SQL, (self.customer_id,))
        CONN.commit()

        del type(self).all[self.customer_id]
        self.customer_id = None

    @classmethod
    def create(cls, name, contact):
        customer = cls(None, name, contact)
        customer.save()
        return customer

    @classmethod
    def instance_from_db(cls, row):
        customer = cls.all.get(row[0])

        if customer:
            customer.name = row[1]
            customer.contact = row[2]
        else:
            customer = cls(row[0], row[1], row[2])
            cls.all[row[0]] = customer
        return customer

    @classmethod
    def get_all(cls):
        SQL = """
        SELECT * FROM customers;
        """
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, customer_id):
        SQL = """
        SELECT * FROM customers
        WHERE customer_id = ?;
        """
        row = CURSOR.execute(SQL, (customer_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_contact(cls, contact):
        SQL = """
        SELECT * FROM customers
        WHERE contact = ?;
        """
        row = CURSOR.execute(SQL, (contact,)).fetchone()
        return cls.instance_from_db(row) if row else None
