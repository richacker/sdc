import keras
from keras.models import model_from_json
from keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import time
from time import sleep
import timeit
from picamera import PiCamera
import scipy
from skimage import feature
from skimage.color import rgb2gray
from skimage.filters import scharr
import imageio
import RPi.GPIO as GPIO
import numpy as np

GPIO.setwarnings(False)
def silence_imageio_warning(*args, **kwargs):
    pass

imageio.core.util._precision_warn = silence_imageio_warning



GPIO.setmode(GPIO.BCM)
Trig = 14
Echo = 15
Motor1 = 18
Motor2 = 23
Motor3 = 24
Motor4 = 25

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)
GPIO.setup(Motor4, GPIO.OUT)
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

camera = PiCamera()

json_file_m1 = open('/home/pi/self-driving/smodel.json', 'r')
loaded_model_json_m1 = json_file_m1.read()
json_file_m1.close()
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model_m1 = model_from_json(loaded_model_json_m1)
model_m1.load_weights("/home/pi/self-driving/smodel.h5")
print("Loaded stop model from disk")

json_file = open('/home/pi/self-driving/model10.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = model_from_json(loaded_model_json)
model.load_weights("/home/pi/self-driving/model10.h5")
model.compile(loss="categorical_crossentropy",
optimizer="adam", metrics=['accuracy'])
print("Loaded track model from disk")


def capture():

        camera.vflip = True
        camera.capture('captured/all/picture.jpg')


def preprocess():
        images = []
        for filename in os.listdir("/home/pi/self-driving/captured/all"):
                if any([filename.endswith('.jpg')]):
                        img = imageio.imread(os.path.join(
                            "/home/pi/self-driving/captured/all", filename))
                        if img is not None:
                                images.append(img)
        for img in images:
                img = rgb2gray(img)
                img = img[200:480, 0:640]
                edge_scharr = scharr(img)
                imageio.imwrite("/home/pi/self-driving/processed/all/image.jpg", edge_scharr)


def stopModel():
        print("READING STOP IMAGE")
        validation_image_generator = ImageDataGenerator(rescale=1./255)
        test_generator = validation_image_generator.flow_from_directory(
                directory='/home/pi/self-driving/captured',
                target_size=(720, 480),
                color_mode="rgb",
                shuffle=False,
                class_mode='binary',
                batch_size=1
        )

        predict = model.predict_generator(test_generator, steps=1)
        predClass = predict[0].tolist()
        predClass = predClass.index(max(predClass))
        print("Stop Model Prediction", predClass)
      
        return(predClass)

def trackModel():
        print("READING IMAGE")
        validation_image_generator = ImageDataGenerator(rescale=1./255)
        test_generator = validation_image_generator.flow_from_directory(
            directory='/home/pi/self-driving/captured',
                target_size=(720, 480),
                color_mode="rgb",
                shuffle=False,
                class_mode='binary',
                batch_size=1
        )

        predict = model.predict_generator(test_generator, steps=1)
        predClass = predict[0].tolist()
        predClass = predClass.index(max(predClass))
        print("Track Model", predClass)
      
        return(predClass)


def deleteStopImage():
        os.remove("/home/pi/self-driving/captured/all/picture.jpg")

def deleteImages():
        os.remove("/home/pi/self-driving/captured/all/picture.jpg")
        #os.remove("/home/pi/self-driving/processed/all/image.jpg")


while True:
                start = timeit.default_timer()
                capture()
                stopPred = stopModel()
                
                if stopPred == 0:
                         GPIO.output(Motor1, GPIO.LOW)
                         GPIO.output(Motor2,GPIO.LOW)
                         GPIO.output(Motor3,GPIO.LOW)
                         GPIO.output(Motor4,GPIO.LOW)
                         #deleteStopImage()
                else:
                        
                #preprocess()
                        trackPred = trackModel()
                        if trackPred == 0:
                                GPIO.output(Motor1,GPIO.LOW)
                                GPIO.output(Motor2,GPIO.HIGH)
                                GPIO.output(Motor3,GPIO.LOW)
                                GPIO.output(Motor4,GPIO.LOW)
                                time.sleep(1)
                        elif trackPred == 1:
                                GPIO.output(Motor1,GPIO.LOW)
                                GPIO.output(Motor2,GPIO.HIGH)
                                GPIO.output(Motor3,GPIO.LOW)
                                GPIO.output(Motor4,GPIO.HIGH)
                                time.sleep(1)

                        GPIO.output(Motor1, GPIO.LOW)
                        GPIO.output(Motor2,GPIO.LOW)
                        GPIO.output(Motor3,GPIO.LOW)
                        GPIO.output(Motor4,GPIO.LOW)

                        deleteImages()
                        
                stop = timeit.default_timer()
                print('Time: ', stop - start)  
                
        
        
        




        

         


    

        
        
                                                        
