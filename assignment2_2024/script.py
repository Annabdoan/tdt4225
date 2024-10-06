# 
from DbConnector import DbConnector
from dataextracter import *
import time
import sys

class GeolifeProgram:
    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.max_packet_size = self.get_max_allowed_packet()

    def create_tables(self):
        user_table = """CREATE TABLE IF NOT EXISTS User (
                            id VARCHAR(50) PRIMARY KEY,
                            has_labels BOOLEAN
                        )"""
        activity_table = """CREATE TABLE IF NOT EXISTS Activity (
                            id INT PRIMARY KEY,
                            user_id VARCHAR(50),
                            transportation_mode VARCHAR(30),
                            start_date_time DATETIME,
                            end_date_time DATETIME,
                            FOREIGN KEY (user_id) REFERENCES User(id)
                        )"""
        trackpoint_table = """CREATE TABLE IF NOT EXISTS Trackpoint (
                            id INT PRIMARY KEY,
                            activity_id INT,
                            lat DOUBLE,
                            lon DOUBLE,
                            altitude INT,
                            date_time DATETIME,
                            FOREIGN KEY (activity_id) REFERENCES Activity(id)
                        )"""

        self.cursor.execute(user_table)
        self.cursor.execute(activity_table)
        self.cursor.execute(trackpoint_table)
        self.db_connection.commit()

    def insert_user_data_batch(self, table_name, user_data_list):
        self.batch_insert(table_name, user_data_list, "id, has_labels", 2)

    def insert_activity_data_batch(self, table_name, activity_data_list):
        self.batch_insert(table_name, activity_data_list, "id, user_id, transportation_mode, start_date_time, end_date_time", 5)

    def insert_trackpoint_data_batch(self, table_name, trackpoint_data_list):
        self.batch_insert(table_name, trackpoint_data_list, "id, activity_id, lat, lon, altitude, date_time", 6)

    def batch_insert(self, table_name, data_list, columns, num_columns):
        query = f"INSERT INTO {table_name} ({columns}) VALUES (%s" + ", %s" * (num_columns - 1) + ")"
        batch = []
        current_batch_size = 0
        
        for data in data_list:
            # Estimate size of the row (each field's size)
            row_size = sum([sys.getsizeof(str(d)) for d in data])
            
            if current_batch_size + row_size > self.max_packet_size:
                # If adding this row would exceed the packet size, commit current batch
                self.cursor.executemany(query, batch)
                self.db_connection.commit()
                batch = []
                current_batch_size = 0
            
            # Add row to batch
            batch.append(data)
            current_batch_size += row_size
        
        # Insert remaining data
        if batch:
            self.cursor.executemany(query, batch)
            self.db_connection.commit()

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print("Tables in the database:", rows)

    def drop_table(self, table_name):
        """ Drops a table if it exists. """
        print(f"Dropping table {table_name}...")
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)

    def get_max_allowed_packet(self):
        query = "SHOW VARIABLES LIKE 'max_allowed_packet'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print(f"max_allowed_packet: {result[1]} bytes")
        return int(result[1])  # Return the packet size as an integer

    def close_connection(self):
        self.connection.close_connection()

def main():
    program = None
    try:
        start_time = time.time()
        program = GeolifeProgram()
        program.drop_table("Trackpoint")
        program.drop_table("Activity")
        program.drop_table("User")
        program.create_tables()
        program.show_tables()

        users = extract_data()
        users = set_has_labels(users)
        users = add_labels(users)

        # Prepare lists to hold batch data
        for user in users:
            user_data_list = []
            activity_data_list = []
            trackpoint_data_list = []
            usercreatetime = time.time()

            user_data = user.get_data()
            user_id = user_data[0]
            has_labels = user_data[1]
            user_data_list.append((user_id, has_labels))

            for activity in user.activities:
                activity_data = activity.get_data()
                activity_id = activity_data[0]
                activity_data_list.append((activity_id, user_id, activity_data[2], activity_data[3], activity_data[4]))

                for trackpoint in activity.trackpoints:
                    trackpoint_data = trackpoint.get_data()
                    trackpoint_id = trackpoint_data[0]
                    trackpoint_data_list.append((trackpoint_id, activity_id, trackpoint_data[2], trackpoint_data[3], trackpoint_data[4], trackpoint_data[5]))

            program.insert_user_data_batch("User", user_data_list)
            program.insert_activity_data_batch("Activity", activity_data_list)
            program.insert_trackpoint_data_batch("Trackpoint", trackpoint_data_list)

            # Commit after batch insertion
            program.db_connection.commit()
            usercreatetime = time.time() - usercreatetime

            print(f"User {user_id} inserted in {usercreatetime:.2f} seconds")

        program.show_tables()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to run main program: {elapsed_time:.2f} seconds")

    except Exception as e:
        print("ERROR: Failed to insert data:", e)
    finally:
        if program:
            program.close_connection()

if __name__ == "__main__":
    main()