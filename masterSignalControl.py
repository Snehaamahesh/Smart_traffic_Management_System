# Import necessary packages
import cv2
import collections
import numpy as np
import time

#GUI Traffic Signal
from trafficSignal import *

# Input Image Size
input_size = 320

# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2

# Store Coco Names in a list
classesFile = "coco.names"
classNames = open(classesFile).read().strip().split('\n')
#print(classNames)

# class index for our required detection classes
#car,motorbike,bus,truck
required_class_index = [2, 3, 5, 7]

detected_classNames = []

#Model Files
modelConfiguration = 'yolov3-320.cfg'
modelWeigheights = 'yolov3-320.weights'

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

# Configure the network backend

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Function for finding the center of a rectangle
def find_center(x, y, w, h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy=y+y1
    return cx, cy
    
# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0]
down_list = [0, 0, 0, 0]

# Function for finding the detected objects from the network output
def postProcess(outputs,img):
    global detected_classNames 
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    if(len(indices)>0):
      for i in indices.flatten():
        x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
        # print(x,y,w,h)

        #color = [int(c) for c in colors[classIds[i]]]
        name = classNames[classIds[i]]
        detected_classNames.append(name)
        detection.append([x, y, w, h, required_class_index.index(classIds[i])])



def from_static_image(image):
    img = cv2.imread(image)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    #outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
    outputNames = ['yolo_82', 'yolo_94', 'yolo_106']
    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    postProcess(outputs,img)

    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    
    print(image)
    print(frequency)
    
    return([frequency['car'] + frequency['motorbike'] + frequency['bus'] + frequency['truck'],image])

def clearSignal() :
    print("######## After 60s #########")
    light["North"].clearAll()
    light["South"].clearAll()
    light["East"].clearAll()
    light["West"].clearAll()    

def traffic_update(sides):
    for i in sides:
        side=i[1]
        print(side)
        if(side=="side1.jpg"):
            print("side1","Green")
            light["North"].setGreen()
        else:
            print("side1","Red")
            light["North"].setRed()
            
        if(side=="side2.jpg"):
            print("side2","Green")
            light["South"].setGreen()
        else:
            print("side2","Red")
            light["South"].setRed()
            
        if(side=="side3.jpeg"):
            print("side3","Green")
            light["East"].setGreen()
        else:
            print("side3","Red")
            light["East"].setRed()
            
        if(side=="side4.jpg"):
            print("side4","Green")
            light["West"].setGreen()
        else:
            print("side4","Red")
            light["West"].setRed()
        top.update()
        time.sleep(3)
        clearSignal()

if __name__ == '__main__':
    # start simulation
    top = Tkinter.Tk()
    #four side images
    sides = ["side1.jpg", "side2.jpg", "side3.jpeg","side4.jpg"]
    processed = []
    for side in sides:
        processed.append(from_static_image(side))
        #clear previous data
        detected_classNames=[]
    processed.sort(reverse = True)
    
    print()
    C = Tkinter.Canvas(top, bg="white", height=370, width=430)
    light={} # hold four traffic signals
    light["North"] = traffic_signal("North",C,0)
    light["South"] = traffic_signal("South",C,110)
    light["East"] = traffic_signal("East",C,220)
    light["West"] = traffic_signal("West",C,330)
    C.pack()
    clearSignal()
    traffic_update(processed)

    
