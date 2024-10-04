from DbConnector import DbConnector
from dataextracter import *

class GeolifeProgram:
    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.users = extract_data()
        self.users = set_has_labels(users)
        self.users = add_labels(users)

    def create_tables(self):
        user_table = """CREATE TABLE IF NOT EXISTS User (
                            id VARCHAR(50) PRIMARY KEY,
                            has_labels BOOLEAN
                        )"""

        activity_table = """CREATE TABLE IF NOT EXISTS Activity (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id VARCHAR(50),
                            transportation_mode VARCHAR(30),
                            start_date_time DATETIME,
                            end_date_time DATETIME,
                            FOREIGN KEY (user_id) REFERENCES User(id)
                        )"""
        trackpoint_table = """CREATE TABLE IF NOT EXISTS Trackpoint (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            activity_id INT,
                            lat DOUBLE,
                            lon DOUBLE,
                            altitude INT,
                            date_days DOUBLE,
                            date_time DATETIME,
                            FOREIGN KEY (activity_id) REFERENCES Activity(id)
                        )"""

        self.cursor.execute(user_table)
        self.cursor.execute(activity_table)
        self.cursor.execute(trackpoint_table)
        self.db_connection.commit()

    def insert_user_data(self, table_name, user_id, has_labels):
        query = f"INSERT INTO {table_name} (id, has_labels) VALUES (%s, %s)"
        values = (user_id, has_labels)
        self.cursor.execute(query, values)
        self.db_connection.commit()

    def insert_activity_data(self, table_name, user_id, transportation_mode, start_date_time, end_date_time):
        query = "INSERT INTO %s (user_id, transportation_mode, start_date_time, end_date_time) VALUES ('%s', '%s', '%s', '%s')"
        values = (table_name, user_id, transportation_mode, start_date_time, end_date_time)
        self.cursor.execute(query, values)
        self.db_connection.commit()

    def insert_trackpoint_data(self, table_name, activity_id, lat, lon, altitude, date_days, date_time):
        query = "INSERT INTO %s (activity_id, lat, lon, altitude, date_days, date_time) VALUES (%d, %f, %f, %d, %f, '%s')"
        values = (table_name, activity_id, lat, lon, altitude, date_days, date_time)
        self.cursor.execute(query, values)
        self.db_connection.commit()
        # self.cursor.execute(query % (table_name, activity_id, lat, lon, altitude, date_days, date_time))

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print("Tables in the database:", rows)

    def drop_table(self, table_name):
        print("Dropping table %s..." % table_name)
        query = "DROP TABLE %s"
        self.cursor.execute(query % table_name)

    def close_connection(self):
        self.connection.close_connection()

def main():
    program = None
    try:
        program = GeolifeProgram()
        program.drop_table("Trackpoint")
        program.drop_table("Activity")
        program.drop_table("User")
        program.create_tables()
        users = extract_data()
        users = set_has_labels(users)
        users = add_labels(users)
        for user in users:
            user_data = user.get_data()
            user_id = user_data[0]
            has_labels = user_data[1]
            program.insert_user_data(table_name="User", user_id = user_id, has_labels = has_labels)
        program.show_tables()
    except Exception as e:
        print("ERROR: Failed to create tables:", e)
    finally:
        if program:
            program.close_connection()

if __name__ == "__main__":
    main()  # Run the program