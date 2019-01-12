import RPi.GPIO as GPIO
import time
import keyboard
from mpd import MPDClient
import os
import psutil

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

counter = {}
last_press = {}
INCREMENT = 1
DECREMENT = 2
last_timings = [time.time(),time.time()]
last_buttons = [0,0]
state = "stop"

def get_client():
	try:
		client = MPDClient()
		client.connect("localhost",6600)
	except:
		time.sleep(10)
		client.connect("localhost",6600)
	return client

def setup_pins():
	global counter
	global last_press
	buttons = [17,23,16,26]
	GPIO.setmode(GPIO.BCM)
	for button in buttons:
		GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		counter[button] = 0
		last_press[button] = time.time()
	

def debug(gpio):
	global counter
	if GPIO.input(gpio) == 1:
		print("on %s" % counter[gpio])
		counter[gpio] += INCREMENT
	elif GPIO.input(gpio) == 0:
		print("off %s" % counter[gpio])
		counter[gpio] -= DECREMENT
	else:
		print("%s" % counter[gpio])

def gpio_is_pressed(gpio):
	global counter
	global last_press
	global state
	if counter[gpio] < 0:
		counter[gpio] = 0
	if GPIO.input(gpio) == 1:
		counter[gpio] += INCREMENT
	elif GPIO.input(gpio) == 0:
		counter[gpio] -= DECREMENT
	if counter[gpio] >= 2000:		
		delta = time.time() - last_press[gpio]
		if ((delta >= 3.0) & (delta <= 3.01)):
			counter[gpio] = 0
			print("resetting")
		elif delta >= 3:
			print('You Pressed %s Key! %s %s' % (gpio,delta,state))
			counter[gpio] = 0
			last_press[gpio] = time.time()
			return True

def load_playlist_and_play(playlist,shuffle=False):	
	global state
	print("loading playlist state %s " %state)
	client = get_client()	
	# if state == "playing":		
	# 	client.pause()
	# 	state = "stop"
	# 	#os.system("espeak 'stopping'")
	# 	return
	state = "playing"
	#os.system("espeak 'playing %s'" % playlist)	
	client.clear()
	client.load(playlist)
	if shuffle:
		client.shuffle()
	print("playing")
	client.play(0)		
				
def check_keys():
	global last_buttons
	global last_timings	
	if gpio_is_pressed(17):
		load_playlist_and_play("tzb",False)
		last_buttons.append(17)
		last_timings.append(time.time())
	elif gpio_is_pressed(23):
		load_playlist_and_play("klassik",True)	
		last_buttons.append(23)
		last_timings.append(time.time())
	elif gpio_is_pressed(16):
		load_playlist_and_play("bonobo",True)	
		last_buttons.append(16)
		last_timings.append(time.time())
	elif gpio_is_pressed(26):
		load_playlist_and_play("marley",True)	
		last_buttons.append(26)
		last_timings.append(time.time())	
	else:
		#print("%s %s %s" % (last_buttons[-1],last_buttons[-2],last_timings[-1]-last_timings[-2]))
		pass

#Wait for mopidy
while True:
	if checkIfProcessRunning("mopidy"):
		#os.system("aplay /home/pi/fanfare1.wav")
		break
	else:
		print("Waiting for mopidy...")
	
setup_pins()
get_client()

		
while True:			
	check_keys()
	#debug(26)
GPIO.cleanup()
