import cv2
import time

cv2.namedWindow("line")
vc = cv2.VideoCapture(1)
# time.strftime("%H:%M:%S")

out = cv2.VideoWriter('output_' + time.strftime("%H:%M:%S") + '.mp4', -1, 20.0, (640, 480))

line_thickness = 2

if vc.isOpened(): # try to get the first frame
    status, frame = vc.read()
else:
    status = False

while status:
    out.write(frame)
    cv2.line(frame,(140,200), (500,200), (0,0,255), line_thickness)
    cv2.line(frame,(140,240), (500,240), (0,0,255), line_thickness)
    cv2.imshow("line", frame)
    status, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyAllWindows()
out.release()
vc.release()