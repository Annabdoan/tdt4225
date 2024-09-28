from DbConnector import DbConnector

class GeolifeProgram:
    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

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
        program.show_tables()
    except Exception as e:
        print("ERROR: Failed to create tables:", e)
    finally:
        if program:
            program.close_connection()

if __name__ == "__main__":
    main()  # Run the program