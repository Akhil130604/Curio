import cv2
import tkinter as tk
from tkinter import filedialog

# Create a GUI window to input the filename
root = tk.Tk()
root.withdraw()

filename = filedialog.asksaveasfilename(
    initialdir="/home/pi/all-projects/curio/curio/faces",
    title="Save as",
    filetypes=[("JPEG Image", ".jpg"), ("All Files", ".*")],
)

# Open the webcam
cap = cv2.VideoCapture(0)

# Read the frame from the webcam
ret, frame = cap.read()

# Save the frame as an image with the provided filename
cv2.imwrite(filename, frame)

# Release the webcam and close the GUI window
cap.release()
cv2.destroyAllWindows()