import cv2
import os
# print(cv2.__version__)

# filename = 'short'
filename = 'long'
frames_dirname = 'frames_' + filename
lower_bound = 3128
upper_bound = 3357

def extract_frames():
    os.mkdir(frames_dirname)

    vidcap = cv2.VideoCapture(filename + '.mp4')
    success,image = vidcap.read()
    count = 0
    success = True

    while success:
      success,image = vidcap.read()
      # print('Read a new frame: ', success)
      if (count >= 3128 and count <= 3357):
          cv2.imwrite(os.path.join(frames_dirname, ("frame%d.jpg" % count)), image)
      count += 1

def cutout_image():
    img = cv2.imread(os.path.join(frames_dirname, ("frame%d.jpg" % lower_bound)))
    crop_img = img[328:(328 + 250), 525:(330 + 525)]  # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    cv2.imwrite('sadf.jpg', crop_img)

# extract_frames()
cutout_image()