
from gpiozero import DistanceSensor
import os
#loading model
from keras.models import load_model
import numpy as np
from collections import deque
import RPi.GPIO as gpio
import time

cnn = load_model("garbage1.h5")
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)

def init():
    #12,16,20,21 -drivermoter 1 gripper moter    12,16 gripper      20,21 up or down control
    #6,13,19,26 .   drivermoter 2 movement moter            6,13 left 19,26 right wheel
    #2,3             ultra sonic sensor
    gpio.setmode(gpio.BCM)
    gpio.setup(2,gpio.OUT)
    gpio.setup(3,gpio.OUT)
    gpio.setup(6,gpio.OUT)
    gpio.setup(12,gpio.OUT)   
    gpio.setup(13,gpio.OUT)
    gpio.setup(16,gpio.OUT)
    gpio.setup(19,gpio.OUT)
    gpio.setup(20,gpio.OUT)
    gpio.setup(21,gpio.OUT)
    gpio.setup(26,gpio.OUT) 
# move foreward()
def moveforward():
    t = 0.5     #time setting
    init()
    gpio.output(6, False)    
    gpio.output(13, True)
    gpio.output(19, True)
    gpio.output(29, False)
    time.sleep(t)
    gpio.cleanup()

def movebackward():
    t = 0.5
    init()
    gpio.output(6, False)
    gpio.output(13, True)
    gpio.output(19, False)
    gpio.output(29, True)
    time.sleep(tf)
    gpio.cleanup()

def avoid_obstacle():
    t = 10
    init()
    #turn right
    gpio.output(6, True)
    gpio.output(13, False)
    gpio.output(19, False)
    gpio.output(29, False)
    time.sleep(tf)
    gpio.cleanup()

def pickup()
    #gripper control code pins 12,16
    init()
    #hold or close
    gpio.output(12, True) 
    gpio.output(16, False)

    #up
    #movement control 20,21

    gpio.output(20,True)
    gpio.output(21,False)
    time.sleep(5)
    gpio.output(20,False)
    gpio.output(21,False)


def move_to_place():
    init()
        t = 10
    init()
    #turn left
    gpio.output(6, True)
    gpio.output(13, False)
    gpio.output(19, False)
    gpio.output(29, False)
    time.sleep(tf)
    gpio.output(6, False)
    gpio.output(13, False)
    gpio.output(19, False)
    gpio.output(29, False)
    #gpio.cleanup()

def place():
    move_to_place()
    #down
    #movement control 20,21
    #down
    gpio.output(20,False)
    gpio.output(21,True)
    time.sleep(5)
    #leave gripper
    gpio.output(12, False) 
    gpio.output(16, True)








    

# main loop
while True :
        
    #ultrasonic distance setting to optimum distance to pick
    
    distance = ultrasonic.distance
    while(distance>0.3):
        moveforward()
        distance = ultrasonic.distance
    while(distance<0.3):
        movebackward()
        distance = ultrasonic.distance

    #take snap
    os.system("raspistill -o picture.jpg")
    #function that returns prediction
    def keras_predict(model, image):
        processed = image
        print("processed: " + str(processed.shape))
        pred_probab = model.predict(processed)[0]
        pred_class = list(pred_probab).index(max(pred_probab))
        dict_labels = {1:"trash",2:"metal",3:"paper",4:"cardboard",5:"plastic",6:"glass"}
        return max(pred_probab), dict_labels[pred_class]


    from keras.preprocessing import image
    test_image = image.load_img('picture.jpg', target_size = (150, 150))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = cnn.predict(test_image)


    a = keras_predict(cnn,test_image)
    print(a)
    flag_garbage = True

    if(flag_garbage == True):
        pickup()
    else:
        avoid_obstacle() #move left or right

    