import cv2
import matplotlib.pyplot as plt

line_thickness = 2

# filename = 'winning'
# filename = 'artifacts_but_still_right'
# filename = 'test'
filename = "good_stuff"

def extract_frames():
    cv2.namedWindow("bw", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("threshold", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blur", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("preview", flags=cv2.WINDOW_AUTOSIZE)
    vidcap = cv2.VideoCapture(filename + '.mp4')
    # vidcap = cv2.VideoCapture(1)

    # plt.axis([0, 600, 4900, 11000])
    plt.axis([0, 600, 0, 100])
    plt.ion()
    xdata = []
    ydata = []
    line, = plt.plot(ydata)

    count = -1

    max = -1000000
    min = 1000000
    global_min = min
    global_max = max

    while True:
        count += 1

        success,image = vidcap.read()
        if (not success):
          break
        image_presentation = image.copy()

        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("bw", bw_image)

        asdf, threshold = cv2.threshold(bw_image, 230, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshold", threshold)

        blur = cv2.medianBlur(threshold, 5)
        bs, contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours.sort(key=lambda contour: cv2.contourArea(contour), reverse=True)

        contours = contours[0:2]

        M_0 = cv2.moments(contours[0])
        M_1 = cv2.moments(contours[1])
        cy_0 = int(M_0['m01'] / M_0['m00'])
        cy_1 = int(M_1['m01'] / M_1['m00'])

        if cy_0 >= cy_1:
            lower_contour_index = 0
        else:
            lower_contour_index = 1

        cv2.drawContours(image_presentation, contours, lower_contour_index, (0, 0, 255), 3)
        cv2.imshow("preview", image_presentation)

        cv2.imshow("blur", blur)

        contour_area = 11000 - cv2.contourArea(contours[lower_contour_index])
        print('contourarea', contour_area)
        if contour_area > max:
            max = contour_area
            #print('new max', max)
        elif contour_area < min:
            min = contour_area
            #print('new min', min)


        if count == 150:
            ratio = (max - min) / 50
            global_min = min - 20 * ratio  # so that the minimum is at 20
            global_max = max + 30 * ratio # so that the maximum is at 70
            print('Calibration finished')
        elif count > 150:
            normalized_area = 100 * (contour_area - global_min) / (global_max - global_min)
            xdata.append(count - 150)
            ydata.append(normalized_area)
            line.set_xdata(xdata)
            line.set_ydata(ydata)
        # plt.pause(0.5)
        plt.pause(0.0333)
        # plt.pause(0.1)

    print('min', min)
    print('max', max)
    while True:
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
          break
    cv2.destroyAllWindows()

extract_frames()
