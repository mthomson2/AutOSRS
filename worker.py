import torch
from torchvision import transforms
from utils.prepare_dataset import Net, PATH, imshow
import mss
import mss.tools
import cv2 # For image processing and saving
import time
import numpy as np
from PIL import Image

# Window 1 Region
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} 

class Worker():

    def __init__(self):
        super().__init__()
        self.state = None
    
    def run(self):
        model = Net() 
        model.load_state_dict(torch.load(PATH))
        model.eval() # Set the model to evaluation mode

        data_transforms = transforms.Compose([
            transforms.Resize((512, 512)), # was 224
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # Initialize mss
        sct = mss.mss()

        while True:
            # Grab the image from the screen
            sct_img = sct.grab(monitor)

            # Convert the raw pixels to a NumPy array
            img_array = np.array(sct_img)
            img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
            img_t = data_transforms(img).unsqueeze(0)  # Add batch dimension

            # Perform inference
            with torch.no_grad():
                output = model(img_t)
                # the class with the highest energy is what we choose as prediction
                _, predicted = torch.max(output, 1)
                predicted_class = predicted.item()  # Convert tensor to integer
                self.state = predicted_class

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break