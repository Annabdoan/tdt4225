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
    directories = os.listdir("/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/Data")
    # Create a list to store all users
    users = []
    # Go through each directory
    for directory in directories:
        # Create a new user with the id of the directory
        user = User(directory, False)
        # Get all files in the directory using a for loop
        files = os.listdir(f"/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/Data/{directory}")
        # Create a list to store all activities
        activities = []
        # Go through each file
        for file in files:
            # Check if the file is a .plt file
            if file.endswith(".plt"):
                # Open the file and read the content
                with open(f"/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/Data/{directory}/{file}", "r") as f:
                    lines = f.read().splitlines()
                    # Get the start and end date time
                    start_date_time = datetime.strptime(lines[6], "Start Time: %Y-%m-%d %H:%M:%S")
                    end_date_time = datetime.strptime(lines[-1], "%Y-%m-%d %H:%M:%S")
                    # Create a new activity with the id of the directory
                    activity = Activity(directory, directory, "Unknown", start_date_time, end_date_time)
                    # Create a list to store all trackpoints
                    trackpoints = []
                    # Go through each line in the file
                    for line in lines[6:]:
                        # Split the line by comma
                        data = line.split(",")
                        # Create a new trackpoint
                        trackpoint = Trackpoint(directory, data[0], data[1], data[3], data[4], data[5], data[6])
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
    with open("/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/labeled_ids.txt", "r") as file:
        labeled_ids = file.read().splitlines()
    # Go through each user
    for user in users:
        # Check if the user id is in labeled_ids
        if user.id in labeled_ids:
            # Set has_labels to True
            user.has_labels = True
    # Return the users
    return users

users = extract_data()
users = set_has_labels(users)
for user in users:
    print(user)


# # Open file "labeled_ids.txt" and read the content
# with open("/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/labeled_ids.txt", "r") as file:
#     labeled_ids = file.read().splitlines()
#     print(labeled_ids)
#     # Only keep directories that are in labeled_ids
#     directories = [d for d in os.listdir("/Users/andreasbuervase/Desktop/4.klasse Indøk/Store, distribuerte datamengder/Group project/tdt4225/assignment2_2024/dataset/dataset/Data") if d in labeled_ids]
#     # Check if the two lists are identical
#     are_identical = sorted(labeled_ids) == sorted(directories)
#     print(are_identical)

