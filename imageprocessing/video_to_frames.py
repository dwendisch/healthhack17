import cv2
import matplotlib.pyplot as plt
import socket

line_thickness = 2

# filename = 'winning'
# filename = 'artifacts_but_still_right'
# filename = 'test'
filename = 'test_w_black'
# filename = "good_stuff"


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytes(MESSAGE, 'UTF-8'))
# data = s.recv(BUFFER_SIZE)
s.close()


def extract_frames():
    cv2.namedWindow("bw", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("threshold", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blur", flags=cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("preview", flags=cv2.WINDOW_AUTOSIZE)
    vidcap = cv2.VideoCapture(filename + '.mp4')
    # vidcap = cv2.VideoCapture(1)

    # plt.axis([0, 600, 4900, 11000])
    plt.axis([0, 600, -20, 120])
    plt.ion()
    xdata = [0]
    ydata = [0]
    line, = plt.plot(ydata)

    count = -1

    max_area = -1000000
    min_area = 1000000
    global_min = min_area
    global_max = max_area

    while True:
        count += 1

        success,image = vidcap.read()
        if (not success):
            print('could not read from video input')
            break
        image_presentation = image.copy()

        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("bw", bw_image)

        asdf, threshold = cv2.threshold(bw_image, 230, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshold", threshold)

        # black image to start calibration
        if cv2.countNonZero(threshold) < 20 * 10:
            count = 0

        blur = cv2.medianBlur(threshold, 5)
        bs, contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) >= 2:
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

            contour_area = (640 * 480) - cv2.contourArea(contours[lower_contour_index])
            print('contourarea', contour_area)
            if contour_area > max_area:
                max_area = contour_area
                #print('new max', max)
            elif contour_area < min_area:
                min_area = contour_area
                #print('new min', min)

        cv2.imshow("preview", image_presentation)
        cv2.imshow("blur", blur)

        if count == 150:
            ratio = (max_area - min_area) / 50
            global_min = min_area - 20 * ratio  # so that the minimum is at 20
            global_max = max_area + 30 * ratio # so that the maximum is at 70
            print('Calibration finished')
        elif count > 150 and contour_area:
            normalized_area = 100 * (contour_area - global_min) / (global_max - global_min)
            xdata.append(xdata[-1] + 1)
            line.set_xdata(xdata)
            if normalized_area < 0 or normalized_area > 100:
                normalized_area = 0 if normalized_area < 0 else 100
            ydata.append(normalized_area)
            line.set_ydata(ydata)
        # plt.pause(0.5)
        plt.pause(0.0333)
        # plt.pause(0.1)

    print('min', min_area)
    print('max', max_area)
    while True:
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
          break
    cv2.destroyAllWindows()

extract_frames()
