# Python file with functions to extract data from the dataset, set labels to users and to activities.

import os
from Activity import Activity
from Trackpoint import Trackpoint
from User import User
from datetime import datetime

######### CHANGE THIS PATH TO YOUR OWN PATH #########
path = "/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset"
####################################################

# Function which goes through all the .tlp files in /assignment2_2024/dataset/dataset/Data, extract the data and create User, Activity and Trackpoint objects
def extract_data():
    # Get all directories in Data
    directories = os.listdir(path + "/Data")
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
                        activity = Activity(ID_Activity, directory, None , start_date_time, end_date_time)
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

# Function to set User.has_labels to True if the user has labels, going through the labeled_ids.txt file 
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

# Function which goes through all the "labels.txt" files in /assignment2_2024/dataset/dataset/Data and add the labels to the activities
def add_labels(users):
    directories = os.listdir(path + "/Data")
    
    # Filter out non-numeric files (like .DS_Store) and sort the numeric filenames
    numeric_directories = [directory for directory in directories if directory.isdigit()]
    sorted_directories = sorted(numeric_directories, key=lambda x: int(x))  # Sort numerically
    for directory in sorted_directories:
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
                    for line in lines[1:]:  # Skip header:
                        data = line.split("\t")
                        # Get data from labels.txt
                        start_time = datetime.strptime(data[0], "%Y/%m/%d %H:%M:%S")
                        end_time = datetime.strptime(data[1], "%Y/%m/%d %H:%M:%S")
                        transportation_mode = data[2]
                        for user in users:
                            if user.id == directory:
                                for activity in user.activities:
                                    # Scenario where the label is "inside" the activity
                                    if activity.start_date_time <= start_time and end_time <= activity.end_date_time:
                                        if (activity.durationlabel < (end_time - start_time).total_seconds()):
                                            activity.transportation_mode = transportation_mode
                                    # Scenario where the activity is "inside" the label
                                    elif start_time <= activity.start_date_time and  activity.end_date_time <= end_time:
                                        if (activity.durationlabel < (end_time - start_time).total_seconds()):
                                            activity.transportation_mode = transportation_mode
                    
                            
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
        for activity in user.activities:
            print(activity)
        if user == users[22]:
            break
                    


