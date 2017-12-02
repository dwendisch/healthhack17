import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

line_thickness = 2

# filename = 'winning'
filename = 'good_stuff'

def extract_frames():
    cv2.namedWindow("preview", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("cropped", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("bw", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("threshold", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blur", flags=cv2.WINDOW_AUTOSIZE)
    vidcap = cv2.VideoCapture(filename + '.mp4')
    # vidcap = cv2.VideoCapture(1)

    plt.axis([0, 600, 2900, 7200])
    plt.ion()
    # plt.show()
    xdata = [0]
    ydata = [2000]
    line, = plt.plot(ydata)

    count = -1

    max = -1000000
    min = 1000000

    # x_s = 346
    # y_s = 327
    # x_e = 405
    # y_e = 378
    x_s = 212
    y_s = 320
    x_e = 430
    y_e = 353

    while True:
        count += 1
        if count < 200:
            continue

        success,image = vidcap.read()
        if (not success):
          break
        image_presentation = image.copy()
        # cv2.line(image_presentation, (140, 200), (500, 200), (0, 0, 255), line_thickness)
        # cv2.line(image_presentation, (140, 240), (500, 240), (0, 0, 255), line_thickness)

        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("bw", bw_image)

        # asdf, threshold = cv2.threshold(bw_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        asdf, threshold = cv2.threshold(bw_image, 210, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshold", threshold)

        blur = cv2.medianBlur(threshold, 5)
        bs, contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        contour_index = -1
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            print(area)
            if area > max_area:
                max_area = area
                contour_index = i

        if contour_index == -1:
            print('didnt find a contour')
        cv2.drawContours(image_presentation, contours, contour_index, (0, 0, 255), 3)
        cv2.imshow("preview", image_presentation)

        cv2.imshow("blur", blur)

        cropped = blur[y_s:y_e, x_s:x_e]
        cv2.imshow("cropped", cropped)

        black_count = (x_e - x_s) * (y_e - y_s) - cv2.countNonZero(blur)
        # white_count = cv2.countNonZero(blur)
        if black_count > max:
            max = black_count
            print('new max', max)
        elif black_count < min:
            min = black_count
            print('new min', min)
        # print(black_count)
        # plt.scatter(count, cv2.countNonZero(blur))
        # plt.plot([count])
        xdata.append(count)
        ydata.append(black_count)
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        # plt.draw()
        # plt.pause(0.5)
        plt.pause(0.0333)
        # plt.pause(0.1)
        #


        # key = cv2.waitKey(50)
        # if key == 27:  # exit on ESC
        #   break
    print('min', min)
    print('max', max)
    while true:
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
          break
    cv2.destroyAllWindows()

def cutout_image():
    img = cv2.imread(os.path.join(frames_dirname, ("frame%d.jpg" % lower_bound)))
    crop_img = img[328:(328 + 250), 525:(330 + 525)]  # Crop from x, y, w, h -> 100, 200, 300, 400
    cv2.imwrite('sadf.jpg', crop_img)

extract_frames()
