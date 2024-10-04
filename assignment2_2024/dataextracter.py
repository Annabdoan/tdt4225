import os
from Activity import Activity
from Trackpoint import Trackpoint
from User import User
from datetime import datetime

# Make me a function which goes through all the directories in assignment2_2024/dataset/dataset/Data and add a user for each folder
# The user should have the same id as the directory and the activities should be added to the user
# The activities should have the same id as the directory and the trackpoints should be added to the activities
# The trackpoints should have the same id as the directory
# The start_date_time and end_date_time should be the earliest and latest time from the trackpoints

path = "/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset"

def extract_data():
    # Get all directories in Data
    directories = os.listdir(path)
    # Create a list to store all users
    users = []
    # Filter out non-numeric files (like .DS_Store) and sort the numeric filenames
    numeric_directories = [directory for directory in directories if directory.isdigit()]
    sorted_directories = sorted(numeric_directories, key=lambda x: int(x))  # Sort numerically
    ID_datapoints = 0
    ID_Activity = 0
    # Go through each directory
    for directory in sorted_directories:
        # Create a new user with the id of the directory
        user = User(directory, False)
        # Get all files in the directory using a for loop
        files = os.listdir(path + f"/Data/{directory}/Trajectory")
        # Filter out .DS_Store files
        files = [file for file in files if not file.startswith(".")]
        # Create a list to store all activities
        activities = []
        # Go through each file
        for file in files:
            # Check if the file is a .plt file
            if file.endswith(".plt"):
                # Open the file and read the content
                with open(path + f"/Data/{directory}/Trajectory/{file}", "r") as f:
                    lines = f.read().splitlines()
                    # Checks if the file is longer 2507 linees and yes, skips the file
                    if len(lines) <= 2506:
                        # Get the start and end date time from the first and last trackpoints
                        start_date_time = datetime.strptime(lines[7].split(',')[-2] + " " + lines[7].split(',')[-1], "%Y-%m-%d %H:%M:%S")
                        end_date_time = datetime.strptime(lines[-1].split(',')[-2] + " " + lines[-1].split(',')[-1], "%Y-%m-%d %H:%M:%S")
                        # Create a new activity with the id of the directory
                        activity = Activity(ID_Activity, directory, "Unknown", start_date_time, end_date_time)
                        ID_Activity += 1
                        # Create a list to store all trackpoints
                        trackpoints = []
                        # Go through each line in the file, dropping the first part of the file
                        for line in lines[6:]:
                            # Split the line by comma
                            data = line.split(",")
                            # Create a new trackpoint
                            date_time = datetime.strptime(data[5] + " " + data[6], "%Y-%m-%d %H:%M:%S")
                            trackpoint = Trackpoint(ID_datapoints, ID_Activity, data[0], data[1], data[3], date_time)
                            ID_datapoints += 1
                            # Add the trackpoint to the list
                            trackpoints.append(trackpoint)
                        # Set the trackpoints for the activity
                        activity.trackpoints = trackpoints
                        # Add the activity to the list
                        activities.append(activity)
                
        # Set the activities for the user
        user.activities = activities
        # Add the user to the list
        users.append(user)
    # Return the list of users
    return users

# Make a function to set User.has_labels to True if the user has labels, going through the labeled_ids.txt file 
def set_has_labels(users):
    # Open file "labeled_ids.txt" and read the content
    with open(path + "/labeled_ids.txt", "r") as file:
        labeled_ids = file.read().splitlines()
    # Go through each user
    for user in users:
        # Check if the user id is in labeled_ids
        if user.id in labeled_ids:
            # Set has_labels to True
            user.has_labels = True
    # Return the users
    return users

# Make a function which goes through all the "labels.txt" files in /assignment2_2024/dataset/dataset/Data and add the labels to the activities
# If starttime in activity is between start_time and end_time in the label, set the activity.transportation_mode
def add_labels(users):
    # Get all directories in Data
    directories = os.listdir(path + "/Data")
    # Filter out non-numeric files (like .DS_Store) and sort the numeric filenames
    numeric_directories = [directory for directory in directories if directory.isdigit()]
    sorted_directories = sorted(numeric_directories, key=lambda x: int(x))  # Sort numerically
    # Go through each directory
    for directory in sorted_directories:
        # Get all files in the directory using a for loop
        files = os.listdir(path + f"/Data/{directory}")
        # Filter out .DS_Store files
        files = [file for file in files if not file.startswith(".")]
        # Go through each file
        for file in files:
            # Check if the file is a labels.txt file
            if file == "labels.txt":
                # Open the file and read the content
                with open(path + f"/Data/{directory}/{file}", "r") as f:
                    lines = f.read().splitlines()
                    # Go through each line
                    for line in lines[1:]:  # Skip header:
                        # Split the line by comma
                        data = line.split("\t")
                        # Get the start and end time
                        start_time = datetime.strptime(data[0], "%Y/%m/%d %H:%M:%S")
                        end_time = datetime.strptime(data[1], "%Y/%m/%d %H:%M:%S")
                        # Get the transportation mode
                        transportation_mode = data[2]
                        # Go through each user
                        for user in users:
                            # Go through each activity
                            for activity in user.activities:
                                # Check if the activity is within the start and end time
                                if activity.start_date_time <= start_time and end_time <= activity.end_date_time:
                                    if (activity.transportation_mode == "Unknown"):
                                        activity.transportation_mode = transportation_mode
                                    else:
                                        activity.transportation_mode = "Multiple"
                                elif start_time <= activity.start_date_time and  activity.end_date_time <= end_time:
                                    if (activity.transportation_mode == "Unknown"):
                                        activity.transportation_mode = transportation_mode
                                    else:
                                        activity.transportation_mode = "Multiple"
                            
    # Return the users
    return users

if __name__ == "__main__":
    # Extract the data
    users = extract_data()
    # Set has_labels to True for the users with labels
    users = set_has_labels(users)
    # Add the labels to the activities
    users = add_labels(users)
    # Printing the users, activities and trackpoints
    for user in users:
        print(user)
        # uservalue = user.get_data()
        if user == users[22]:
            for activity in user.activities:
                for trackpoint in activity.trackpoints:
                    print(trackpoint)


