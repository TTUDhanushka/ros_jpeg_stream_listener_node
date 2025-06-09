#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import cv_bridge
import numpy as np
import cv2


file_count = 0
ros_topic =''

def integer_to_char(integer_to_convert) -> list:
    DECIMAL = 10
    char_string = []
    diviser = integer_to_convert

    if diviser < DECIMAL:
        char_string.append(str(round(diviser)))

    # Split the number
    while diviser >= DECIMAL:
        remainder = diviser % DECIMAL
        diviser -= remainder
        diviser /= DECIMAL

        char_string.append(str(round(remainder)))

        if diviser < DECIMAL:
            char_string.append(str(round(diviser)))

    # Reverse the list
    reversed_list = []
    for digit in range(len(char_string)):
        reversed_list.append(char_string[(len(char_string) - 1) - digit])

    return reversed_list


def to_fixed_char_count_string(number_as_list, char_count) -> str:
    file_prefix = []

    for i in range(char_count):
        file_prefix.append("0")

    if char_count >= len(number_as_list):
        for char in range(len(number_as_list)):
            file_prefix[(char_count - len(number_as_list)) + char] = number_as_list[char]

    str_out = ''.join(file_prefix)

    return str_out

def video_decoder(message):
    np_arr = np.fromstring(message.data, np.uint8)
    global file_count
    global ros_topic

    print(f"Received image format: {message.format}")

    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    dir = '/home/dhanushka/IceBucket/3. Extracted_data/9. 2025-03 Soela Ferry/2025-02-23-13-13-25_0/image_topic_thermal/'
    # dir = '/home/dhanushka/x/'
    file_prefix = '_frame_'
    str_file_count = to_fixed_char_count_string(integer_to_char(file_count), 6)

    file_name = ros_topic + file_prefix + str_file_count +'.jpg'
    file_count += 1

    file_path = dir + file_name
    print(f"Writing {file_path} to disk")

    cv2.imwrite(file_path, image_np)
    cv2.imshow("Image",image_np)
    cv2.waitKey(2)


def main():
    global file_count
    global ros_topic

    ros_topic = 'image_topic_thermal' #'cam1_image'

    rospy.init_node('video_listener', anonymous=False)

    rospy.Subscriber(ros_topic, CompressedImage, video_decoder)

    rospy.Rate(10)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print(f"Shutting down")


if __name__ == "__main__":
    main() 
