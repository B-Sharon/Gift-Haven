from models.__init__ import CURSOR, CONN

class Gift:
    all = {}

    def __init__(self, gift_id, gift_name, gift_price):
        self.gift_id = gift_id
        self.gift_name = gift_name
        self.gift_price = gift_price

    def __repr__(self):
        return f"<Gift {self.gift_id}: {self.gift_name}, Price: {self.gift_price}>"

    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_name TEXT,
            gift_price REAL
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        SQL = "DROP TABLE IF EXISTS gifts;"
        CURSOR.execute(SQL)
        CONN.commit()

    def save(self):
        SQL = """
        INSERT INTO gifts (gift_name, gift_price)
        VALUES (?, ?);
        """
        CURSOR.execute(SQL, (self.gift_name, self.gift_price))
        CONN.commit()
        self.gift_id = CURSOR.lastrowid
        type(self).all[self.gift_id] = self

    def update(self):
        SQL = """
        UPDATE gifts
        SET gift_name = ?, gift_price = ?
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.gift_name, self.gift_price, self.gift_id))
        CONN.commit()

    def delete(self):
        SQL = """
        DELETE FROM gifts
        WHERE id = ?;
        """
        CURSOR.execute(SQL, (self.gift_id,))
        CONN.commit()
        del type(self).all[self.gift_id]
        self.gift_id = None

    @classmethod
    def create(cls, gift_name, gift_price):
        gift = cls(gift_id=None, gift_name=gift_name, gift_price=gift_price)
        gift.save()
        return gift

    @classmethod
    def instance_from_db(cls, row):
        gift = cls.all.get(row[0])
        if gift:
            gift.gift_name = row[1]
            gift.gift_price = row[2]
        else:
            gift = cls(row[0], row[1], row[2])
            cls.all[row[0]] = gift
        return gift

    @classmethod
    def get_all(cls):
        SQL = "SELECT * FROM gifts;"
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, gift_id):
        SQL = "SELECT * FROM gifts WHERE id = ?;"
        row = CURSOR.execute(SQL, (gift_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
