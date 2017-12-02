import cv2

cv2.namedWindow("line")
vc = cv2.VideoCapture(1)

line_thickness = 2

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.line(frame,(140,200), (500,200), (0,0,255), line_thickness)
    cv2.line(frame,(140,240), (500,240), (0,0,255), line_thickness)
    cv2.imshow("line", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("line")