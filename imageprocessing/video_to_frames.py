import cv2
import os

filename = 'winning'
frames_dirname = 'frames_' + filename

def extract_frames():
    #os.mkdir(frames_dirname)
    cv2.namedWindow("preview", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("cropped", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("bw", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("threshold", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blur", flags=cv2.WINDOW_AUTOSIZE)
    vidcap = cv2.VideoCapture(filename + '.mov')

    while True:
        success,image = vidcap.read()
        if (not success):
          break
        cv2.imshow("preview", image)

        cropped = image[330:390, 610:690]
        cv2.imshow("cropped", cropped)

        bw_image = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imshow("bw", bw_image)
        asdf, threshold = cv2.threshold(bw_image, 240, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshold", threshold)
        blur = cv2.medianBlur(threshold, 7)
        cv2.imshow("blur", blur)
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
          break
    cv2.destroyWindow("preview")
    cv2.destroyWindow("bw")
    cv2.destroyWindow("cropped")
    cv2.destroyWindow("threshold")
    cv2.destroyWindow("blur")

def cutout_image():
    img = cv2.imread(os.path.join(frames_dirname, ("frame%d.jpg" % lower_bound)))
    crop_img = img[328:(328 + 250), 525:(330 + 525)]  # Crop from x, y, w, h -> 100, 200, 300, 400
    cv2.imwrite('sadf.jpg', crop_img)

extract_frames()
