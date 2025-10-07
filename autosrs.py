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
    while (True):
        red_boxes = worker_marks.reds
        green_boxes = worker_marks.greens
        worker_state = worker.state # Building Number
        worker_marks_state = worker_marks.state # 0 = Green, 1 = Red
        worker_marks_marks = worker_marks.marks # True = Mark is on Screen

        if ((len(green_boxes) == 0) and (len(red_boxes) == 0)):
            time.sleep(1)
            if (worker.state == 8) and (current_building == 0):
                print("Stuck on ground")
            else:
                continue

        match current_building:
            case 0:
                # If we didn't move for some reason
                if (worker.state == 8):
                    pyautogui.click(x=871, y=393)
                    pyautogui.click(x=871, y=393)
                    time.sleep(7)
                    current_building = 0
                    continue
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            0, # build index
                                            1, # next build
                                            5) # timer
                # pyautogui.click(x=929, y=381)
                # pyautogui.click(x=929, y=381)
            case 1:
                # print("Block 1")
                # # Get closest Green box
                # closest_x, closest_y = green_boxes[0]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=770, y=532)
                # pyautogui.click(x=770, y=532)
                # time.sleep(5)
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            1, # build index
                                            2, # next build
                                            5) # timer
            case 2:
                # print("Block 2")
                # # if state is red (1), take second closest red box
                # # otherwise, take second closest green
                # closest_x, closest_y = green_boxes[1]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # # pyautogui.click(x=716, y=702)
                # # pyautogui.click(x=716, y=702)
                # current_building = 3
                # time.sleep(6)
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
                # print("Block 3")
                # # take closest green
                # closest_x, closest_y = green_boxes[0]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # # pyautogui.click(x=952, y=758)
                # # pyautogui.click(x=952, y=758)
                # current_building = 4
                # time.sleep(6)
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            3, # build index
                                            4, # next build
                                            6) # timer
            case 4:
                # print("Block 4")
                # # take closest green or red 
                # closest_x, closest_y = green_boxes[0]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # # pyautogui.click(x=1014, y=620)
                # # pyautogui.click(x=1014, y=620)
                # current_building = 5
                # time.sleep(7)
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            4, # build index
                                            5, # next build
                                            7) # timer
            case 5:
                # print("Block 5")
                # # Get closest Green box 
                # closest_x, closest_y = green_boxes[0]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # # pyautogui.click(x=1394, y=511)
                # # pyautogui.click(x=1394, y=511)
                # current_building = 6
                # time.sleep(8)
                current_building = handler(worker_marks_state,
                                            green_boxes, 
                                            red_boxes, 
                                            0, # box index
                                            5, # build index
                                            6, # next build
                                            8) # timer
            case 6:
                # print("Block 6")
                # # Get closest Green box 
                # closest_x, closest_y = green_boxes[0]
                # pyautogui.click(x=closest_x, y=closest_y)
                # pyautogui.click(x=closest_x, y=closest_y)
                # # pyautogui.click(x=933, y=349)
                # # pyautogui.click(x=933, y=349)
                # time.sleep(5)
                # pyautogui.click(x=871, y=393)
                # pyautogui.click(x=871, y=393)
                # time.sleep(7)
                # current_building = 1
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
            # case 7:
            #     print("Tree")
            #     # Take tree 
            #     # pyautogui.click(x=871, y=393)
            #     # pyautogui.click(x=871, y=393)
            #     time.sleep(7)
            # case 8:
            #     print("Floor - ToDo")
            #     # pyautogui.click(x=871, y=393)
            #     # pyautogui.click(x=871, y=393)
            #     time.sleep(4)
            case _: # Default
                print("Will pause to retry")
                time.sleep(1)

    # last_state = None

    # while (True):

    #     if (worker_marks.state == 1 or worker_marks.marks == True):
    #         print("In worker_marks")
    #         pyautogui.click(x=worker_marks.closest["x"], y=worker_marks.closest["y"])
    #         pyautogui.click(x=worker_marks.closest["x"], y=worker_marks.closest["y"])
    #         time.sleep(7)
        
    #     else: 
    #         print(f"worker state: {worker.state}")

    #         if (last_state == 2) and (worker.state == 5):
    #             worker.state = 3
            
    #         match worker.state:
    #             case 0:
    #                 print("Block 1")
    #                 # Get closest Green box 
    #                 pyautogui.click(x=929, y=381)
    #                 pyautogui.click(x=929, y=381)
    #                 time.sleep(5)
    #             case 1:
    #                 print("Block 2")
    #                 # Get closest Green box 
    #                 pyautogui.click(x=770, y=532)
    #                 pyautogui.click(x=770, y=532)
    #                 time.sleep(5)
    #             case 2:
    #                 print("Block 3")
    #                 # if state is red (1), take second closest red box
    #                 # otherwise, take second closest green
    #                 pyautogui.click(x=716, y=702)
    #                 pyautogui.click(x=716, y=702)
    #                 time.sleep(6)
    #             case 3:
    #                 print("Block 4")
    #                 # take closest green
    #                 pyautogui.click(x=952, y=758)
    #                 pyautogui.click(x=952, y=758)
    #                 time.sleep(6)
    #             case 4:
    #                 print("Block 5")
    #                 # take closest green or red 
    #                 pyautogui.click(x=1014, y=620)
    #                 pyautogui.click(x=1014, y=620)
    #                 time.sleep(7)
    #             case 5:
    #                 print("Block 6")
    #                 # Get closest Green box 
    #                 pyautogui.click(x=1394, y=511)
    #                 pyautogui.click(x=1394, y=511)
    #                 time.sleep(8)
    #             case 6:
    #                 print("Block 7")
    #                 # Get closest Green box 
    #                 pyautogui.click(x=933, y=349)
    #                 pyautogui.click(x=933, y=349)
    #                 time.sleep(5)
    #             case 7:
    #                 print("Tree")
    #                 # Take tree 
    #                 pyautogui.click(x=871, y=393)
    #                 pyautogui.click(x=871, y=393)
    #                 time.sleep(7)
    #             case 8:
    #                 print("Floor - ToDo")
    #                 # pyautogui.click(x=871, y=393)
    #                 # pyautogui.click(x=871, y=393)
    #                 time.sleep(4)
    #             case _: # Default
    #                 print("Will pause to retry")
    #                 time.sleep(1)
            
    #         last_state = worker.state
            
            # time.sleep(1)  # Pauses the program for 1 seconds

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
