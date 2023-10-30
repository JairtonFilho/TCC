import cv2

# Path to video file

def FrameCapture(path):
    vidObj = cv2.VideoCapture(path)

    count = 0

    success = 1

    while success:
        success, image = vidObj.read()
        cv2.imwrite("C:/Users/jsff/Desktop/frames_terminal_2020/terminal%d.jpg" % count, image)


        count += 1
if __name__ == '__main__':
    FrameCapture("C:/Users/jsff/Pictures/Camera Roll/terminal.mp4")