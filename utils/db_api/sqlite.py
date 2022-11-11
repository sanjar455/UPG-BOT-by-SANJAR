from pickletools import string1
import sqlite3


class Database:
<<<<<<< HEAD
    def __init__(self, path_to_db="D:/sanjar/data/UPGBot/data/main.db"):
=======
    def __init__(self, path_to_db="D:/BOT/UPGBot/main.db"):
>>>>>>> ae1d5241c341c01fd52cccf98bc1e286901da43b
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER NOT NULL UNIQUE,
            full_name VARCHAR(100) NOT NULL,
            username TEXT UNIQUE,
            phone_number VARCHAR(20),
            language_code VARCHAR(5)
        );"""
        self.execute(sql, commit=True)

    def create_category_table(self):
        sql = """
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY,
            title VARCHAR(30) NOT NULL,
            slug VARCHAR(30) NOT NULL,
            image_url TEXT
        );"""
        self.execute(sql, commit=True)
    

    def create_sub_category_table(self):
        sql = """
        CREATE TABLE Subcategory (
            id INTEGER PRIMARY KEY,
            title VARCHAR(30) NOT NULL,
            slug VARCHAR(30) NOT NULL,
            image_url TEXT,
            category_id INTEGER NOT NULL
        );"""
        self.execute(sql, commit=True)


    def create_product_table(self):
        sql = """
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY,
            title VARCHAR(30) NOT NULL,
            slug VARCHAR(30) NOT NULL,
            desc TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT,
            info_url TEXT,
            subcategory_id INTEGER NOT NULL
        );"""
        self.execute(sql, commit=True)

    def create_cart_table(self):
        sql = """
        CREATE TABLE Cart (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            amount INTEGER NOT NULL
        );"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, tg_id: int, full_name: str, username: str):
        sql = """
        INSERT INTO Users(tg_id, full_name, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, full_name, username), commit=True)

    def add_product(self, tg_id: int, product_id: int, amount: int):
        sql1 = """SELECT * FROM Cart WHERE product_id=? AND tg_id=?"""
        res = self.execute(sql1, parameters=(product_id, tg_id), fetchone=True)
        print("*" * 20, res, "*" * 20)
        if res:
            amount += res[-1]
            tg_id = res[1]
            product_id = res[-2]
            sql = f"""
            UPDATE Cart SET amount=? WHERE tg_id=? AND product_id=?
            """
            return self.execute(sql, parameters=(amount, tg_id, product_id), commit=True)
        else:
            sql = """
            INSERT INTO Cart(tg_id, product_id, amount) VALUES(?, ?, ?)
            """
            self.execute(sql, parameters=(tg_id, product_id, amount), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_cats(self):
        sql = """
        SELECT * FROM Category
        """
        return self.execute(sql, fetchall=True)

    def get_category_info(self, **kwargs):
        sql = """
        SELECT id,title,slug,image_url FROM Category WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_cart_items(self, **kwargs):
        sql = """
        SELECT * FROM Cart WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_product_info(self, **kwargs):
        sql = """
        SELECT * FROM Product WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_sub_cats_by_cat_id(self, **kwargs):
        sql = """SELECT title, slug FROM Subcategory WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_sub_category_info(self, **kwargs):
        sql = """
        SELECT id,title,slug,image_url FROM Subcategory WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_products_by_sub_cat_id(self, **kwargs):
        sql = """SELECT title, slug FROM Product WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def search_products(self, query):
        sql = f"SELECT * FROM Product WHERE title LIKE '%{query}%' OR desc LIKE '%{query}%'"
        return self.execute(sql, fetchall=True)

    def get_product_info(self, **kwargs):
        sql = """
        SELECT * FROM Product WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    # def update_user_email(self, email, id):
    #     # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

    #     sql = f"""
    #     UPDATE Users SET email=? WHERE id=?
    #     """
    #     return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    def delete_product_cart(self, **kwargs):
        sql = "DELETE FROM Cart WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
