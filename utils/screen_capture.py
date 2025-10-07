import mss
import mss.tools
import cv2 # For image processing and saving
import time
import numpy as np

# Window 1 Region
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} 

# Initialize mss
sct = mss.mss()

# Define how often to display/save (in seconds)
display_time = 1
start_time = time.time()
frame_count = 0
frame_count_name = 0
cap = "data/marksofgrace/cap4/"

while True:
    # Grab the image from the screen
    sct_img = sct.grab(monitor)

    # Convert the raw pixels to a NumPy array
    img_array = np.array(sct_img)
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # --- Option 1: Save the image directly to a file ---
    # Generate a unique filename, for example with a timestamp or frame number
    filename = f"{cap}{frame_count_name}.png"
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
    print(f"Saved {filename}")

    # --- Option 2: Display the captured image (for real-time view) ---
    # cv2.imshow("Screen Capture", img)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

    # Optional: Log FPS (frames per second)
    frame_count += 1
    if (time.time() - start_time) >= display_time:
        print(f"FPS: {frame_count / (time.time() - start_time)}")
        frame_count = 0
        start_time = time.time()
    
    frame_count_name += 1