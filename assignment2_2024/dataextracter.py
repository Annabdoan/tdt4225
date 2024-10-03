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

def extract_data():
    # Get all directories in Data
    directories = os.listdir("./tdt4225/assignment2_2024/dataset/dataset/Data")
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
        files = os.listdir(f"./tdt4225/assignment2_2024/dataset/dataset/Data/{directory}/Trajectory")
        # Filter out .DS_Store files
        files = [file for file in files if not file.startswith(".")]
        # Create a list to store all activities
        activities = []
        # Go through each file
        for file in files:
            # Check if the file is a .plt file
            if file.endswith(".plt"):
                # Open the file and read the content
                with open(f"./tdt4225/assignment2_2024/dataset/dataset/Data/{directory}/Trajectory/{file}", "r") as f:
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
        if (users.index(user) == 0):
            break
    # Return the list of users
    return users

# Make a function to set User.has_labels to True if the user has labels, going through the labeled_ids.txt file 
def set_has_labels(users):
    # Open file "labeled_ids.txt" and read the content
    with open("./tdt4225/assignment2_2024/dataset/dataset/labeled_ids.txt", "r") as file:
        labeled_ids = file.read().splitlines()
    # Go through each user
    for user in users:
        # Check if the user id is in labeled_ids
        if user.id in labeled_ids:
            # Set has_labels to True
            user.has_labels = True
    # Return the users
    return users

# Make a function which goes through all the users with labels, and for each activity, checks if the activity has labels from labels.txt
# If the activity has labels, set the activity.transportation_mode to the label
def set_labels():
    # Get all directories in Data
    directories = os.listdir("./tdt4225/assignment2_2024/dataset/dataset/Data")
    # Create a list to store all users
    users = []
    # Filter out non-numeric files (like .DS_Store) and sort the numeric filenames
    numeric_directories = [directory for directory in directories if directory.isdigit()]
    sorted_directories = sorted(numeric_directories, key=lambda x: int(x))  # Sort numerically
    ID_datapoints = 0
    ID_Activity = 0
    # Go through each directory
    for directory in sorted_directories:
        # Get all files in the directory using a for loop
        files = os.listdir(f"./tdt4225/assignment2_2024/dataset/dataset/Data/{directory}")
        # Filter out .DS_Store files
        files = [file for file in files if not file.startswith(".")]
        # Create a list to store all activities
        activities = []
        # Go through each file
        for file in files:
            # Check if the file is a .plt file
            if file.endswith(".plt"):
                # Open the file and read the content
                with open(f"./tdt4225/assignment2_2024/dataset/dataset/Data/{directory}/Trajectory/{file}", "r") as f:
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
        if (users.index(user) == 0):
            break
    # Return the list of users
    return users


users = extract_data()
users = set_has_labels(users)

# Printing the users, activities and trackpoints
for user in users[:1]:
    print(user)
    uservalue = user.get_data()
    for activity in user.activities:
        print(activity)


