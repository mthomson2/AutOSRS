import cv2
from ultralytics import YOLO
import mss
import time
import numpy as np
import math

MODEL_PATH = "runs/detect/train/weights/best.pt"

# Window 1 Region
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} 
center_screen = {"x": 960, "y": 540}

class WorkerMarks():

    def __init__(self):
        super().__init__()
        self.state = 0 # 0 = Green, 1 = Red
        self.marks = False # False = Marks not in screen
        self.closest = {"x": None, "y": None}
        self.reds = []
        self.greens = []
    
    def getCenter(self, x1, y1, x2, y2):
        cx = (x1+x2) // 2
        cy = (y1+y2) // 2
        center = (cx,cy)
        return center
    
    def get_closest_to_screen_center(self, points):
        sorted_coords = sorted(points, key=lambda p: (p[0] -  center_screen["x"])**2 + (p[1] - center_screen["y"])**2)
        return sorted_coords
        # closest_point = None
        # min_distance = float('inf')

        # for point_x, point_y in points:
        #     distance = math.sqrt((point_x - center_screen["x"])**2 + (point_y - center_screen["y"])**2)
        #     if distance < min_distance:
        #         min_distance = distance
        #         closest_point = (point_x, point_y)

        # return closest_point

    def run(self):
        model = YOLO(MODEL_PATH)

        # Initialize mss
        sct = mss.mss()

        # Define how often to display/save (in seconds)
        display_time = 1
        start_time = time.time()
        frame_count = 0
        frame_count_name = 0

        while True:
            # Grab the image from the screen
            frame = sct.grab(monitor)

            # Convert the raw pixels to a NumPy array
            img_array = np.array(frame)
            # Remove Alpha Channel
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

            # YOLO Detection Here
            # Perform inference on the frame
            results = model.predict(img_array, conf=0.3, iou=0.5, stream=True, verbose=False)
            
            # Process and visualize results
            red_box_centers = []
            green_box_centers = []
            for r in results:
                box_centers = []
                annotated_frame = r.plot() # YOLOv8's built-in plotting function
                cv2.imshow("YOLOv8 Real-time Detection", annotated_frame)

                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist() # Get bounding box coordinates
                    center_x, center_y = self.getCenter(x1, y1, x2, y2)

                    box_centers.append((center_x,center_y))

                    if (box.cls[0] == 0):
                        self.marks = True
                        red_box_centers.append((center_x,center_y))
                    else:
                        self.marks = False

                    if (box.cls[0] == 2):
                        self.state = 1
                        red_box_centers.append((center_x,center_y))

                    if (box.cls[0] == 1):
                        green_box_centers.append((center_x,center_y))
                        self.state = 0
                    # print(f"Class: {box.cls[0]}    Center: ({center_x}, {center_y})")
            
            # Compute Closest Red/Marks box
            self.reds = self.get_closest_to_screen_center(red_box_centers)
            self.greens = self.get_closest_to_screen_center(green_box_centers)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
