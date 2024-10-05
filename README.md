# TDT4225 - Very Large Distributed Data Volumes

In this project, we analyzed a dataset about user movements from Microsoft for non-commercial use. The GPS trajectory dataset was collected in the Microsoft Research Asia Geolife project by 182 users over a period of more than five years (from April 2007 to August 2012). A GPS trajectory in this dataset is represented by a sequence of time-stamped points, each containing information on latitude, longitude, and altitude. This dataset contains 17,621 trajectories with a total distance of 1,292,951 kilometers and a total duration of 50,176 hours. These trajectories were recorded by different GPS loggers and GPS-phones, and have a variety of sampling rates. 91.5 percent of the trajectories are logged in a dense representation, e.g., every 1-5 seconds or every 5-10 meters per point.

## Work Completed

The goal of the project was to clean the data, insert it into a database, and perform SQL queries to uncover interesting findings.

## Structure

To read the data, the code includes three classes: `User`, `Activity`, and `Trackpoint`. To send data to the database, the classes `GeolifeProgram` and `DBConnector` are used. `scripy.py` is the file that is being used to insert data in the database

## Requirements

Run the following command to download the required packages:

```bash pip install -r requirements.txt bash```

To be able to run the code, the path of the data directory should be changed in dataextracter.py. Here the path should be changed to your local directory where you have your project.

Also, in `DBConnector.py`, the credidentials should be changed to get access to the database. These can be stored in an .env-file if using venv.

## Citations
[1] Yu Zheng, Lizhu Zhang, Xing Xie, Wei-Ying Ma. Mining interesting locations and travel sequences from GPS trajectories. In 
Proceedings of International conference on World Wild Web (WWW 2009), Madrid Spain. ACM Press: 791-800.  

[2] Yu Zheng, Quannan Li, Yukun Chen, Xing Xie, Wei-Ying Ma. Understanding Mobility Based on GPS Data. In Proceedings of 
ACM conference on Ubiquitous Computing (UbiComp 2008), Seoul, Korea. ACM Press: 312-321. 

[3] Yu Zheng, Xing Xie, Wei-Ying Ma, GeoLife: A Collaborative Social Networking Service among User, location and trajectory. 
Invited paper, in IEEE Data Engineering Bulletin. 33, 2, 2010, pp. 32-40. 

