import cv2
import pyrealsense2 as rs
import numpy as np

# def take_picture():
#
#     if cap.isOpened():
#         _, frame = cap.read()
#         # cv2.imwrite("teste.jpg", frame)
#
#     return frame
#
# cap = cv2.VideoCapture(2)
# # focus = 1  # multiplos de 5
# # cap.set(28, focus)
# cap.set(3, 1280)
# cap.set(4, 720)
#
# while (1):
#     ret, frame = cap.read()
#     cv2.imshow("Video", frame)
#     take_picture()
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
# cap.release()
# cv2.destroyAllWindows()

def take_picture_realsense():

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline.start(config)
    count = 0
    while count <= 12:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        count+=1

    cv2.imwrite('teste14.jpg', color_image)




frame = take_picture_realsense()
