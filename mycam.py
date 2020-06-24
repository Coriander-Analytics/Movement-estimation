import numpy as np
import cv2

from Arduino import Arduino
import time

# Python-Arduino Command API
board = Arduino("9600", port="/dev/cu.usbmodem14301")
board.pinMode(13, "OUTPUT")
cap = cv2.VideoCapture(0)

# OpenCV API
while(True):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if gray[200][200] < 50:
		board.digitalWrite(13, "HIGH")
	else:
		board.digitalWrite(13, "LOW")
	cv2.imshow('frame', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()