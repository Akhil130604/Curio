import serial
import pyttsx3
import os
def speak():
	#espeak.synth('Hello Ansilla')
	text = "Hello raspi Team"
	#os.system('espeak "'+text+'"')
	engine = pyttsx3.init()
	engine.say("I will speak this text")
	engine.runAndWait()




if __name__=='__main__':
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	ser.flush()
	while True:
		if ser.in_waiting > 0:
			data = ser.readline().decode('utf-8').rstrip()
			print(data)
			#print(type(data))
			if data == "1":
				print("Success!")
				#speak()
				engine = pyttsx3.init()
				engine.say("I will speak this text")

