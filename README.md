# Video-Motion-Detector
A program that detects objects in front of a camera and records time stamps as well for time of appearances.

Using OpenCV, the code is written to determine if there are objecs in the view of a laptop camera (can be adjusted for use with other external cameras as well).

An initial frame is captured by the camera, and the other proceeding frames are compared to see if they are above a given threshold . The status is set to 0 and changed to 1 each time an object is detected.
Time stamps are collected each time the status changes from 0 to 1 and theses are written to a .csv file called "Times.csv" using pandas. 
