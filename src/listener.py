#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import cv_bridge
import numpy as np
import cv2

file_count = 0

def video_decoder(message):
    np_arr = np.fromstring(message.data, np.uint8)
    global file_count
    print(f"Received image format: {message.format}")

    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    dir = '/home/dhanushka/2025 Soela Ferry Results/Extracted data/2025-02-24-09-51-57_0/cam_1/'
    # dir = '/home/dhanushka/x/'
    file_prefix = 'frame'

    file_name = file_prefix + str(file_count)+'.jpg'
    file_count += 1

    file_path = dir + file_name
    print(f"Writing {file_path} to disk")

    cv2.imwrite(file_path, image_np)
    cv2.imshow("Image",image_np)
    cv2.waitKey(2)


def main():
    global file_count

    rospy.init_node('video_listener', anonymous=False)

    rospy.Subscriber('cam1_image', CompressedImage, video_decoder)
    rospy.Rate(10)

    while not rospy.is_shutdown():
        file_count += 1

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print(f"Shutting down")


if __name__ == "__main__":
    main() 
