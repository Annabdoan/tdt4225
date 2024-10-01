class ProgramQueries:
    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def query1(self):
    ## How many users, activities and trackpoints there are in the dataset
    ## Assuming each user, activity and  has a unique id
        query_users = """SELECT COUNT(DISTINCT id) FROM User"""
    
        query_activity = """SELECT COUNT(DISTINCT id) FROM Activity"""
        
        query_trackpoint = """SELECT COUNT(DISTINCT id) FROM Trackpoint"""
        
        self.cursor.execute(query_users)
        users = self.cursor.fetchall()

        self.cursor.execute(query_activity)
        activities = self.cursor.fetchall()

        self.cursor.execute(query_trackpoint)   
        trackpoints = self.cursor.fetchall()

        users_count = users[0][0]
        activities_count = activities[0][0]
        trackpoints_count = trackpoints[0][0]

        print("Number of users:", users_count, "Number of activities:", activities_count, "Number of trackpoints:", trackpoints_count)
        return users, activities, trackpoints

    
    def query2(self):
    # Find the average number of activities per user
        query = """
                SELECT AVG(activities_per_user) 
                FROM (SELECT COUNT(id) AS activities_per_user 
                    FROM Activity 
                    GROUP BY user_id) AS user_activity_count
                """
        
        self.cursor.execute(query)
        avg_activities = self.cursor.fetchone()[0]  # Extract the first value
        print("Average number of activities per user:", avg_activities)
        return avg_activities


    def query3(self):
    # The top 20 users with the highest number of activities
        query = """
                SELECT user_id, COUNT(id) AS activity_count 
                FROM Activity 
                GROUP BY user_id 
                ORDER BY activity_count DESC 
                LIMIT 20
                """
        
        self.cursor.execute(query)
        top_20_users = self.cursor.fetchall()

        # Print the top 20 users with the highest number of activities
        print("Top 20 users with the highest number of activities:")
        for idx, (user_id, activity_count) in enumerate(top_20_users, 1):
            print(f"{idx}. User id: {user_id}, Number of activities: {activity_count}")
        
        return top_20_users

    
    def query4(self):
    # All users who have taken a taxi
        query = """
                SELECT DISTINCT user_id 
                FROM Activity 
                WHERE transportation_mode = 'taxi'
                """
        
        self.cursor.execute(query)
        taxi_users = self.cursor.fetchall()

        # Print the users who have taken a taxi
        print("Users who have taken a taxi:")
        for idx, (user_id,) in enumerate(taxi_users, 1):
            print(f"{idx}. User id: {user_id}")
        
        return taxi_users

    
    def query5(self):
        #####TODO 5#####

            
        

