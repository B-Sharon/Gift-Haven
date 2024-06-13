from models.__init__ import CURSOR, CONN
from models.gift import Gift

class OrderItems:
    all = {}

    def __init__(self, id, order_id, gift_id, quantity, price):
        self.id = id
        self.order_id = order_id
        self.gift_id = gift_id
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<OrderItem {self.id}: Order {self.order_id}, Gift {self.gift_id}, Quantity: {self.quantity}, Price: {self.price}>"

    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            gift_id INTEGER,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(gift_id) REFERENCES gifts(gift_id)
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        SQL = "DROP TABLE IF EXISTS order_items;"
        CURSOR.execute(SQL)
        CONN.commit()

    def save(self):
        SQL = """
        INSERT INTO order_items (order_id, gift_id, quantity, price)
        VALUES (?, ?, ?, ?);
        """
        CURSOR.execute(SQL, (self.order_id, self.gift_id, self.quantity, self.price))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        SQL = """
        UPDATE order_items
        SET order_id = ?, gift_id = ?, quantity = ?, price = ?
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.order_id, self.gift_id, self.quantity, self.price, self.id))
        CONN.commit()

    def delete(self):
        SQL = """
        DELETE FROM order_items
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, order_id, gift_id, quantity, price):
        order_item = cls(None, order_id, gift_id, quantity, price)
        order_item.save()
        return order_item

    @classmethod
    def instance_from_db(cls, row):
        order_item = cls.all.get(row[0])
        if order_item:
            order_item.order_id = row[1]
            order_item.gift_id = row[2]
            order_item.quantity = row[3]
            order_item.price = row[4]
        else:
            order_item = cls(row[0], row[1], row[2], row[3], row[4])
            cls.all[row[0]] = order_item
        return order_item

    @classmethod
    def get_all(cls):
        SQL = "SELECT * FROM order_items;"
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        SQL = "SELECT * FROM order_items WHERE id = ?;"
        row = CURSOR.execute(SQL, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_order_id(cls, order_id):
        SQL = "SELECT * FROM order_items WHERE order_id = ?;"
        CURSOR.execute(SQL, (order_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
