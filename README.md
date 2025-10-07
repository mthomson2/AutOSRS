# AutOSRS
A totally legal and ethical approach to Old School Runescape 

# Current Skill Support
### 1. Agility - Canifis Course 
### 2. Others In Progress

# How It Works

AutOSRS is currently a computer vision application that utilizes pyautogui to simulate clicks on the screen. It uses two computer vision models localize clicks and functionality:

1. Classification Model: Feed-forward Convolutional Neural Network (CNN)
    * Classifies buildings and ground floor 
    * Classes: classes = ('block1', 'block2', 'block3', 'block4',
           'block5', 'block6', 'block7', 'tree', 'floor')
    * Model: [osrs_net.pth](models/osrs_net.pth)
    * See [prepare_dataset.py](utils/prepare_dataset.py) for training code

2. Object Detection Model: YOLO 
    * Detects the clickable parts of the agility course 
    * Classes: ('marks', 'redboxes', 'greenboxes', 'tree')
    * Model: [best.pt](runs/detect/train/weights/best.pt)
    * YOLO CLI: `yolo task=detect mode=train model=yolov8s.pt data=data/marks_of_grace_dataset/marks.yaml epochs=100 batch=8 imgsz=640 device=0` 

This application currently assumes the PC starts at Block 0 (the first building after the tree climb). It will then progress throughout the course by detecting Red Boxes, Green Boxes, and Marks of Grace. There is Fall Support (for the fail possiblity between Block 2 and 3), and a reset mechanism for when the player gets stuck. 

# How to Use
Although this can be an extremely efficient method to training, it does require a specific setup. Be sure to follow all guidelines carefully. 

1. This is a two-screen setup. If you don't have at least two windows, this could be difficult to run. (Not tested).
    * This program assumes a 1920x1080 resolution on Window 1. There is currently no support for other resolutions or screens. 
2. You must start OSRS with RuneLite or another client that will highlight the jump locations in Green or Red boxes. 
    * Ensure RuneLite client is on Window 1 and fully maximized. 
3. Ensure Python and Pip are installed
4. Open your terminal of choice and clone this repository to your preferred location. 
5. Create a virtual environment (conda, virtualenv, etc.)
    * <i> e.g. python -m venv myenv</i>
6. Activate your environment
    * <i>e.g. ./myenv/Scripts/activate</i>
7. Install requirements 
    * `pip install -r requirements.txt`
8. Start AutOSRS
    * `python autosrs.py` 

This will start the program. OpenCV will open up a separate window to display detections. Make sure you move this separate window to Window 2 so it doesn't interfere with the computer vision. 