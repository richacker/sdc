import RPi.GPIO as GPIO
import time
from time import sleep
import paho.mqtt.client as paho
from picamera import PiCamera


camera = PiCamera()
broker="mqtt.thingify.xyz"
decode="hello"
GPIO.setmode(GPIO.BCM)
Trig=14
Echo=15
Motor1= 18
Motor2= 23
Motor3= 24
Motor4= 25
s="m"
flag = 0

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)
GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)


def forward():

     GPIO.output(Motor1,GPIO.LOW)
     GPIO.output(Motor2,GPIO.HIGH)
     GPIO.output(Motor3,GPIO.LOW)
     GPIO.output(Motor4,GPIO.HIGH)
     print('Forward')
     
     
def right():
     
     GPIO.output(Motor1,GPIO.LOW)
     GPIO.output(Motor2,GPIO.HIGH)
     GPIO.output(Motor3,GPIO.LOW)
     GPIO.output(Motor4,GPIO.LOW)
     print('Right')

def left():

     GPIO.output(Motor1,GPIO.LOW)
     GPIO.output(Motor2,GPIO.LOW)
     GPIO.output(Motor3,GPIO.LOW)
     GPIO.output(Motor4,GPIO.HIGH)
     print('Left')

def stop():
     
      GPIO.output(Motor1,GPIO.LOW)
      GPIO.output(Motor2,GPIO.LOW)
      GPIO.output(Motor3,GPIO.LOW)
      GPIO.output(Motor4,GPIO.LOW)
      print('Stop')

try: 
  def on_message(client, userdata, msg):
    print("On", str(msg.payload.decode("utf-8")))
    mess = str(msg.payload.decode("utf-8")).strip()
    if mess == "f":
      forward()
      
    elif mess == "s":
      stop()
      
    elif mess == "l":
      right()
      time.sleep(0.5)

    elif mess == "r":
      left()
      time.sleep(1.5) 



  client= paho.Client(str(round(time.time() * 1000))) 

  client.username_pw_set(username="thingify",password="T#i_@i_2018")
  client.on_message=on_message

  print("connecting to broker ",broker)
  client.connect(broker)#connect
  client.subscribe("hello")
  print("subscribing ")
  client.loop_forever()
          
          
except KeyboardInterrupt:
        GPIO.cleanup()
