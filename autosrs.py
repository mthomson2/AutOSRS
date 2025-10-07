from worker import Worker
from worker_marks import WorkerMarks
import threading
import time
import pyautogui

worker = Worker()
worker_marks = WorkerMarks()

def start_worker():
    # Get the Worker to run the model and provide inference
    worker.run()

def start_worker_marks():
    # Get the Worker to run the model and provide inference
    worker_marks.run()

# Returns next building number
def handler(wm_state, g_boxes, r_boxes, box_index, build_index, build_index_next, timer):
    print(f"Block: {build_index}")
    # Get closest Green box
    if (wm_state == 0):
        try:
            closest_x, closest_y = g_boxes[box_index]
        except IndexError as e:
            print(e)
            if (box_index == 1):
                closest_x, closest_y = g_boxes[0]
            else:
                pyautogui.click(x=960, y=500)
                pyautogui.click(x=960, y=500)
                time.sleep(2) 
                return build_index
        pyautogui.click(x=closest_x, y=closest_y)
        pyautogui.click(x=closest_x, y=closest_y)
        time.sleep(timer)
        current_building = build_index_next
    else: 
        try:
            closest_x, closest_y = r_boxes[box_index]
        except IndexError as e:
            print(e)
            if (box_index == 1):
                closest_x, closest_y = r_boxes[0]
            else:
                pyautogui.click(x=960, y=500)
                pyautogui.click(x=960, y=500)
                time.sleep(2) 
                return build_index
            return build_index
        # If mark is on screen. go to next red
        pyautogui.click(x=closest_x, y=closest_y)
        pyautogui.click(x=closest_x, y=closest_y)
        
        # Now wait and check if worker marks marks updated 
        time.sleep(timer)
        if (worker_marks.state == 1):
            current_building = build_index_next
        else:
            # Stay on this building for next green
            current_building = build_index
    
    return current_building

def handle_fall():
    print("Fall Detected. Going back to start.")
    pyautogui.click(x=1630, y=874)
    time.sleep(8)
    pyautogui.click(x=1230, y=565)
    pyautogui.click(x=1230, y=565)
    time.sleep(9)
    return 0

def start_autosrs():
    # Utilize worker status to calculate next click 
    current_building = 0 # Index starts at 0

    # We are going to assume we start at Block 1 (First building 
    # after the climb up the tree)
    time.sleep(3)
    while (True):
        red_boxes = worker_marks.reds
        green_boxes = worker_marks.greens
        worker_marks_state = worker_marks.state # 0 = Green, 1 = Red

        if ((len(green_boxes) == 0) and (len(red_boxes) == 0)):
            time.sleep(1)
            if (worker.state == 8) and (current_building == 0):
                print("Stuck on ground")
            else:
                continue

        match current_building:
            case 0:
                # If we didn't move for some reason
                # if (worker.state == 8):
                #     pyautogui.click(x=871, y=393)
                #     pyautogui.click(x=871, y=393)
                #     time.sleep(7)
                #     current_building = 0
                #     print("Worker State 8 :: Didn't Move?")
                #     continue
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            0, # build index
                                            1, # next build
                                            5) # timer
            case 1:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            1, # build index
                                            2, # next build
                                            5) # timer
            case 2:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            1, # box index
                                            2, # build index
                                            3, # next build
                                            6) # timer
                # Handle Fall Scenario
                if (worker.state == 7):
                    current_building = handle_fall()
            case 3:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            3, # build index
                                            4, # next build
                                            6) # timer
            case 4:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            4, # build index
                                            5, # next build
                                            7) # timer
            case 5:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            5, # build index
                                            6, # next build
                                            8) # timer
            case 6:
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            6, # build index
                                            7, # next build
                                            5) # timer
                pyautogui.click(x=871, y=393)
                pyautogui.click(x=871, y=393)
                time.sleep(7)
                current_building = 0
            case _: # Default
                print("Will pause to retry")
                time.sleep(1)

if __name__ == "__main__":
    thread1 = threading.Thread(target=start_worker)
    thread2 = threading.Thread(target=start_worker_marks)
    thread3 = threading.Thread(target=start_autosrs)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join() # Wait for thread1 to complete
    thread2.join() # Wait for thread2 to complete
    thread3.join() # Wait for thread2 to complete

    print("All processes finished.")
