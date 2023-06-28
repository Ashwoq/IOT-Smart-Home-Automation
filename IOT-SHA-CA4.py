import telepot
import RPi.GPIO as GPIO
from time import sleep
import datetime
from telepot.loop import MessageLoop

touch = 16
servo = 18
buzzz = 22
flame = 36

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(touch,GPIO.IN)
GPIO.setup(flame,GPIO.IN)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(buzzz,GPIO.OUT)
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BOARD	)
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

msg=GPIO.PWM(servo,50)
msg.start(2.5)
GPIO.output(buzzz,False)
motion = 0
motionNew = 0
 
  
def bell():
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.1)
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.1)
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.2)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.2)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.2)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.1)
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.1)
    GPIO.output(22,GPIO.HIGH)
    sleep(.1)
    GPIO.output(22,GPIO.LOW)
    sleep(.7)
    
def flames():
    GPIO.output(22,GPIO.HIGH)
    sleep(2)
    GPIO.output(22,GPIO.LOW)
    sleep(.5)
    GPIO.output(22,GPIO.HIGH)
    sleep(2)
    GPIO.output(22,GPIO.LOW)
    sleep(.5)
    GPIO.output(22,GPIO.HIGH)
    sleep(2)
    GPIO.output(22,GPIO.LOW)
    sleep(.5)
    GPIO.output(22,GPIO.HIGH)
    sleep(2)
   
def dooropening():
    GPIO.output(22,GPIO.HIGH)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.5)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.5)
    GPIO.output(22,GPIO.LOW)
    sleep(.2)
    GPIO.output(22,GPIO.HIGH)
    sleep(.5)

def call_btn():
    bell()
    GPIO.output(22,GPIO.LOW)

def fire_alarm():
    msg.ChangeDutyCycle(12.5)
    flames()
    GPIO.output(22,GPIO.LOW)
    
def open_door():
    msg.ChangeDutyCycle(12.5)
    dooropening()

def handle(msg):
    global telegramText
    global chat_id
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
  
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Welcome to House Notification')

    while True:
        main()
        
bot = telepot.Bot('6004655891:AAExL2_WbrJxmqnjT0hGtX5M1FtPN1a6ZsY')
bot.message_loop(handle)		
   
           

def main():
	    
    global chat_id
    global motion 
    global motionNew
    global telegramText
    
    if GPIO.input(37) == 1:
        motion = 1
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
        call_btn()
            
    elif telegramText == '/opened':
        bot.sendMessage(chat_id, 'OPENING ...')       
#     elif GPIO.input(37) == 0:
#         print("No motion detected")
#         motion = 0
#         if motionNew != motion:
#             sendNotification(motion)
#             motionNew = motion
            
    elif(GPIO.input(touch)==1):
        motion = 3
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
        open_door()
        
    elif(GPIO.input(flame)==1):
        motion = 5
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
        fire_alarm()
            
#     elif(GPIO.input(37)==1):
#         print("sfsdcsdfsdfdsfdsfdsf")
#         sleep(5)
#         call_btn()
            
    elif(GPIO.input(touch)==0 or GPIO.input(flame)==0 or GPIO.input(37)==1):
        msg.ChangeDutyCycle(2.5)
        GPIO.output(22,GPIO.LOW)
        motion = 4
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
            
    


def sendNotification(motion):   

    global chat_id
    
    if motion == 1:
        bot.sendMessage(chat_id, 'Someone is at your front door')
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif motion == 0:
        bot.sendMessage(chat_id, 'Nobody is at your front door')
    elif motion == 3:
        bot.sendMessage(chat_id, 'Door is opening !!!')
    elif motion == 4:
        bot.sendMessage(chat_id, 'Door is closed...')
    elif motion == 5:
        bot.sendMessage(chat_id, 'FIRE ALERT - OPENING ALL THE DOOR ...')


while 1:
    sleep(10)      
