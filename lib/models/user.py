from models.__init__ import CURSOR, CONN

class User:
    # Dictionary of objects saved to the database
    all = {}

    def __init__(self, user_id, username, full_name):
        self.user_id = user_id
        self._username = username
        self._full_name = full_name

    def __repr__(self):
        return f"<User {self.user_id}: {self._username}, {self._full_name}>"

    # Setting the username
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if isinstance(username, str) and len(username):
            self._username = username
        else:
            raise ValueError("Username must be a non-empty string")
        
    # Setting the full name
    @property
    def full_name(self):
        return self._full_name
    
    @full_name.setter
    def full_name(self, full_name):
        if isinstance(full_name, str) and len(full_name):
            self._full_name = full_name
        else:
            raise ValueError("Full name must be a non-empty string")

    # Creating the tables
    @classmethod
    def create_table(cls):
        SQL = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL
        );
        """
        CURSOR.execute(SQL)
        CONN.commit()

    @classmethod
    # Drops the table if it exists
    def drop_table(cls):
        """Drops the table if it exists"""
        SQL = "DROP TABLE IF EXISTS users;"
        CURSOR.execute(SQL)
        CONN.commit()

    # Instance method to save a user
    def save(self):
        """
        Inserts a new row with the values of the current User object
        Saves the instance to the database
        """
        SQL = """
        INSERT INTO users (username, full_name)
        VALUES (?, ?);
        """
        CURSOR.execute(SQL, (self._username, self._full_name))
        CONN.commit()

        self.user_id = CURSOR.lastrowid
        type(self).all[self.user_id] = self
    
    # Updating the table row
    def update(self):
        """
        Updates a row with the values of the current User object
        Saves the instance to the database
        """
        SQL = """
        UPDATE users
        SET username = ?, full_name = ?
        WHERE user_id = ?;
        """
        CURSOR.execute(SQL, (self._username, self._full_name, self.user_id))
        CONN.commit()
        
    # Deleting the table row
    def delete(self):
        """
        Deletes a row with the values of the current User object
        Saves the instance to the database
        """
        SQL = """
        DELETE FROM users
        WHERE user_id = ?;
        """
        CURSOR.execute(SQL, (self.user_id,))
        CONN.commit()

        # Deleting the dictionary entry using the user_id as the key
        del type(self).all[self.user_id]

        # Set the id to None
        self.user_id = None

    @classmethod
    # Creating a new User instance and save it to the database
    def create(cls, username, full_name):
        """
        Creates a new User instance and save it to the database
        """
        user = cls(None, username, full_name)
        user.save()
        return user
    
    # Returns a user instance corresponding to a database row, using the instance from the all dictionary if it exists
    @classmethod
    def instance_from_db(cls, row):
        # Check the dictionary for existing instances using the row's primary key
        user = cls.all.get(row[0])

        if user: 
            # Ensure attributes match row values in case local instance was modified
            user.username = row[1]
            user.full_name = row[2]
        else:
            # Not in dictionary, create new instance and add to the dictionary
            user = cls(row[0], row[1], row[2])
            cls.all[row[0]] = user
        return user

    @classmethod
    # Returns a list of all user instances from the database
    def get_all(cls):
        SQL = """
        SELECT * FROM users;
        """
        CURSOR.execute(SQL)
        rows = CURSOR.fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    # Finds and returns a user instance by its id
    def find_by_id(cls, user_id):
        SQL = """
        SELECT * FROM users
        WHERE user_id = ?;
        """
        row = CURSOR.execute(SQL, (user_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    # Finds and returns a user instance by its username
    def find_by_username(cls, username):
        SQL = """
        SELECT * FROM users
        WHERE username = ?;
        """
        row = CURSOR.execute(SQL, (username,)).fetchone()
        return cls.instance_from_db(row) if row else None
