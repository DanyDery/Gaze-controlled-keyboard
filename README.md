# Gaze-controlled-keyboard

First, we identify our face in real time using the Dlib library.
Let's move on to calling the shape_predictor_68_face_landmarks.dat file, which will be used to determine the points on our face.
![alt text](https://ibug.doc.ic.ac.uk/media/uploads/images/annotpics/figure_68_markup.jpg)
By capturing real-time footage from the webcam, once a face is detected, you can move on to eye detection.
Using the face landmark detection approach, we can find 68 specific facial landmarks.
Each point is assigned a specific index. We need to find reference coordinates for the two eyes:
Points for the left eye: (36, 37, 38, 39, 40, 41);
Points for the right eye: (42, 43, 44, 45, 46, 47).

Let's create two lines:
one crossing the eye horizontally, the second - vertically.
It can be seen that the size of the horizontal line is almost the same for the closed and open eyes, while the vertical line for the open eye is much longer.

Let's take the horizontal line as a reference point and calculate the ratio compared to the vertical line.
If the ratio falls below a certain number, we will assume that the eye is closed, otherwise it is open.


Computationally similar to EAR, MAR measures the ratio of mouth length to mouth width.
We will also define the reference points of the nose and change its position
