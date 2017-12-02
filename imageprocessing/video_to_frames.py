import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

line_thickness = 2

# filename = 'winning'
filename = 'good_stuff'

def extract_frames():
    cv2.namedWindow("cropped", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("bw", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("threshold", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blur", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("preview", flags=cv2.WINDOW_AUTOSIZE)
    vidcap = cv2.VideoCapture(filename + '.mp4')
    # vidcap = cv2.VideoCapture(1)

    # plt.axis([0, 600, 4900, 11000])
    plt.axis([0, 600, 0, 6100])
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

        areas = []
        contours.sort(key=lambda contour: cv2.contourArea(contour), reverse=True)

        # for i, contour in enumerate(contours):

            # areas.append({'area': cv2.contourArea(contour), 'index': )
            # print(area)
            # if area > max_area:
            #     max_area = area
            #     contour_index = i


        # if contour_index == -1:
        #     print('didnt find a contour')
        contours = contours[0:2]

        M_0 = cv2.moments(contours[0])
        M_1 = cv2.moments(contours[1])
        cy_0 = int(M_0['m01'] / M_0['m00'])
        cy_1 = int(M_1['m01'] / M_1['m00'])

        if cy_0 >= cy_1:
            lower_contour_index = 0
        else:
            lower_contour_index = 1

        # scnd_biggest_contour_index = 1
        cv2.drawContours(image_presentation, contours, lower_contour_index, (0, 0, 255), 3)
        cv2.imshow("preview", image_presentation)

        cv2.imshow("blur", blur)

        cropped = blur[y_s:y_e, x_s:x_e]
        cv2.imshow("cropped", cropped)

        black_count = (x_e - x_s) * (y_e - y_s) - cv2.countNonZero(blur)
        # white_count = cv2.countNonZero(blur)
        # print(black_count)
        contour_area = 11000 - cv2.contourArea(contours[lower_contour_index])
        # plt.scatter(count, contour_area)
        print('contourarea', contour_area)
        if contour_area > max:
            max = contour_area
            print('new max', max)
        elif contour_area < min:
            min = contour_area
            print('new min', min)

        # plt.plot([count])
        xdata.append(count)
        ydata.append(contour_area)
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
