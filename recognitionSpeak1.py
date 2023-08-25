import face_recognition
import os, sys
import cv2
import numpy as np
import math
import pyttsx3
#from guizero import App, PushButton, TextBox,Text
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import threading
from queue import Queue

def speak(name):
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('rate',150)
    engine.say("hello"+name)
    engine.runAndWait()
    engine.say("i am curio 3 point O")
    engine.runAndWait()
    engine.say( "welcome to tiara twenty twenty three")
    engine.runAndWait()

# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition ():
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = False


    def __init__(self):
        self.encode_faces()
        self.frame_queue=Queue()
        self.data_queue=Queue()
        
    def run(self):
        t1=Thread(target=fr.run_recognition)
        t2=Thread(target=fr.gui)
        t1.deamon=True
        t2.deamon=True
        t1.start()
        t2.start()
        
        
        
    def gui(self):
        # Create a GUI window to input the filename
        data=self.data_queue.get()
        if data == "":
            root = tk.Tk()
            root.withdraw()
        while True:
            frame=self.frame_queue.get()
            filename = filedialog.asksaveasfilename(
                initialdir="/home/pi/all-projects/curio/curio/faces",
                title="Save as",
                filetypes=[("JPEG Image", ".jpg"), ("All Files", ".*")],)
            cv2.imwrite(filename, frame)
            root.destroy()
            print("done")

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')
        
        justonce=1
        counterToSkipFrame = 0
        unknownCounter = 0
        
        while True:
            ret, frame = video_capture.read()
            self.frame_queue.put(frame)

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = ""
                    nameForSpeak = ""
                    confidence = '91.00'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        nameForSpeak = name
                        # Getting the confidence
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')
                
                if self.process_current_frame == True:
                    self.process_current_frame = False

            
            counterToSkipFrame = counterToSkipFrame+1

            if counterToSkipFrame == 40:
                self.process_current_frame = not self.process_current_frame
                counterToSkipFrame = 0

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                #print("Hello " + name[0:len(name)-13])

                #print("HERE: "+str(len(nameForSpeak)+len("s  s"))+" string: "+nameForSpeak)

                
                data=nameForSpeak[0:len(nameForSpeak)-4]
                self.data_queue.put(data)

                # data= name.split('.')[:-1]
                if justonce==1:
                    previousData=nameForSpeak[0:len(nameForSpeak)-4]
                    previousflag=0
                    justonce=0
                
#                 if data == "":
#                     gui(frame,data)
                    
                
                if data == previousData and data == "":
                    unknownCounter = unknownCounter + 1
                    print(unknownCounter)
                if unknownCounter == 300:
                    unknownCounter = 0
                    previousflag = 0

#                 print("Hello " + name[0:len(name)-13])
                if(data==previousData):
                    print("check_1")
                    print("data: "+data + "length : "+ str(len(data)))
                    print("previousData: "+previousData+ " length : "+ str(len(previousData)))
                    if previousflag==0:
                        previousData=nameForSpeak[0:len(nameForSpeak)-4]
                        print("check2")
                        print("=======================================================previousData: "+previousData+ " length : "+ str(len(previousData)))
                        # Check whether the confidence is greater than 70%
                        print(type(confidence))
                        print(float(confidence[0:len(confidence)-1]))
                        if int(float(confidence[0:len(confidence)-1])) > 90:
                            speak(nameForSpeak[0:len(nameForSpeak)-4])
                        previousflag=1
                else:
                    previousflag=0
                    unknownCounter = 0
                    print("check3")
                    previousData=data
                    
            # Display the resulting image
#             frame=cv2.resize(frame,(720,720))
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run()
