from models.__init__ import CURSOR, CONN

class Gift:
    # Dictionary of objects saved to the database
    all = {}

    def __init__(self, gift_id, gift_name, gift_price):
        self.gift_id = gift_id
        self.gift_name = gift_name
        self.gift_price = gift_price

    def __repr__(self):
        return f"<Gift {self.gift_id}: {self.gift_name}, {self.gift_price}>"

    @classmethod
    def create_table(cls):
        """Creating a new table to persist the attributes of gifts instances"""
        SQL = """
        CREATE TABLE IF NOT EXISTS gifts (
            gift_id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_name TEXT NOT NULL,
            gift_price REAL NOT NULL
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the table if it exists"""
        SQL = "DROP TABLE IF EXISTS gifts;"
        CURSOR.execute(SQL)
        CONN.commit()

    def save(self):
        """Inserts a new row with the values of the current gift object and saves the instance to the database"""
        SQL = """
        INSERT INTO gifts (gift_name, gift_price)
        VALUES (?, ?);
        """
        CURSOR.execute(SQL, (self.gift_name, self.gift_price))
        CONN.commit()
        self.gift_id = CURSOR.lastrowid
        type(self).all[self.gift_id] = self

    def update(self):
        """Updates a row with the values of the current gift object and saves the instance to the database"""
        SQL = """
        UPDATE gifts
        SET gift_name=?, gift_price=?
        WHERE gift_id=?;
        """
        CURSOR.execute(SQL, (self.gift_name, self.gift_price, self.gift_id))
        CONN.commit()

    def delete(self):
        """Deletes a row with the values of the current gift object and saves the instance to the database"""
        SQL = """
        DELETE FROM gifts
        WHERE gift_id=?;
        """
        CURSOR.execute(SQL, (self.gift_id,))
        CONN.commit()
        del type(self).all[self.gift_id]
        self.gift_id = None

    @classmethod
    def create(cls, gift_name, gift_price):
        """Creates a new Gift instance and saves it to the database"""
        gift = cls(None, gift_name, gift_price)
        gift.save()
        return gift

    @classmethod
    def instance_from_db(cls, row):
        """Returns a gift instance corresponding to a database row"""
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
        """Returns a list of all gift instances from the database"""
        SQL = """
        SELECT * FROM gifts;
        """
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, gift_id):
        """Finds and returns a gift instance by its id"""
        sql = """
            SELECT * FROM gifts
            WHERE gift_id = ?
        """
        row = CURSOR.execute(sql, (gift_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, gift_name):
        """Finds and returns a gift instance by its name"""
        sql = """
            SELECT * FROM gifts
            WHERE gift_name = ?
        """
        row = CURSOR.execute(sql, (gift_name,)).fetchone()
        return cls.instance_from_db(row) if row else None
