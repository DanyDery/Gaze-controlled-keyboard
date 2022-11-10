# Gaze_Controlled_Keyboard

Project where we will control the keyboard through our eyes using Python with Opencv

## Table of Content:
* [Overview](https://github.com/DanyDery/Gaze-controlled-keyboard#Overview)
* [Motivation](https://github.com/DanyDery/Gaze-controlled-keyboard#Motivation)
* [Core-Logic](https://github.com/DanyDery/Gaze-controlled-keyboard#Core-Logic)
* [Inspiration From](https://github.com/DanyDery/Gaze-controlled-keyboardd#Inspiration-From)


## Overview 
The “Gaze controlled keyboard” is a project where we will control the keyboard through our eyes using Python with Opencv, completely from scratch.The goal of such app is to write without using the hands. 
![alt text](https://www.mdpi.com/sensors/sensors-19-03630/article_deploy/html/images/sensors-19-03630-g001-550.jpg)

## Motivation 
To implement the technology for a better tomorrow is the motivation for this project.
I came across Opencv and read about it through various blogs on it. Thus the zeal to work on opencv sparked within me and the idea to  create the virtual keyboard which could be controlled by our gaze without using the hands.Such applications are really important for people affected by quadriplegia who completely lost the control of their limbs.

## Core-Logic
This project is built in 2 main parts.
  * Eye detection: detection of the eyes, their movement and most important their blinking.
  * Virtual keyboard: a keyboard on the screen where we’re going to select the letters by just using our eyes.

### 1.1Eye detection
We are taking the frames in real time from the webcam, so to detect the eyes we will use face landmarks detection approach. We can find 68 specific landmarks of the face. To each point there is a specific index assigned.
We will use the following landmark points to detect the eye.

* Left eye points: (36, 37, 38, 39, 40, 41)
* Right eye points: (42, 43, 44, 45, 46, 47)

![landmarks_points_eyes](https://user-images.githubusercontent.com/44902363/85774006-10714180-b73c-11ea-93ff-542ff0a70958.png)

### 1.2 Detecting the blinking
When we detected the eye, we also detected two lines: an horizontal line and a vertical line crossing the eye.

It can be seen that the size of the horizontal line is almost the same for the closed and open eyes, while the vertical line for the open eye is much longer.

We will take horizontal line as the point of reference, and from this we calculate the ratio in comparison with the vertical line.
If this ratio is more than 5.7 than the eyes are blinking otherwise they are open.

### 1.3 Gaze Detection

What at a first glance is really clear, by looking at the image above, it’s that the sclera (white part of the eye) fills the right part of the eye when the eye is looking at the left, the opposite happens when it’s looking to the right and when it’s looking to the center the white is well balanced between left and right.

The idea is to split the eye in two parts and to find out in which of the two parts there is more sclera visible.

![eye_splitted](https://user-images.githubusercontent.com/44902363/85776329-3b5c9500-b73e-11ea-9f67-c91a6c61cbb1.png)

If the sclera is more visible on the right part, so the eye is looking at the left (our left) like in this case.Technically to detect the sclera we convert the eye into grayscale, we find a treshold and we count the white pixels.

We divide the white pixels of the left part and those of the right part and we get the gaze ratio. If the gaze ratio is smaller than 1 when looking to the right side and greater than 1.7 when the eyes are looking to the left side.

Eye-Aspect-Ratio (EAR)
You will see that Eye-Aspect-Ratio is the simplest and the most elegant feature that takes good advantage of the facial landmarks. EAR helps us in detecting blinks and winks etc.
You can see that the EAR value drops whenever the eye closes. We can train a simple classifier to detect the drop. However, a normal if condition works just fine. 

You can see that the EAR value drops whenever the eye closes. We can train a simple classifier to detect the drop. However, a normal if condition works just fine. Something like this:

Mouth-Aspect-Ratio (MAR)
Highly inspired by the EAR feature, I tweaked the formula a little bit to get a metric that can detect open/closed mouth. Unoriginal but it works.  

Computationally similar to EAR, MAR measures the ratio of mouth length to mouth width.
We will also define the reference points of the nose and change its position

The model offers two important functions. A detector to detect the face and a predictor to predict the landmarks. The face detector used is made using the classic Histogram of Oriented Gradients (HOG) feature combined with a linear classifier, an image pyramid, and sliding window detection scheme. 

### 2.1 Virtual Keyboard and Mouse

The idea is to display the Keys on the screen and light them up one at time. Once the key we want to press is lighted up, we simply would need to close our eyes and the key will be pressed.

Using numpy and cv2 we will create a simple keyboard 

 - Squinting your eyes (**squint** - To look with the eyes partly closed, as in bright sunlight)
 - Winking
 - Moving your head around (pitch and yaw)
 - Opening your mouth (a little bit, yes)

### 2.2 Light up letters each 10 frames
Basically we are lighting up a letter for 10 frames, and after that we light up the next one, so that when we reach the letter we want to press, we simply close our eyes and it gets pressed.

At this point, you are forced to work with the facial movements I chose but I am working on making them configurable. The list of actions include:

**Final result**

You can get the trained model file from http://dlib.net/files, click on **shape\_predictor\_68\_face\_landmarks.dat.bz2**. The model dat file has to be in the model folder.

Note: The license for the iBUG 300-W dataset excludes commercial use. So you should contact Imperial College London to find out if it's OK for you to use this model file in a commercial product.

## Inspiration From

* Pyscource [blogs](https://pysource.com/category/tutorials/gaze-controlled-keyboard/) by Sergio Canu
g
* Tereza Soukupova´ and Jan Cˇ ech. _[Real-Time Eye Blink Detection using Facial Landmarks](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)_. In 21st Computer Vision Winter Workshop, February 2016.

* Adrian Rosebrock. _[Detect eyes, nose, lips, and jaw with dlib, OpenCV, and Python](https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/)_. 

* Adrian Rosebrock. _[Eye blink detection with OpenCV, Python, and dlib](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)_.

* Vahid Kazemi, Josephine Sullivan. _[One millisecond face alignment with an ensemble of regression trees](https://ieeexplore.ieee.org/document/6909637)_. In CVPR, 2014.

* S. Zafeiriou, G. Tzimiropoulos, and M. Pantic. _[The 300 videos in the wild (300-VW) facial landmark tracking in-the-wild challenge](http://ibug.doc.ic.ac.uk/resources/300-VW/.3)_. In ICCV Workshop, 2015. 

* C. Sagonas, G. Tzimiropoulos, S. Zafeiriou, M. Pantic. _[300 Faces in-the-Wild Challenge: The first facial landmark localization Challenge](https://ibug.doc.ic.ac.uk/media/uploads/documents/sagonas_iccv_2013_300_w.pdf)_. Proceedings of IEEE Int’l Conf. on Computer Vision (ICCV-W), 300 Faces in-the-Wild Challenge (300-W). Sydney, Australia, December 2013

* Adrian Rosebrock. *Imutils*. [https://github.com/jrosebr1/imutils](https://github.com/jrosebr1/imutils).

* Akshay Chandra Lagandula. *Mouse Cursor Control Using Facial Movements*. [https://towardsdatascience.com/c16b0494a971](https://towardsdatascience.com/c16b0494a971).


#### Danylo Derevianskyi (DanyDery)

<a href="https://www.linkedin.com/in/daniel-dear"><img src="https://cdn2.iconfinder.com/data/icons/simple-social-media-shadow/512/14-512.png" align="left" height="60" width="60" ></a>
