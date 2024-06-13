from models.__init__ import CURSOR, CONN
from models.gift import Gift
from models.order import Order

class OrderItems:
    all = {}

    def __init__(self, order_item_id, order_id, gift_id, quantity):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.gift_id = gift_id
        self.quantity = quantity
        self.price = self.get_price() * self.quantity

    def __repr__(self):
        gift = Gift.find_by_id(self.gift_id)
        return f"<OrderItem {self.order_item_id}: Order {self.order_id}, Gift: {gift.gift_name}, Quantity: {self.quantity}, Price: {self.price}>"

    def get_price(self):
        gift = Gift.find_by_id(self.gift_id)
        return gift.gift_price if gift else 0

    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            gift_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(gift_id) REFERENCES gifts(id)
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
        self.order_item_id = CURSOR.lastrowid
        type(self).all[self.order_item_id] = self

        # Update the associated Order's total_amount
        self.update_order_total_amount()

    def update(self):
        self.price = self.get_price() * self.quantity
        SQL = """
        UPDATE order_items
        SET order_id = ?, gift_id = ?, quantity = ?, price = ?
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.order_id, self.gift_id, self.quantity, self.price, self.order_item_id))
        CONN.commit()

        # Update the associated Order's total_amount
        self.update_order_total_amount()

    def delete(self):
        SQL = """
        DELETE FROM order_items
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.order_item_id,))
        CONN.commit()
        del type(self).all[self.order_item_id]
        self.order_item_id = None

        # Update the associated Order's total_amount
        self.update_order_total_amount()

    def update_order_total_amount(self):
        # Retrieve all order items for the current order
        order_items = OrderItems.find_by_order_id(self.order_id)

        # Calculate the total amount based on all order items
        total_amount = sum(item.price for item in order_items)

        # Update the associated Order's total_amount
        order = Order.find_by_id(self.order_id)
        if order:
            order.total_amount = total_amount
            order.update()  # Ensure the updated total_amount is saved to the database

    @classmethod
    def create(cls, order_id, gift_id, quantity):
        order_item = cls(order_item_id=None, order_id=order_id, gift_id=gift_id, quantity=quantity)
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
            order_item = cls(row[0], row[1], row[2], row[3])
            order_item.price = row[4]
            cls.all[row[0]] = order_item
        return order_item

    @classmethod
    def get_all(cls):
        SQL = "SELECT * FROM order_items;"
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, order_item_id):
        SQL = "SELECT * FROM order_items WHERE id = ?;"
        row = CURSOR.execute(SQL, (order_item_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_order_id(cls, order_id):
        SQL = "SELECT * FROM order_items WHERE order_id = ?;"
        CURSOR.execute(SQL, (order_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
