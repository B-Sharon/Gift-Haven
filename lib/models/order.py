from models.__init__ import CURSOR, CONN
from models.customer import Customer
from models.user import User

class Order:
    all = {}

    def __init__(self, order_id, date, customer_id, user_id, total_amount):
        self.order_id = order_id
        self.date = date
        self.customer_id = customer_id
        self.user_id = user_id
        self.total_amount = total_amount

    def __repr__(self):
        return f"<Order {self.order_id}: {self.date}, Customer: {self.customer_id}, User: {self.user_id}, Total Amount: {self.total_amount}>"

    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT DEFAULT (datetime('now', 'localtime')),
            customer_id INTEGER,
            user_id INTEGER,
            total_amount REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        SQL = "DROP TABLE IF EXISTS orders;"
        CURSOR.execute(SQL)
        CONN.commit()

    def save(self):
        SQL = """
        INSERT INTO orders (date, customer_id, user_id, total_amount)
        VALUES (?, ?, ?, ?);
        """
        CURSOR.execute(SQL, (self.date, self.customer_id, self.user_id, self.total_amount))
        CONN.commit()
        self.order_id = CURSOR.lastrowid
        type(self).all[self.order_id] = self

    def update(self):
        SQL = """
        UPDATE orders
        SET date = ?, customer_id = ?, user_id = ?, total_amount = ?
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.date, self.customer_id, self.user_id, self.total_amount, self.order_id))
        CONN.commit()

    def delete(self):
        SQL = """
        DELETE FROM orders
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.order_id,))
        CONN.commit()
        del type(self).all[self.order_id]
        self.order_id = None

    @classmethod
    def create(cls, date, customer_id, user_id, total_amount):
        order = cls(order_id = None, date = date, customer_id= customer_id, user_id = user_id, total_amount=total_amount)
        order.total_amount = total_amount
        order.save()
        return order

    @classmethod
    def instance_from_db(cls, row):
        order = cls.all.get(row[0])
        if order:
            order.date = row[1]
            order.customer_id = row[2]
            order.user_id = row[3]
            order.total_amount = row[4]
        else:
            order = cls(row[0], row[1], row[2], row[3], row[4])
            cls.all[row[0]] = order
        return order

    @classmethod
    def get_all(cls):
        SQL = "SELECT * FROM orders;"
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, order_id):
        SQL = "SELECT * FROM orders WHERE id = ?;"
        row = CURSOR.execute(SQL, (order_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
