from DbConnector import DbConnector
import os

class GeolifeProgram:
    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.users = os.listdir("./dataset/dataset/Data")
        self.users = sorted([user for user in self.users if user.isdigit()], key=lambda x: int(x))
        self.labels = open("./dataset/dataset/labeled_ids.txt", "r").read().split("\n")


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

        print("Tables user, activity and trackpoint created")
        print(self.users)
        print("Lable table: ", self.labels)

    def insert_user_data(self, table_name):
        for user_id in self.users:
            if user_id in self.labels:
                query = "INSERT INTO %s (id, has_labels) VALUES ('%s', True)"
                self.cursor.execute(query % (table_name, user_id))
            else:
                query = "INSERT INTO %s (id, has_labels) VALUES ('%s', False)"
                self.cursor.execute(query % (table_name, user_id))
        self.db_connection.commit()

    def insert_activity_data(self, table_name):
        query = "INSERT INTO %s (user_id, transportation_mode, start_date_time, end_date_time) VALUES ('%s', '%s', '%s', '%s')"
        # self.cursor.execute(query % (table_name, user_id, transportation_mode, start_date_time, end_date_time))


    def insert_trackpoint_data(self, table_name):
        query = "INSERT INTO %s (activity_id, lat, lon, altitude, date_days, date_time) VALUES (%d, %f, %f, %d, %f, '%s')"
        # self.cursor.execute(query % (table_name, activity_id, lat, lon, altitude, date_days, date_time))

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print("Tables in the database:", rows)

    def close_connection(self):
        self.connection.close_connection()

def main():
    program = None
    try:
        program = GeolifeProgram()
        program.create_tables()
        program.insert_user_data(table_name="User")
        # program.insert_activity_data(table_name="Activity")
        # program.insert_trackpoint_data(table_name="Trackpoint")
        program.show_tables()
    except Exception as e:
        print("ERROR: Failed to create tables:", e)
    finally:
        if program:
            program.close_connection()

if __name__ == "__main__":
    main()  # Run the program